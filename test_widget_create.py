import asyncio
import time
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

EMAIL = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"
BASE_URL = "https://preprod.hawkvision.ai"


async def create_dashboard_with_widget():

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
        # 1. LOGIN
        # =====================================================
        await page.goto(
            f"{BASE_URL}/login",
            wait_until="domcontentloaded",
            timeout=120000
        )

        # Wait for both fields
        await page.wait_for_selector("input[placeholder='username@example.com']", timeout=30000)
        await page.wait_for_selector("input[type='password']", timeout=30000)
        await page.wait_for_timeout(1000)

        await page.fill("input[placeholder='username@example.com']", EMAIL)
        await page.wait_for_timeout(500)
        await page.fill("input[type='password']", PASSWORD)
        await page.wait_for_timeout(500)

        # FIX: Sign In button is NOT inside a form — click it directly
        sign_in_btn = page.get_by_role("button", name="Sign In")
        await sign_in_btn.wait_for(state="visible", timeout=10000)
        await sign_in_btn.click()

        await page.wait_for_url("**/home", timeout=60000)
        await page.wait_for_timeout(3000)
        print("Login Successful ✅")

        # =====================================================
        # 2. OPEN DASHBOARD PAGE
        # =====================================================
        await page.goto(
            f"{BASE_URL}/manage-dashboards",
            wait_until="domcontentloaded",
            timeout=60000
        )
        await page.wait_for_selector("button", timeout=15000)
        await page.wait_for_timeout(2000)
        print("Dashboard Page Opened ✅")

        # =====================================================
        # 3. CREATE DASHBOARD
        # =====================================================
        create_btn = page.get_by_role("button", name="Create").first
        await create_btn.wait_for(state="visible", timeout=10000)
        await create_btn.click()
        await page.wait_for_selector("text=Create New Dashboard", timeout=10000)
        await page.wait_for_timeout(800)

        dashboard_name = "Automation Dashboard Widget Creation Testing"

        title_input = page.locator("input[placeholder='e.g., Security Overview Dashboard']")
        await title_input.wait_for(state="visible", timeout=8000)
        await title_input.fill(dashboard_name)

        desc_input = page.locator("textarea[placeholder='Brief description of this dashboard...']")
        await desc_input.wait_for(state="visible", timeout=8000)
        await desc_input.fill("Dashboard created for advanced widget automation testing")
        await page.wait_for_timeout(500)

        create_dash_btn = page.get_by_role("button", name="Create Dashboard")
        await create_dash_btn.wait_for(state="visible", timeout=8000)
        await create_dash_btn.click()

        await page.wait_for_selector("text=Create New Dashboard", state="hidden", timeout=15000)
        await page.wait_for_timeout(2000)
        print("Dashboard Created ✅")

        # =====================================================
        # 4. OPEN NEW DASHBOARD
        # =====================================================
        dash_link = page.get_by_text(dashboard_name).first
        await dash_link.wait_for(state="visible", timeout=10000)
        await dash_link.click()
        await page.wait_for_timeout(3000)
        print("Dashboard Opened ✅")

        # =====================================================
        # 5. OPEN CREATE WIDGET MODAL
        # =====================================================
        print("Opening Create Widget modal...")

        create_widget_btn = page.locator("button").filter(has_text="Create Widget").first
        await create_widget_btn.wait_for(state="visible", timeout=10000)
        await create_widget_btn.click()
        await page.wait_for_selector("text=Create New Widget", timeout=10000)
        await page.wait_for_timeout(800)
        print("Widget Modal Opened ✅")

        # =====================================================
        # 6. FILL WIDGET DETAILS
        # =====================================================
        widget_name = f"Automation_Widget_{int(time.time())}"

        widget_name_input = page.locator("input[placeholder*='Incident Summary']")
        await widget_name_input.wait_for(state="visible", timeout=8000)
        await widget_name_input.fill(widget_name)
        print(f"Widget Name filled: {widget_name} ✅")

        widget_type_sel = page.locator("select").nth(0)
        await widget_type_sel.wait_for(state="visible", timeout=8000)
        await widget_type_sel.select_option(label="Incident")
        await page.wait_for_timeout(1000)
        print("Widget Type selected: Incident ✅")

        display_sel = page.locator("select").nth(1)
        await display_sel.wait_for(state="visible", timeout=8000)
        await page.wait_for_function(
            "() => document.querySelectorAll('select')[1].options.length > 1",
            timeout=8000
        )
        await display_sel.select_option(label="Summary")
        await page.wait_for_timeout(1000)
        print("Display Type selected: Summary ✅")

        graph_sel = page.locator("select").nth(2)
        await graph_sel.wait_for(state="visible", timeout=8000)
        await page.wait_for_function(
            "() => document.querySelectorAll('select')[2].options.length > 1",
            timeout=8000
        )
        await graph_sel.select_option(label="Stacked Bar")
        await page.wait_for_timeout(1000)
        print("Graph Type selected: Stacked Bar ✅")

        group_sel = page.locator("select").nth(3)
        await group_sel.wait_for(state="visible", timeout=8000)
        await page.wait_for_function(
            "() => document.querySelectorAll('select')[3].options.length > 1",
            timeout=8000
        )
        await group_sel.select_option(label="Usecases")
        await page.wait_for_timeout(1000)
        print("Group By selected: Usecases ✅")

        time_range_btn = page.locator("button").filter(has_text="Last 30 Days").first
        await time_range_btn.wait_for(state="visible", timeout=8000)
        await time_range_btn.click()
        await page.wait_for_timeout(800)
        print("Time Range selected: Last 30 Days ✅")

        # =====================================================
        # 7. CREATE WIDGET
        # =====================================================
        await page.wait_for_timeout(500)

        final_create_btn = page.locator("button").filter(has_text="Create Widget").last
        await final_create_btn.wait_for(state="visible", timeout=8000)
        await final_create_btn.click()
        await page.wait_for_timeout(4000)
        print("Widget Created Successfully ✅")

        print("=" * 50)
        print("✅ DASHBOARD + WIDGET FLOW COMPLETED 🚀")
        print("=" * 50)

        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(create_dashboard_with_widget())