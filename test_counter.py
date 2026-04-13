import asyncio
from playwright.async_api import async_playwright

EMAIL = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"


async def create_counter_test():

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
        # 2️⃣ NAVIGATE TO SITES PAGE
        # =====================================================
        await page.goto(
            "https://preprod.hawkvision.ai/configure",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(3000)
        print("Sites Page Opened ✅")

        # =====================================================
        # 3️⃣ OPEN QUALITY ASSURANCE SITE
        # =====================================================
        await page.locator("text=Jaipur PreProd Site").click()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        print("Jaipur PreProd  Site Opened ✅")

        # =====================================================
        # 4️⃣ CLICK COUNTER TAB
        # =====================================================
        await page.locator("text=Counter").click()
        await page.wait_for_timeout(2000)
        print("Counter Tab Opened ✅")

        # =====================================================
        # 5️⃣ CLICK + ADD COUNTERS BUTTON
        # =====================================================
        await page.locator("button:has-text('Add Counters')").click()
        await page.wait_for_selector("text=Create Counter")
        await page.wait_for_timeout(1500)
        print("Create Counter Modal Opened ✅")

        # =====================================================
        # 6️⃣ FILL COUNTER NAME
        # =====================================================
        await page.get_by_placeholder("Lift 1").fill("TestCounter")
        await page.wait_for_timeout(500)
        print("Counter Name filled: TestCounter ✅")

        # =====================================================
        # 7️⃣ SELECT TOTAL NUMBER OF PEOPLE
        # =====================================================
        await page.locator("label:has-text('Total number of People')").click()
        await page.wait_for_timeout(1000)
        print("Selected: Total number of People ✅")

        # =====================================================
        # 8️⃣ SELECT NO LIMIT
        # =====================================================
        await page.locator("label:has-text('No')").click()
        await page.wait_for_timeout(1000)
        print("Limit selected: No ✅")

        # =====================================================
        # 9️⃣ SELECT TIMEZONE - UTC
        # =====================================================
        print("Selecting Timezone: UTC...")

        # Click timezone dropdown to open it
        await page.locator("text=Asia/Kolkata (UTC +05:30)").click()
        await page.wait_for_timeout(1500)

        # Click UTC option - first item in the dropdown list
        await page.get_by_text("UTC", exact=True).click()
        await page.wait_for_timeout(1000)
        print("Timezone selected: UTC ✅")

        # =====================================================
        # 🔟 COUNTER CONFIGURATION
        # Reporting Schedule: 5 Minutes (Fixed - no action)
        # Reset Schedule: Daily + 12:00 AM (default - no action)
        # =====================================================
        print("Reporting Schedule: 5 Minutes (Fixed) ✅")
        print("Reset Schedule: Daily at 12:00 AM (default) ✅")

        # =====================================================
        # 1️⃣1️⃣ CLICK CREATE
        # =====================================================
        await page.get_by_role("button", name="Create").click()
        await page.wait_for_timeout(3000)
        print("Counter Created Successfully ✅")

        # Verify counter appears in list
        await page.wait_for_selector("text=TestCounter", timeout=7000)
        print("Counter 'TestCounter' visible in list ✅")

        print("=" * 50)
        print("✅ CREATE COUNTER TEST COMPLETED 🚀")
        print("=" * 50)

        await page.wait_for_timeout(3000)
        await browser.close()


# =====================================================
# RUN SCRIPT
# =====================================================
if __name__ == "__main__":
    asyncio.run(create_counter_test())