import asyncio
from playwright.async_api import async_playwright, TimeoutError
import pandas as pd

all_data = []


async def scrape_josaa():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to the page with a longer timeout
            await page.goto(
                "https://josaa.admissions.nic.in/applicant/SeatAllotmentResult/CurrentORCR.aspx",
                wait_until="networkidle",
                timeout=60000,
            )

            # Wait for the page to be fully loaded
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_load_state("networkidle")

            # Wait for the institute dropdown with state visible
            await page.wait_for_selector(
                "#ctl00_ContentPlaceHolder1_ddlInstitute",
                state="visible",
                timeout=60000,
            )

            # Get dropdown handles
            async def get_options(selector):
                await page.wait_for_selector(selector, state="visible", timeout=30000)
                return await page.eval_on_selector_all(
                    selector,
                    "els => els.map(e => ({value: e.value, label: e.textContent.trim()}))",
                )

            institutes = await get_options("#ctl00_ContentPlaceHolder1_ddlInstitute")
            quotas = await get_options("#ctl00_ContentPlaceHolder1_ddlQuota")
            seat_types = await get_options("#ctl00_ContentPlaceHolder1_ddlSeatType")
            genders = await get_options("#ctl00_ContentPlaceHolder1_ddlGender")

            for institute in institutes[1:]:  # Skip default option
                await page.select_option(
                    "#ctl00_ContentPlaceHolder1_ddlInstitute", institute["value"]
                )
                await page.wait_for_timeout(1000)  # Increased wait time

                programs = await get_options("#ctl00_ContentPlaceHolder1_ddlBranch")
                for program in programs[1:]:
                    await page.select_option(
                        "#ctl00_ContentPlaceHolder1_ddlBranch", program["value"]
                    )

                    for quota in quotas[1:]:
                        await page.select_option(
                            "#ctl00_ContentPlaceHolder1_ddlQuota", quota["value"]
                        )

                        for seat_type in seat_types[1:]:
                            await page.select_option(
                                "#ctl00_ContentPlaceHolder1_ddlSeatType",
                                seat_type["value"],
                            )

                            for gender in genders[1:]:
                                await page.select_option(
                                    "#ctl00_ContentPlaceHolder1_ddlGender",
                                    gender["value"],
                                )
                                await page.click("#ctl00_ContentPlaceHolder1_btnSubmit")
                                await page.wait_for_load_state("networkidle")
                                await page.wait_for_timeout(2000)  # Increased wait time

                                rows = await page.query_selector_all(
                                    "#ctl00_ContentPlaceHolder1_GridView1 > tbody > tr"
                                )
                                for row in rows[1:]:  # Skip header
                                    cols = await row.query_selector_all("td")
                                    text = [await col.inner_text() for col in cols]
                                    if text:
                                        all_data.append(
                                            {
                                                "Institute": institute["label"],
                                                "Program": program["label"],
                                                "Quota": quota["label"],
                                                "Seat Type": seat_type["label"],
                                                "Gender": gender["label"],
                                                "Round": text[0],
                                                "Opening Rank": text[1],
                                                "Closing Rank": text[2],
                                            }
                                        )

                                # Go back
                                await page.go_back()
                                await page.wait_for_load_state("networkidle")
                                await page.wait_for_selector(
                                    "#ctl00_ContentPlaceHolder1_ddlInstitute",
                                    state="visible",
                                )
                                await page.select_option(
                                    "#ctl00_ContentPlaceHolder1_ddlInstitute",
                                    institute["value"],
                                )
                                await page.select_option(
                                    "#ctl00_ContentPlaceHolder1_ddlBranch",
                                    program["value"],
                                )
                                await page.select_option(
                                    "#ctl00_ContentPlaceHolder1_ddlQuota",
                                    quota["value"],
                                )
                                await page.select_option(
                                    "#ctl00_ContentPlaceHolder1_ddlSeatType",
                                    seat_type["value"],
                                )

        except TimeoutError as e:
            print(f"Timeout error occurred: {e}")
            raise
        finally:
            await browser.close()


try:
    asyncio.run(scrape_josaa())
    # Save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv("josaa_opening_closing_ranks.csv", index=False)
    print("Data saved to josaa_opening_closing_ranks.csv")
except Exception as e:
    print(f"An error occurred: {e}")
