import asyncio
from playwright.async_api import async_playwright

EMAIL = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"


async def switch_environment_test():

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

        # =====================================================
        # 1️⃣ LOGIN
        # =====================================================
        await page.goto(
            "https://preprod.hawkvision.ai/login",
            wait_until="domcontentloaded",
            timeout=120000
        )

        await page.wait_for_selector("input[placeholder='username@example.com']")
        await page.fill("input[placeholder='username@example.com']", EMAIL)
        await page.fill("input[type='password']", PASSWORD)
        await page.locator("form").get_by_role("button", name="Sign In").click()

        await page.wait_for_url("**/home", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        print("Login Successful ✅")

        # =====================================================
        # 2️⃣ SWITCH TO VIRTUAL MODE
        # =====================================================
        print("Switching to Virtual Mode...")

        await page.locator("text=Ranu Khandelwal").click()
        await page.wait_for_timeout(1500)
        print("Profile Menu Opened ✅")

        await page.get_by_role("button", name="Virtual").click()
        await page.wait_for_timeout(1500)
        print("Virtual button clicked ✅")

        # Confirmation popup - Switch to Virtual
        await page.wait_for_selector("text=Switch to Virtual Environment", timeout=7000)
        await page.get_by_role("button", name="Switch to Virtual").click()
        await page.wait_for_timeout(3000)
        print("Switched to Virtual Mode ✅")

        # Verify virtual banner visible
        await page.wait_for_selector("text=VIRTUAL ENVIRONMENT", timeout=7000)
        print("Virtual Environment Banner Visible ✅")

        await page.wait_for_timeout(3000)

        # =====================================================
        # 3️⃣ SWITCH BACK TO REAL MODE
        # =====================================================
        print("Switching back to Real Mode...")

        # Click Turn Off in the top banner
        await page.get_by_text("Turn Off", exact=True).click()
        await page.wait_for_timeout(2000)
        print("Turn Off clicked ✅")

        # The popup is now open - click Switch to Real with force
        await page.wait_for_selector("text=Switch to Real Environment", timeout=7000)
        await page.wait_for_timeout(500)
        print("Switch to Real Environment popup visible ✅")

        await page.get_by_role("button", name="Switch to Real").click(force=True)
        await page.wait_for_timeout(3000)
        print("Switch to Real button clicked ✅")

        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)

        is_virtual = await page.locator("text=VIRTUAL ENVIRONMENT").is_visible()
        if not is_virtual:
            print("Back to Real Mode Successfully ✅")
        else:
            print("Still in Virtual Mode ❌")

        print("=" * 50)
        print("✅ SWITCH ENVIRONMENT TEST COMPLETED 🚀")
        print("=" * 50)

        await page.wait_for_timeout(3000)
        await browser.close()


# =====================================================
# RUN SCRIPT
# =====================================================
if __name__ == "__main__":
    asyncio.run(switch_environment_test())