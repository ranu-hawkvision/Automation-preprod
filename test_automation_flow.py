import asyncio
from playwright.async_api import async_playwright

EMAIL = "ranu.khandelwal@hawkvision.ai"
PASSWORD = "Ranu@123"
BASE_URL = "https://preprod.hawkvision.ai"


async def automation_flow():

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

        # ======================
        # LOGIN
        # ======================

        await page.goto(f"{BASE_URL}/login")

        await page.fill(
            "input[placeholder='username@example.com']",
            EMAIL
        )

        await page.fill(
            "input[type='password']",
            PASSWORD
        )

        await page.locator("form").get_by_role(
            "button",
            name="Sign In"
        ).click()

        await page.wait_for_url("**/home")

        print("Login ✅")

        await page.wait_for_timeout(3000)

        # ======================
        # CONFIGURE
        # ======================

        await page.goto(f"{BASE_URL}/configure")

        await page.wait_for_timeout(3000)

        # click pre project site

        site = page.locator("div").filter(
            has_text="Pre"
        )

        await site.first.click()

        await page.wait_for_timeout(3000)

        print("Site opened ✅")

        # ======================
        # AUTOMATION TAB
        # ======================

        await page.get_by_text("Automation").click()

        await page.wait_for_timeout(2000)

        # ======================
        # DEVICES TAB
        # ======================

        await page.get_by_text("Devices").click()

        await page.wait_for_timeout(2000)

        # ======================
        # ADD DEVICE
        # ======================

        await page.get_by_role(
            "button",
            name="Add Device"
        ).click()

        await page.wait_for_timeout(2000)

        # device name

        await page.locator("input").first.fill(
            "Test_Device"
        )

        # open capability dropdown

        dropdown = page.locator(
            "div.multi-select-dropdown-container"
        ).last

        await dropdown.click()

        await page.wait_for_timeout(1000)

        # select alarm

        await page.get_by_text("alarm").first.click()

        # select machine_power

        await page.get_by_text("machine_power").first.click()

        # close dropdown

        await dropdown.click()

        # create device

        await page.get_by_role(
            "button",
            name="Create"
        ).last.click()

        print("Device created ✅")

        await page.wait_for_timeout(5000)

        # ======================
        # RULES TAB
        # ======================

        await page.get_by_text("Rules").click()

        await page.wait_for_timeout(2000)

        # ======================
        # ADD RULE
        # ======================

        await page.get_by_role(
            "button",
            name="Add Rule"
        ).click()

        await page.wait_for_timeout(2000)

        # rule name

        await page.get_by_placeholder(
            "Material spill Hooter setup"
        ).fill("TestRule")

        # add capability

        await page.get_by_role(
            "button",
            name="Add capability"
        ).click()

        await page.wait_for_timeout(1000)

        # open capability dropdown

        dropdown = page.locator(
            "div.single-select-dropdown-container"
        ).last

        await dropdown.click()

        await page.wait_for_timeout(1000)

        # select alarm

        menu = page.locator("div.absolute").last

        await menu.locator("span").filter(
            has_text="alarm"
        ).first.click()

        print("Capability selected ✅")

        # create rule

        await page.get_by_role(
            "button",
            name="Create"
        ).last.click()

        print("Rule created ✅")

        await page.wait_for_timeout(5000)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(automation_flow())
    