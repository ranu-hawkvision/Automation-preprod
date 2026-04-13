import asyncio
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

EMAIL = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"
BASE_URL = "https://preprod.hawkvision.ai"


async def login(page):
    """Reusable login — use this in ALL your scripts."""
    await page.goto(
        f"{BASE_URL}/login",
        wait_until="domcontentloaded",
        timeout=120000
    )
    await page.wait_for_selector(
        "input[placeholder='username@example.com']", timeout=30000
    )
    await page.wait_for_timeout(1000)
    await page.fill("input[placeholder='username@example.com']", EMAIL)
    await page.wait_for_timeout(500)

    # Password field — confirmed selector
    await page.wait_for_selector(
        "input[autocomplete='current-password']", timeout=10000
    )
    await page.fill("input[autocomplete='current-password']", PASSWORD)
    await page.wait_for_timeout(500)

    # Click the SUBMIT Sign In button (not the tab toggle one)
    sign_in_btn = page.locator("button[type='submit']").filter(has_text="Sign In")
    await sign_in_btn.wait_for(state="visible", timeout=10000)
    await sign_in_btn.click()

    await page.wait_for_url("**/home", timeout=60000)
    await page.wait_for_timeout(3000)
    print("Login Successful ✅")


async def run():

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

        # ===============================
        # 1. LOGIN
        # ===============================
        await login(page)
        await page.wait_for_timeout(3000)
        print("Stayed 3 seconds on Home ✅")

        # ===============================
        # 2. GO TO SUPPORT PAGE
        # ===============================
        await page.goto(
            f"{BASE_URL}/support",
            wait_until="domcontentloaded",
            timeout=60000
        )
        await page.wait_for_selector("button", timeout=15000)
        await page.wait_for_timeout(2000)
        print("Support page opened ✅")

        # ===============================
        # 3. OPEN CREATE TICKET MODAL
        # ===============================
        create_ticket_btn = page.get_by_role("button", name="Create Ticket")
        await create_ticket_btn.wait_for(state="visible", timeout=10000)
        await create_ticket_btn.click()
        await page.wait_for_selector("text=Subject", timeout=10000)
        await page.wait_for_timeout(800)
        print("Create Ticket modal opened ✅")

        # ===============================
        # 4. FILL TICKET DETAILS
        # ===============================

        # Subject
        subject_input = page.locator(
            "input[placeholder='Brief description of your issue']"
        )
        await subject_input.wait_for(state="visible", timeout=8000)
        await subject_input.fill("Automation Test Ticket Creation")
        print("Subject filled ✅")

        # Category
        category_trigger = page.get_by_text("Select category", exact=False).first
        await category_trigger.wait_for(state="visible", timeout=8000)
        await category_trigger.click()
        await page.wait_for_timeout(1000)
        try:
            bug_option = page.locator("[role='option']").filter(has_text="Bug").first
            await bug_option.wait_for(state="visible", timeout=5000)
            await bug_option.click()
        except PWTimeoutError:
            await page.locator("li").filter(has_text="Bug").first.click()
        await page.wait_for_timeout(500)
        print("Category selected: Bug ✅")

        # Priority
        priority_trigger = page.get_by_text("Select priority", exact=False).first
        await priority_trigger.wait_for(state="visible", timeout=8000)
        await priority_trigger.click()
        await page.wait_for_timeout(1000)
        try:
            low_option = page.locator("[role='option']").filter(has_text="Low").first
            await low_option.wait_for(state="visible", timeout=5000)
            await low_option.click()
        except PWTimeoutError:
            await page.locator("li").filter(has_text="Low").first.click()
        await page.wait_for_timeout(500)
        print("Priority selected: Low ✅")

        # Description
        desc_input = page.locator(
            "textarea[placeholder='Detailed description of your issue or request']"
        )
        await desc_input.wait_for(state="visible", timeout=8000)
        await desc_input.fill(
            "This ticket is being created through automated Playwright testing to validate "
            "the complete support workflow including category selection, priority selection, "
            "site selection and final ticket submission successfully."
        )
        print("Description filled ✅")

        # ===============================
        # 5. CREATE TICKET
        # ===============================
        create_btn = page.get_by_role("button", name="Create", exact=True)
        await create_btn.wait_for(state="visible", timeout=8000)
        await create_btn.click()
        await page.wait_for_timeout(3000)
        print("Ticket Created Successfully ✅")

        print("=" * 50)
        print("✅ SUPPORT TICKET TEST COMPLETED 🚀")
        print("=" * 50)

        await page.wait_for_timeout(5000)
        await browser.close()
        print("Browser Closed ✅")


if __name__ == "__main__":
    asyncio.run(run())