import asyncio
import time
from playwright.async_api import async_playwright

EMAIL = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"


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

        # =====================================================
        # 1️⃣ LOGIN
        # =====================================================
        await page.goto(
            "https://preprod.hawkvision.ai/login",
            wait_until="domcontentloaded"
        )

        await page.fill("input[placeholder='username@example.com']", EMAIL)
        await page.fill("input[type='password']", PASSWORD)
        await page.locator("form").get_by_role("button", name="Sign In").click()

        await page.wait_for_url("**/home")
        print("Login Successful ✅")

        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)

        # =====================================================
        # 2️⃣ NAVIGATE TO INCIDENTS PAGE
        # =====================================================
        await page.goto(
            "https://preprod.hawkvision.ai/report",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(3000)
        print("Incidents Page Opened ✅")

        # =====================================================
        # 3️⃣ WAIT FOR TABLE TO LOAD
        # =====================================================
        print("Waiting for table to load...")

        await page.wait_for_selector(
            "table tbody tr",
            state="visible",
            timeout=15000
        )

        row_count = await page.locator("table tbody tr").count()
        print(f"Total rows found: {row_count}")

        if row_count == 0:
            print("No incidents found ❌")
            await browser.close()
            return

        print("Table Loaded ✅")
        # =====================================================
        # 6️⃣ APPLY SITE FILTER
        # =====================================================
        print("Applying Site filter...")

        await page.locator("th:has-text('Site')").click()
        await page.wait_for_timeout(1500)

        await page.wait_for_selector("text=Jaipur Preprod", timeout=7000)
        print("Selecting Jaipur PreProd...")
        await page.locator("text=Jaipur PreProd").first.click()
        await page.wait_for_timeout(1000)

        # Click Apply button inside the filter dropdown
        try:
            apply_btn = page.locator("button:has-text('Apply')").last
            await apply_btn.click()
            print("Apply button clicked for Camera filter ✅")
            await page.wait_for_timeout(2000)
        except:
            print("No Apply button found, continuing...")

        # Close dropdown by pressing Escape
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1500)

        # Wait for thead dropdown to fully close
        try:
            await page.wait_for_selector(
                "label:has-text('To')",
                state="hidden",
                timeout=5000
            )
        except:
            pass

        # Click outside to ensure dropdown is closed
        await page.locator("body").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(2000)

        print("Camera Filter Applied ✅")

        # =====================================================
        # 7️⃣ APPLY TIME CREATED FILTER
        # =====================================================
        print("Applying Time Created filter...")

        # Make sure table is stable
        await page.wait_for_selector(
            "table tbody tr",
            state="visible",
            timeout=10000
        )
        await page.wait_for_timeout(1500)

        await page.locator("th:has-text('Time Created')").click()
        await page.wait_for_timeout(1500)

        await page.wait_for_selector("text=Last 30 Days", timeout=7000)
        print("Selecting Last 30 Days...")
        await page.locator("text=Last 30 Days").first.click()
        await page.wait_for_timeout(1000)

        # Click Apply button inside the filter dropdown
        try:
            apply_btn = page.locator("button:has-text('Apply')").last
            await apply_btn.click()
            print("Apply button clicked for Time Created filter ✅")
            await page.wait_for_timeout(2000)
        except:
            print("No Apply button found, continuing...")

        # Close dropdown by pressing Escape
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1500)

        # Click outside to ensure dropdown is fully closed
        await page.locator("body").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(2000)

        print("Time Created Filter Applied ✅")

        # =====================================================
        # 8️⃣ OPEN 5TH INCIDENT AFTER FILTERS APPLIED
        # =====================================================
        print("Opening 5th Incident after filters...")

        # Wait for table to reload with filtered data
        await page.wait_for_selector(
            "table tbody tr",
            state="visible",
            timeout=10000
        )
        await page.wait_for_timeout(2000)

        # Make sure no dropdown/overlay is blocking
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)
        await page.locator("body").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(1000)

        row_count = await page.locator("table tbody tr").count()
        print(f"Total rows after filters: {row_count}")

        if row_count == 0:
            print("No rows found after filters ❌")
            await browser.close()
            return
        elif row_count < 5:
            print(f"Only {row_count} rows found, opening last row...")
            await page.locator("table tbody tr").nth(row_count - 1).click()
        else:
            print("Opening 5th row...")
            # Use JavaScript click to bypass any overlay blocking
            await page.locator("table tbody tr").nth(4).click(force=True)

        await page.wait_for_timeout(3000)
        print("5th Incident Opened ✅")

        print("Full Test Completed 🚀")

        await page.wait_for_timeout(3000)
        await browser.close()


# =====================================================
# RUN SCRIPT
# =====================================================
if __name__ == "__main__":
    asyncio.run(full_website_test())