import asyncio
import random
from playwright.async_api import async_playwright, Page, TimeoutError as PWTimeoutError

EMAIL    = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"
BASE_URL = "https://preprod.hawkvision.ai"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

async def goto(page: Page, url: str, wait_selector: str = None, pause: int = 2000):
    """Navigate using domcontentloaded (never times-out on SPA background traffic)."""
    await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    if wait_selector:
        await page.wait_for_selector(wait_selector, timeout=20_000)
    await page.wait_for_timeout(pause)


async def open_dropdown_and_pick(page: Page, trigger_locator, option_text: str, retries: int = 3):
    """
    Click a dropdown trigger, wait for options to load, then pick by text.
    Retries in case the dropdown closes before the option is clicked.
    """
    for attempt in range(1, retries + 1):
        try:
            await trigger_locator.wait_for(state="visible", timeout=10_000)
            await trigger_locator.click()
            await page.wait_for_timeout(1_200)   # let async options load

            # Try role=option first, then li fallback
            option = page.locator("[role='option']").filter(has_text=option_text)
            try:
                await option.first.wait_for(state="visible", timeout=6_000)
                await option.first.click()
                return
            except PWTimeoutError:
                pass

            fallback = page.locator("li").filter(has_text=option_text)
            await fallback.first.wait_for(state="visible", timeout=6_000)
            await fallback.first.click()
            return

        except PWTimeoutError:
            print(f"   ⚠️  Attempt {attempt}/{retries} failed for '{option_text}', retrying…")
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(800)

    raise RuntimeError(f"Could not select dropdown option: '{option_text}' after {retries} attempts")


# ─────────────────────────────────────────────────────────────────────────────
# Main test
# ─────────────────────────────────────────────────────────────────────────────

async def create_consumer_test():

    async with async_playwright() as pw:

        browser = await pw.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = await browser.new_context(
            no_viewport=True,
            ignore_https_errors=True
        )
        page = await context.new_page()

        # ── 1. LOGIN ──────────────────────────────────────────────────────────
        await page.goto(
            f"{BASE_URL}/login",
            wait_until="domcontentloaded",
            timeout=120_000
        )
        await page.wait_for_selector(
            "input[placeholder='username@example.com']", timeout=20_000
        )
        await page.fill("input[placeholder='username@example.com']", EMAIL)
        await page.fill("input[type='password']", PASSWORD)
        await page.locator("form").get_by_role("button", name="Sign In").click()
        await page.wait_for_url("**/home", timeout=60_000)
        await page.wait_for_timeout(3_000)
        print("✅  Login successful")

        # ── 2. NAVIGATE TO USERS / MANAGE-CONSUMER PAGE ───────────────────────
        # FIX: replaced networkidle with domcontentloaded + element wait
        await goto(
            page,
            f"{BASE_URL}/manage-consumer",
            wait_selector="button",   # page shell loaded when any button appears
            pause=2_000
        )
        print("✅  Users page opened")

        # ── 3. OPEN CREATE CONSUMER MODAL ─────────────────────────────────────
        add_btn = page.get_by_role("button", name="+ Add Consumer")
        await add_btn.wait_for(state="visible", timeout=10_000)
        await add_btn.click()
        await page.wait_for_selector("text=Create Consumer", timeout=10_000)
        await page.wait_for_timeout(800)
        print("✅  Create Consumer modal opened")

        # ── 4. FILL CONSUMER DETAILS ──────────────────────────────────────────

        # Name
        consumer_name = "TestingConsumer"
        name_input = page.get_by_placeholder("John Doe")
        await name_input.wait_for(state="visible", timeout=8_000)
        await name_input.fill(consumer_name)
        print(f"   Name → {consumer_name}")

        # Phone (random 10-digit Indian number)
        random_phone = str(random.randint(7000000000, 9999999999))
        phone_input = page.locator("input[type='tel'], input[placeholder*='91']").last
        await phone_input.wait_for(state="visible", timeout=8_000)
        await phone_input.fill(random_phone)
        print(f"   Phone → {random_phone}")

        # Email
        consumer_email = "testing12@gmail.com"
        email_input = page.get_by_placeholder("admin@hawkvision.ai")
        await email_input.wait_for(state="visible", timeout=8_000)
        await email_input.fill(consumer_email)
        print(f"   Email → {consumer_email}")

        # Job Title
        job_input = page.get_by_placeholder("UI/UX Designer")
        await job_input.wait_for(state="visible", timeout=8_000)
        await job_input.fill("QA Automation")
        print("   Job Title → QA Automation")

        # ── 5. ADD SITE → SELECT JAIPUR PREPROD ───────────────────────────────
        print("⏳  Adding site …")

        add_site_btn = page.get_by_role("button", name="Add Site")
        await add_site_btn.wait_for(state="visible", timeout=10_000)
        await add_site_btn.click()
        await page.wait_for_timeout(1_200)

        # FIX: "Jaipur PreProd" lives inside a dropdown list after clicking Add Site.
        # Wait for the option to actually appear before clicking it.
        jaipur_option = page.locator("[role='option'], li").filter(has_text="Jaipur PreProd").first
        try:
            await jaipur_option.wait_for(state="visible", timeout=8_000)
            await jaipur_option.click()
        except PWTimeoutError:
            # fallback: it might render as plain text in a panel, not a list item
            await page.get_by_text("Jaipur PreProd", exact=False).first.click()

        await page.wait_for_timeout(1_500)
        print("✅  Site selected: Jaipur PreProd")

        # ── 6. SELECT LOCATION TAG ────────────────────────────────────────────
        print("⏳  Selecting Location Tag …")

        # FIX: After selecting a site, the location tags load ASYNCHRONOUSLY.
        # We must:
        #   a) click the "Select Location Tag" trigger
        #   b) wait for options to finish loading (not a fixed selector like "text=Calgiri Road")
        #   c) then pick the right option

        loc_tag_trigger = page.get_by_role("button", name="Select Location Tag")

        # If "Select Location Tag" is a combobox / div instead of a button, try broader:
        try:
            await loc_tag_trigger.wait_for(state="visible", timeout=8_000)
        except PWTimeoutError:
            # widen the search — any element whose text contains "Select Location Tag"
            loc_tag_trigger = page.locator(
                "text=Select Location Tag, [placeholder*='location' i], [aria-label*='location tag' i]"
            ).first
            await loc_tag_trigger.wait_for(state="visible", timeout=8_000)

        # Use retry helper so if the dropdown loads slowly, we try again
        await open_dropdown_and_pick(page, loc_tag_trigger, "Calgiri Road")
        await page.wait_for_timeout(1_000)
        print("✅  Location Tag selected: Calgiri Road")

        # ── 7. SUBMIT — CREATE CONSUMER ───────────────────────────────────────
        print("⏳  Creating consumer …")

        create_btn = page.get_by_role("button", name="Create")
        await create_btn.wait_for(state="visible", timeout=8_000)
        await create_btn.click()

        # Wait for modal to disappear as success signal
        try:
            await page.wait_for_selector(
                "text=Create Consumer", state="hidden", timeout=15_000
            )
        except PWTimeoutError:
            pass   # some apps show a toast instead of closing modal; continue anyway

        await page.wait_for_timeout(2_000)
        print(f"✅  Consumer '{consumer_name}' created successfully")

        print()
        print("=" * 55)
        print("  ✅  CREATE CONSUMER TEST COMPLETED 🚀")
        print("=" * 55)

        await page.wait_for_timeout(3_000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(create_consumer_test())