import asyncio
import time
from playwright.async_api import async_playwright, Page, TimeoutError as PWTimeoutError

EMAIL    = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"
BASE_URL = "https://preprod.hawkvision.ai"


# ─────────────────────────────────────────────────────────────────────────────
# Helper: navigate without relying on "networkidle"
# ─────────────────────────────────────────────────────────────────────────────
async def goto(page: Page, url: str, wait_selector: str = None, pause: int = 2000):
    """
    Navigate to a URL.
    • Uses 'domcontentloaded' (never times-out on busy SPA backgrounds).
    • Optionally waits for a specific element to confirm the page is ready.
    • Always waits `pause` ms extra so React/Vue can finish rendering.
    """
    await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    if wait_selector:
        await page.wait_for_selector(wait_selector, timeout=20_000)
    await page.wait_for_timeout(pause)


async def select_dropdown_option(page: Page, text: str, timeout: int = 10_000):
    """Click a visible dropdown option by text (role=option → li fallback)."""
    opt = page.locator("[role='option']").filter(has_text=text)
    try:
        await opt.first.wait_for(state="visible", timeout=timeout)
        await opt.first.click()
        return
    except PWTimeoutError:
        pass
    fallback = page.locator("li").filter(has_text=text)
    await fallback.first.wait_for(state="visible", timeout=timeout)
    await fallback.first.click()


# ─────────────────────────────────────────────────────────────────────────────
# Main test
# ─────────────────────────────────────────────────────────────────────────────
async def full_website_test():

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

        # ══════════════════════════════════════════════════════════════════════
        # 1. LOGIN
        # ══════════════════════════════════════════════════════════════════════
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

        # ══════════════════════════════════════════════════════════════════════
        # 2. CONFIGURE PAGE → LOCATION TAG
        # ══════════════════════════════════════════════════════════════════════
        # FIX: use domcontentloaded + wait for a known element instead of networkidle
        await goto(
            page,
            f"{BASE_URL}/configure",
            wait_selector="text=Jaipur PreProd",   # wait until site card appears
            pause=2_000
        )
        print("✅  Configure / Sites page opened")

        # Open Jaipur PreProd site
        await page.get_by_text("Jaipur PreProd", exact=False).first.click()
        await page.wait_for_timeout(2_000)
        print("✅  Jaipur PreProd Site opened")

        # Click Location Tags tab
        await page.get_by_role("button", name="Location Tags").click()
        await page.wait_for_timeout(1_500)

        # Click top Create button
        await page.get_by_role("button", name="Create").first.click()
        await page.wait_for_selector("text=Create Location Tag", timeout=10_000)
        await page.wait_for_timeout(800)

        # Unique tag name
        tag_name = f"Testing_Location_{int(time.time())}"
        await page.get_by_placeholder("Enter Here").fill(tag_name)
        await page.wait_for_timeout(500)

        # Click Create inside modal
        await page.get_by_role("button", name="Create").last.click()
        await page.wait_for_selector(f"text={tag_name}", timeout=15_000)
        print(f"✅  Location Tag '{tag_name}' created")

        await page.wait_for_timeout(2_000)

        # ══════════════════════════════════════════════════════════════════════
        # 3. INCIDENT PAGE — open 5th row
        # ══════════════════════════════════════════════════════════════════════
        await goto(
            page,
            f"{BASE_URL}/report",
            wait_selector="table tbody tr",   # wait until table rows exist
            pause=2_000
        )
        print("✅  Incident / Report page opened")

        rows = page.locator("table tbody tr")
        count = await rows.count()
        print(f"   Incidents visible: {count}")

        if count >= 5:
            print("   Opening 5th incident …")
            await rows.nth(4).click()
            await page.wait_for_timeout(4_000)
            print("   Closing incident preview …")
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(2_000)
        else:
            print("   ⚠️  Less than 5 incidents available — skipping.")

        # ══════════════════════════════════════════════════════════════════════
        # 4. ANALYTICS PAGE — filter to Last 30 Days
        # ══════════════════════════════════════════════════════════════════════
        await goto(
            page,
            f"{BASE_URL}/analysis",
            wait_selector="button",           # any button = page shell loaded
            pause=2_000
        )
        print("✅  Analytics page opened")

        # Hover then click the "Days" time-filter button
        days_btn = page.locator("button").filter(has_text="Days").first
        await days_btn.wait_for(state="visible", timeout=10_000)
        await days_btn.hover()
        await page.wait_for_timeout(600)
        await days_btn.click()
        await page.wait_for_timeout(1_500)

        # Select "Last 30 Days" from the dropdown
        last30 = page.get_by_text("Last 30 Days", exact=True).first
        await last30.wait_for(state="visible", timeout=10_000)
        await last30.hover()
        await page.wait_for_timeout(400)
        await last30.click()
        await page.wait_for_timeout(2_500)
        print("✅  Analytics filtered to Last 30 Days")

        # ══════════════════════════════════════════════════════════════════════
        # 5. DASHBOARD PAGE — create new dashboard
        # ══════════════════════════════════════════════════════════════════════
        await goto(
            page,
            f"{BASE_URL}/manage-dashboards",
            wait_selector="button",
            pause=2_000
        )
        print("✅  Dashboard page opened")

        # Click top Create button
        create_btn = page.get_by_role("button", name="Create").first
        await create_btn.wait_for(state="visible", timeout=10_000)
        await create_btn.click()
        await page.wait_for_selector("text=Create New Dashboard", timeout=10_000)
        await page.wait_for_timeout(800)

        # Fill Title
        title_input = page.locator("input[placeholder='e.g., Security Overview Dashboard']")
        await title_input.wait_for(state="visible", timeout=8_000)
        await title_input.fill("Automation Dashboard Test")

        # Fill Description
        desc_input = page.locator("textarea[placeholder='Brief description of this dashboard...']")
        await desc_input.wait_for(state="visible", timeout=8_000)
        await desc_input.fill("Dashboard created automatically using Playwright automation test")

        await page.wait_for_timeout(800)

        # Click Create Dashboard (inside the form/modal)
        create_dash_btn = page.locator("form").get_by_role("button", name="Create Dashboard")
        await create_dash_btn.wait_for(state="visible", timeout=8_000)
        await create_dash_btn.click()

        # Wait for modal to close as confirmation
        await page.wait_for_selector(
            "text=Create New Dashboard", state="hidden", timeout=15_000
        )
        await page.wait_for_timeout(2_000)
        print("✅  Dashboard 'Automation Dashboard Test' created")

        # ══════════════════════════════════════════════════════════════════════
        # 6. RETURN HOME
        # ══════════════════════════════════════════════════════════════════════
        await goto(page, f"{BASE_URL}/home", wait_selector="body", pause=3_000)
        print("✅  Returned to Home")

        print()
        print("=" * 55)
        print("  ✅  FULL WEBSITE FLOW COMPLETED SUCCESSFULLY 🚀")
        print("=" * 55)

        await page.wait_for_timeout(4_000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(full_website_test())