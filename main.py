# Step 3.1: Fetch HTML Content
# Please be careful to follow instructions on how to run the program; 
# the Run menu or right-click > Run options do not work in the simulated environment. 
# Ensure you have run the terminal command to install the correct libraries using pip.
# You must use the terminal window as directed in Step 3.
### YOUR CODE HERE ###
import requests
from bs4 import BeautifulSoup

# Fetch the webpage content
url = "http://127.0.0.1:5500/baseball_stats.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Print the HTML content to inspect
print(soup.prettify())

# Step 3.2: Extract the Required Data
### YOUR CODE HERE ###
# Find the table with the game stats
# Try to locate the table
table = soup.find('table')  # Adjust with class_ or id= if needed

if not table:
    print("No table found! Check HTML structure.")
    exit()

# Extract headers
headers = [th.text.strip() for th in table.find_all('th')]

# Extract rows into list of dicts
game_data = []
for tr in table.find_all('tr')[1:]:  # skip header row
    tds = tr.find_all('td')
    if len(tds) == len(headers):
        row = {headers[i]: tds[i].text.strip() for i in range(len(tds))}
        game_data.append(row)

# Inspect
for row in game_data[:3]:
    print(row)

# Step 4.1: Convert to a DataFrame
# Import pandas
### YOUR CODE HERE ###

import pandas as pd

import pandas as pd
import re

# Step 4.1: Convert to a DataFrame
df = pd.DataFrame(game_data)

# Normalize column names: lowercase, replace non-alphanumeric characters with underscores
def normalize_column(col):
    col = col.strip().lower()
    col = re.sub(r'[^a-z0-9]+', '_', col)        # Replace non-alphanumeric with _
    col = re.sub(r'_+', '_', col).strip('_')     # Remove duplicate/leading/trailing underscores
    return col

df.columns = [normalize_column(col) for col in df.columns]

# Debug: print the cleaned column names
print("Cleaned column names:", df.columns.tolist())

# Clean and convert specific fields
if "expected_runs" in df.columns:
    df["expected_runs"] = pd.to_numeric(df["expected_runs"], errors='coerce')

if "over_under" in df.columns:
    df["over_under"] = df["over_under"].str.lower()

if "moneyline_favorite" in df.columns:
    df["moneyline_favorite"] = df["moneyline_favorite"].str.strip()

# Preview the cleaned DataFrame
print(df.head())



# Step 5.1: Save to a CSV File
# Save the DataFrame to a CSV file named sports_statistics.csv
### YOUR CODE HERE ###

import pandas as pd
import re

# Convert scraped data to DataFrame
df = pd.DataFrame(game_data)

# Normalize column names
def normalize_column(col):
    col = col.strip().lower()
    col = re.sub(r'[^a-z0-9]+', '_', col)
    col = re.sub(r'_+', '_', col).strip('_')
    return col

df.columns = [normalize_column(col) for col in df.columns]

# Clean specific fields
if "expected_runs" in df.columns:
    df["expected_runs"] = pd.to_numeric(df["expected_runs"], errors='coerce')
if "over_under" in df.columns:
    df["over_under"] = df["over_under"].str.lower()
if "moneyline_favorite" in df.columns:
    df["moneyline_favorite"] = df["moneyline_favorite"].str.strip()
    
# Rename columns to match exact required header format
df.rename(columns={
    'gameid': 'GameID',
    'team_1': 'Team 1',
    'team_2': 'Team 2',
    'expected_runs_team_1': 'Expected Runs (Team 1)',
    'expected_runs_team_2': 'Expected Runs (Team 2)',
    'over_under': 'Over/Under',
    'moneyline_favorite': 'Moneyline Favorite'
}, inplace=True)

# Save to CSV with correct headers
df.to_csv('sports_statistics.csv', index=False)
print("CSV saved with correct headers.")

