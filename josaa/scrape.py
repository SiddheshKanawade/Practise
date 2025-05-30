import asyncio
from playwright.async_api import async_playwright, TimeoutError
import pandas as pd

all_data = []


async def scrape_josaa():
    print("Starting the scraping process...")
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            print("Navigating to JOSAA website...")
            await page.goto(
                "https://josaa.admissions.nic.in/applicant/SeatAllotmentResult/CurrentORCR.aspx",
                wait_until="networkidle",
                timeout=60000,
            )

            print("Waiting for page to load completely...")
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_load_state("networkidle")

            # Get dropdown handles
            async def get_options(selector):
                await page.wait_for_selector(selector, state="visible", timeout=30000)
                return await page.eval_on_selector_all(
                    selector,
                    "els => els.map(e => ({value: e.value, label: e.textContent.trim()}))",
                )

            # Click on the round dropdown
            await page.click(
                "#ctl00_ContentPlaceHolder1_ddlroundno_chosen", timeout=10000
            )

            # Get rounds options
            rounds = await page.query_selector_all(
                "#ctl00_ContentPlaceHolder1_ddlroundno_chosen .chosen-drop .chosen-results .active-result"
            )
            print(f"Found {len(rounds)} rounds")

            # Select round
            for i in range(1, len(rounds)):
                # Open dropdown
                await page.click("#ctl00_ContentPlaceHolder1_ddlroundno_chosen")
                await page.wait_for_timeout(1000)

                # Find and click the option directly (without storing references)
                option = await page.wait_for_selector(
                    f"#ctl00_ContentPlaceHolder1_ddlroundno_chosen .chosen-drop .chosen-results li:nth-child({i + 1})"
                )
                print(option)
                option_text = await option.inner_text()
                print(f"Clicking option: {option_text}")
                await option.click()

                await page.wait_for_timeout(1000)

            exit()

            for round_num in rounds[1:]:  # Skip default option
                print(f"\nProcessing Round: {round_num['label']}")
                await page.select_option(
                    "#ctl00_ContentPlaceHolder1_ddlroundno", round_num["value"]
                )
                await page.wait_for_load_state("networkidle")
                await page.wait_for_timeout(
                    2000
                )  # Wait for institute dropdown to populate

                # Wait for and select institute
                print("Waiting for institute dropdown to populate...")
                await page.wait_for_selector(
                    "#ctl00_ContentPlaceHolder1_ddlInstitute", state="visible"
                )
                institutes = await get_options(
                    "#ctl00_ContentPlaceHolder1_ddlInstitute"
                )
                print(
                    f"Found {len(institutes)-1} institutes for round {round_num['label']}"
                )

                for i, institute in enumerate(institutes[1:], 1):
                    print(
                        f"\nProcessing institute {i}/{len(institutes)-1}: {institute['label']}"
                    )
                    await page.select_option(
                        "#ctl00_ContentPlaceHolder1_ddlInstitute", institute["value"]
                    )
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(
                        2000
                    )  # Wait for program dropdown to populate

                    # Wait for and select program
                    print("Waiting for program dropdown to populate...")
                    await page.wait_for_selector(
                        "#ctl00_ContentPlaceHolder1_ddlBranch", state="visible"
                    )
                    programs = await get_options("#ctl00_ContentPlaceHolder1_ddlBranch")
                    print(f"Found {len(programs)-1} programs for this institute")

                    for j, program in enumerate(programs[1:], 1):
                        print(
                            f"  Processing program {j}/{len(programs)-1}: {program['label']}"
                        )
                        await page.select_option(
                            "#ctl00_ContentPlaceHolder1_ddlBranch", program["value"]
                        )
                        await page.wait_for_load_state("networkidle")
                        await page.wait_for_timeout(
                            2000
                        )  # Wait for quota dropdown to populate

                        # Wait for and select quota
                        print("    Waiting for quota dropdown to populate...")
                        await page.wait_for_selector(
                            "#ctl00_ContentPlaceHolder1_ddlQuota", state="visible"
                        )
                        quotas = await get_options(
                            "#ctl00_ContentPlaceHolder1_ddlQuota"
                        )

                        for quota in quotas[1:]:
                            print(f"    Processing quota: {quota['label']}")
                            await page.select_option(
                                "#ctl00_ContentPlaceHolder1_ddlQuota", quota["value"]
                            )
                            await page.wait_for_load_state("networkidle")
                            await page.wait_for_timeout(
                                2000
                            )  # Wait for seat type dropdown to populate

                            # Wait for and select seat type
                            print("      Waiting for seat type dropdown to populate...")
                            await page.wait_for_selector(
                                "#ctl00_ContentPlaceHolder1_ddlSeatType",
                                state="visible",
                            )
                            seat_types = await get_options(
                                "#ctl00_ContentPlaceHolder1_ddlSeatType"
                            )

                            for seat_type in seat_types[1:]:
                                print(
                                    f"      Processing seat type: {seat_type['label']}"
                                )
                                await page.select_option(
                                    "#ctl00_ContentPlaceHolder1_ddlSeatType",
                                    seat_type["value"],
                                )
                                await page.wait_for_load_state("networkidle")
                                await page.wait_for_timeout(
                                    2000
                                )  # Wait for gender dropdown to populate

                                # Wait for and select gender
                                print(
                                    "        Waiting for gender dropdown to populate..."
                                )
                                await page.wait_for_selector(
                                    "#ctl00_ContentPlaceHolder1_ddlGender",
                                    state="visible",
                                )
                                genders = await get_options(
                                    "#ctl00_ContentPlaceHolder1_ddlGender"
                                )

                                for gender in genders[1:]:
                                    print(
                                        f"        Processing gender: {gender['label']}"
                                    )
                                    await page.select_option(
                                        "#ctl00_ContentPlaceHolder1_ddlGender",
                                        gender["value"],
                                    )
                                    await page.click(
                                        "#ctl00_ContentPlaceHolder1_btnSubmit"
                                    )
                                    await page.wait_for_load_state("networkidle")
                                    await page.wait_for_timeout(2000)

                                    # Get the data
                                    rows = await page.query_selector_all(
                                        "#ctl00_ContentPlaceHolder1_GridView1 > tbody > tr"
                                    )
                                    data_count = len(rows) - 1 if len(rows) > 0 else 0
                                    print(f"        Found {data_count} data rows")

                                    for row in rows[1:]:  # Skip header
                                        cols = await row.query_selector_all("td")
                                        text = [await col.inner_text() for col in cols]
                                        if text:
                                            all_data.append(
                                                {
                                                    "Round": round_num["label"],
                                                    "Institute": institute["label"],
                                                    "Program": program["label"],
                                                    "Quota": quota["label"],
                                                    "Seat Type": seat_type["label"],
                                                    "Gender": gender["label"],
                                                    "Opening Rank": text[1],
                                                    "Closing Rank": text[2],
                                                }
                                            )

                                    print("        Going back to previous page...")
                                    await page.go_back()
                                    await page.wait_for_load_state("networkidle")

                                    # Reselect all previous options after going back
                                    await page.wait_for_selector(
                                        "#ctl00_ContentPlaceHolder1_ddlroundno",
                                        state="visible",
                                    )
                                    await page.select_option(
                                        "#ctl00_ContentPlaceHolder1_ddlroundno",
                                        round_num["value"],
                                    )
                                    await page.wait_for_timeout(2000)

                                    await page.select_option(
                                        "#ctl00_ContentPlaceHolder1_ddlInstitute",
                                        institute["value"],
                                    )
                                    await page.wait_for_timeout(2000)

                                    await page.select_option(
                                        "#ctl00_ContentPlaceHolder1_ddlBranch",
                                        program["value"],
                                    )
                                    await page.wait_for_timeout(2000)

                                    await page.select_option(
                                        "#ctl00_ContentPlaceHolder1_ddlQuota",
                                        quota["value"],
                                    )
                                    await page.wait_for_timeout(2000)

                                    await page.select_option(
                                        "#ctl00_ContentPlaceHolder1_ddlSeatType",
                                        seat_type["value"],
                                    )
                                    await page.wait_for_timeout(2000)

            print("\nScraping completed successfully!")

        except TimeoutError as e:
            print(f"\nTimeout error occurred: {e}")
            print(f"Current progress: {len(all_data)} records collected")
            raise
        except Exception as e:
            print(f"\nUnexpected error occurred: {e}")
            print(f"Current progress: {len(all_data)} records collected")
            raise
        finally:
            print("Closing browser...")
            await browser.close()


try:
    print("Starting the script...")
    asyncio.run(scrape_josaa())
    print(f"\nTotal records collected: {len(all_data)}")
    print("Saving data to CSV...")
    # Save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv("josaa_opening_closing_ranks.csv", index=False)
    print("Data successfully saved to josaa_opening_closing_ranks.csv")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    if all_data:
        print("Attempting to save partial data...")
        try:
            df = pd.DataFrame(all_data)
            df.to_csv("josaa_opening_closing_ranks_partial.csv", index=False)
            print("Partial data saved to josaa_opening_closing_ranks_partial.csv")
        except Exception as save_error:
            print(f"Failed to save partial data: {save_error}")
