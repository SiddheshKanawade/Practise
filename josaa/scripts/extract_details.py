from bs4 import BeautifulSoup
import pandas as pd
import os
import glob

# Get all HTML files from raw_data directory and its subdirectories
html_files = glob.glob("./raw_data/**/**/*.html", recursive=True)

for filename in html_files:
    # Extract category and round name from the file path
    parts = filename.split("/")
    category = parts[2]  # Category is the subdirectory name (open, obc-ncl, etc.)
    round_name = parts[-1].split(".")[0]  # Round name from the filename

    print(f"Processing {category} - {round_name}...")

    # Load HTML file
    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find the table by ID
    table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_GridView1"})

    # Initialize data list
    data = []

    # Extract rows, skipping the header
    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 7:
            continue  # skip malformed rows

        data.append(
            [
                round_name[-1],
                cols[0].text.strip(),  # Institute
                cols[1].text.strip(),  # Academic Program Name
                cols[2].text.strip(),  # Quota
                cols[3].text.strip(),  # Seat Type
                cols[4].text.strip(),  # Gender
                cols[5].text.strip(),  # Opening Rank
                cols[6].text.strip(),  # Closing Rank
            ]
        )

    # Define column names from table header
    columns = [
        "Round",
        "Institute",
        "Academic Program Name",
        "Quota",
        "Seat Type",
        "Gender",
        "Opening Rank",
        "Closing Rank",
    ]

    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Save to CSV
    dir = f"./output/{category}/"
    os.makedirs(dir, exist_ok=True)
    path = f"{dir}/{round_name}.csv"
    df.to_csv(path, index=False)
    print(f"CSV saved as {path}")
