import asyncio
import time
import random
from playwright.async_api import async_playwright

EMAIL = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"


async def master_automation_test():

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
            "https://hawk2.5.0.hawkvision.ai/login",
            wait_until="domcontentloaded",
            timeout=120000
        )

        await page.wait_for_selector("input[placeholder='username@example.com']")
        await page.fill("input[placeholder='username@example.com']", EMAIL)
        await page.fill("input[type='password']", PASSWORD)
        await page.locator("form").get_by_role("button", name="Sign In").click()

        await page.wait_for_url("**/home", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)
        print("Login Successful ✅")

        # =====================================================
        # 2️⃣ HOME PAGE
        # =====================================================
        print("On Home Page...")
        await page.wait_for_timeout(3000)
        print("Home Page Loaded ✅")

        # =====================================================
        # 3️⃣ SITES PAGE - CREATE LOCATION TAG
        # =====================================================
        """print("Opening Sites page...")

        await page.goto(
            "https://hawk2.5.0.hawkvision.ai/configure",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(3000)
        print("Sites Page Opened ✅")

        # Open Quality Assurance site
        await page.locator("text=Quality Assurance").click()
        await page.wait_for_timeout(2000)

        # Click Location Tags tab
        await page.get_by_role("button", name="Location Tags").click()
        await page.wait_for_timeout(2000)

        # Click Create button
        await page.get_by_role("button", name="Create").first.click()
        await page.wait_for_selector("text=Create Location Tag")

        # Unique tag name (alphabets only with timestamp)
        tag_name = f"TestingLocation{int(time.time())}"
        await page.get_by_placeholder("Enter Here").fill(tag_name)

        # Click Create inside modal
        await page.get_by_role("button", name="Create").last.click()
        await page.wait_for_selector(f"text={tag_name}")
        await page.wait_for_timeout(3000)
        print(f"Location Tag '{tag_name}' Created ✅") """

        # =====================================================
        # 4️⃣ INCIDENTS PAGE - APPLY FILTERS + OPEN 5TH INCIDENT
        # =====================================================
        print("Opening Incidents page...")

        await page.goto(
            "https://hawk2.5.0.hawkvision.ai/report",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(3000)

        # Wait for table
        await page.wait_for_selector(
            "table tbody tr",
            state="visible",
            timeout=15000
        )
        row_count = await page.locator("table tbody tr").count()
        print(f"Total rows found: {row_count}")
        print("Incidents Page Loaded ✅")

        # ---- APPLY SITE FILTER ----
        print("Applying Site filter...")

        await page.locator("th:has-text('Site')").click()
        await page.wait_for_timeout(1500)

        await page.wait_for_selector("text=Quality Assurance", timeout=7000)
        await page.locator("text=Quality Assurance").first.click()
        await page.wait_for_timeout(1000)

        try:
            await page.locator("button:has-text('Apply')").last.click()
            print("Apply clicked for Site filter ✅")
            await page.wait_for_timeout(2000)
        except:
            pass

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1500)
        await page.locator("body").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(2000)
        print("Site Filter Applied ✅")

        # ---- APPLY USE CASE FILTER ----
        print("Applying Use Case filter...")

        await page.wait_for_selector(
            "table tbody tr",
            state="visible",
            timeout=10000
        )
        await page.wait_for_timeout(1500)

        await page.locator("th:has-text('Use Case')").click()
        await page.wait_for_timeout(1500)

        # Wait for dropdown to open
        await page.wait_for_selector("text=Near_Miss", timeout=7000)

        # Click Near_Miss INSIDE the dropdown only (not in table rows)
        await page.locator("li:has-text('Near_Miss'), label:has-text('Near_Miss'), div[role='option']:has-text('Near_Miss')").first.click()
        await page.wait_for_timeout(1000)

        # Click Apply
        await page.locator("button:has-text('Apply')").last.click()
        print("Apply clicked for Use Case filter ✅")
        await page.wait_for_timeout(2000)

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1500)
        await page.locator("body").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(2000)
        print("Use Case Filter Applied: Near_Miss ✅")

        # ---- APPLY TIME CREATED FILTER ----
        print("Applying Time Created filter...")

        await page.wait_for_selector(
            "table tbody tr",
            state="visible",
            timeout=10000
        )
        await page.wait_for_timeout(1500)

        await page.locator("th:has-text('Time Created')").click()
        await page.wait_for_timeout(1500)

        await page.wait_for_selector("text=Last 30 Days", timeout=7000)
        await page.locator("text=Last 30 Days").first.click()
        await page.wait_for_timeout(1000)

        try:
            await page.locator("button:has-text('Apply')").last.click()
            print("Apply clicked for Time Created filter ✅")
            await page.wait_for_timeout(2000)
        except:
            pass

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1500)
        await page.locator("body").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(2000)
        print("Time Created Filter Applied ✅")

        # ---- OPEN 5TH INCIDENT ----
        print("Opening 5th Incident after filters...")

        await page.wait_for_selector(
            "table tbody tr",
            state="visible",
            timeout=10000
        )
        await page.wait_for_timeout(2000)

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)
        await page.locator("body").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(1000)

        row_count = await page.locator("table tbody tr").count()
        print(f"Total rows after filters: {row_count}")

        if row_count == 0:
            print("No rows found after filters ❌")
        elif row_count < 5:
            print(f"Only {row_count} rows, opening last row...")
            await page.locator("table tbody tr").nth(row_count - 1).click(force=True)
        else:
            print("Opening 5th row...")
            await page.locator("table tbody tr").nth(4).click(force=True)

        await page.wait_for_timeout(3000)
        print("5th Incident Opened ✅")

        # Close incident preview
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(2000)

        # =====================================================
        # 5️⃣ ANALYTICS PAGE - APPLY 30 DAYS FILTER
        # =====================================================
        """ print("Opening Analytics page...")

        await page.goto(
            "https://hawk2.5.0.hawkvision.ai/analysis",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(3000)
        print("Analytics Page Opened ✅")

        await page.locator("button", has_text="Days").first.click()
        await page.wait_for_timeout(2000)

        await page.get_by_text("Last 30 Days", exact=True).first.click()
        await page.wait_for_timeout(3000)
        print("Analytics filtered to Last 30 Days ✅")

        # =====================================================
        # 6️⃣ DASHBOARDS PAGE - CREATE DASHBOARD + WIDGET
        # =====================================================
        print("Opening Dashboards page...")

        await page.goto(
            "https://hawk2.5.0.hawkvision.ai/manage-dashboards",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(3000)
        print("Dashboards Page Opened ✅")

        # Create Dashboard
        await page.get_by_role("button", name="Create").first.click()
        await page.wait_for_selector("text=Create New Dashboard")

        dashboard_name = "Automation Dashboard Widget Creation Testing"
        await page.locator(
            "input[placeholder='e.g., Security Overview Dashboard']"
        ).fill(dashboard_name)

        await page.locator(
            "textarea[placeholder='Brief description of this dashboard...']"
        ).fill("Dashboard created for advanced widget automation testing")

        await page.wait_for_timeout(1000)
        await page.locator("form").get_by_role("button", name="Create Dashboard").click()
        await page.wait_for_timeout(4000)
        print("Dashboard Created ✅")

        # Open the new dashboard
        await page.get_by_text(dashboard_name).click()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        print("Dashboard Opened ✅")

        # Open Create Widget modal
        await page.wait_for_selector("button:has-text('Create Widget')")
        await page.locator("button:has-text('Create Widget')").first.click()
        await page.wait_for_selector("text=Create New Widget")
        print("Widget Modal Opened ✅")

        # Fill widget details
        widget_name = f"AutomationWidget{int(time.time())}"
        await page.locator("input[placeholder*='Incident Summary']").fill(widget_name)
        print(f"Widget Name: {widget_name}")

        # Widget Type
        await page.locator("select").nth(0).select_option(label="Incident")
        print("Widget Type: Incident ✅")

        # Display Type
        await page.wait_for_timeout(1000)
        await page.wait_for_function(
            "() => document.querySelectorAll('select')[1].options.length > 1"
        )
        await page.locator("select").nth(1).select_option(label="Summary")
        print("Display Type: Summary ✅")

        # Graph Type
        await page.wait_for_timeout(1000)
        await page.wait_for_function(
            "() => document.querySelectorAll('select')[2].options.length > 1"
        )
        await page.locator("select").nth(2).select_option(label="Stacked Bar")
        print("Graph Type: Stacked Bar ✅")

        # Group By
        await page.wait_for_timeout(1000)
        await page.wait_for_function(
            "() => document.querySelectorAll('select')[3].options.length > 1"
        )
        await page.locator("select").nth(3).select_option(label="Usecases")
        print("Group By: Usecases ✅")

        # Time Range
        await page.locator("button:has-text('Last 30 Days')").click()
        print("Time Range: Last 30 Days ✅")

        await page.wait_for_timeout(1000)

        # Create Widget
        await page.locator("button:has-text('Create Widget')").last.click()
        await page.wait_for_timeout(5000)
        print("Widget Created Successfully ✅")

        # =====================================================
        # 7️⃣ USERS PAGE - CREATE CONSUMER
        # =====================================================
        print("Opening Users page...")

        await page.goto(
            "https://hawk2.5.0.hawkvision.ai/manage-consumer",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(3000)
        print("Users Page Opened ✅")

        # Click + Add Consumer
        await page.get_by_role("button", name="+ Add Consumer").click()
        await page.wait_for_selector("text=Create Consumer")
        await page.wait_for_timeout(1000)
        print("Create Consumer Modal Opened ✅")

        # ---- Name (alphabets only) ----
        consumer_name = "TestingConsumerCreation"
        await page.get_by_placeholder("John Doe").fill(consumer_name)
        print(f"Name filled: {consumer_name}")

        # ---- Phone Number (random) ----
        random_phone = str(random.randint(7000000000, 9999999999))
        await page.locator("input[type='tel'], input[placeholder*='91']").last.fill(random_phone)
        print(f"Phone filled: {random_phone}")

        # ---- Email ID ----
        consumer_email = "testing12@gmail.com"
        await page.get_by_placeholder("admin@hawkvision.ai").fill(consumer_email)
        print(f"Email filled: {consumer_email}")

        # ---- Job Title ----
        await page.get_by_placeholder("UI/UX Designer").fill("QA Automation")
        print("Job Title filled: QA Automation")

        # ---- Add Site - Quality Assurance ----
        print("Adding Site...")
        await page.get_by_role("button", name="Add Site").click()
        await page.wait_for_timeout(1500)

        await page.wait_for_selector("text=Quality Assurance", timeout=7000)
        await page.locator("text=Quality Assurance").click()
        await page.wait_for_timeout(1500)
        print("Site Selected: Quality Assurance ✅")

        # ---- Select Location Tag - Calgiri Road ----
        print("Selecting Location Tag...")
        await page.get_by_role("button", name="Select Location Tag").click()
        await page.wait_for_timeout(1500)

        await page.wait_for_selector("text=Calgiri Road", timeout=7000)
        await page.locator("text=Calgiri Road").click()
        await page.wait_for_timeout(1500)
        print("Location Tag Selected: Calgiri Road ✅")

        # ---- Create Consumer ----
        await page.get_by_role("button", name="Create").click()
        await page.wait_for_timeout(3000)
        print("Consumer Created Successfully ✅")

        await page.wait_for_timeout(2000)

        # =====================================================
        # 8️⃣ SUPPORT PAGE - CREATE TICKET
        # =====================================================
        print("Opening Support page...")

        await page.goto(
            "https://hawk2.5.0.hawkvision.ai/support",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(2000)
        print("Support Page Opened ✅")

        # Click Create Ticket
        await page.get_by_role("button", name="Create Ticket").click()
        await page.wait_for_selector("text=Subject")
        print("Create Ticket Modal Opened ✅")

        # Fill Subject
        await page.fill(
            "input[placeholder='Brief description of your issue']",
            "Automation Test Ticket Creation"
        )

        # Select Category
        await page.locator("text=Select category").click()
        await page.wait_for_selector("text=Ask a Question")
        await page.locator("text=Ask a Question").last.click(force=True)
        await page.wait_for_timeout(1000)

        # Select Priority
        await page.locator("text=Select priority").click()
        await page.wait_for_selector("text=Medium")
        await page.locator("text=Medium").last.click(force=True)
        await page.wait_for_timeout(1000)

        # Fill Description
        await page.fill(
            "textarea[placeholder='Detailed description of your issue or request']",
            "This ticket is being created through automated Playwright testing to validate the complete support workflow including category selection, priority selection, site selection and final ticket submission successfully."
        )

        # Submit ticket
        await page.get_by_role("button", name="Create", exact=True).click()
        await page.wait_for_timeout(3000)
        print("Ticket Created Successfully ✅") """

        # =====================================================
        # 9️⃣ RETURN TO HOME
        # =====================================================
        print("Returning to Home page...")

        await page.goto(
            "https://hawk2.5.0.hawkvision.ai/home",
            wait_until="networkidle"
        )
        await page.wait_for_timeout(5000)
        print("Home Page ✅")

        print("=" * 50)
        print("✅ FULL MASTER AUTOMATION TEST COMPLETED 🚀")
        print("=" * 50)

        await browser.close()


# =====================================================
# RUN SCRIPT
# =====================================================
if __name__ == "__main__":
    asyncio.run(master_automation_test())