import requests
import pandas as pd

# Fetch GDP Growth (annual %) Data
gdp_growth_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.KD.ZG?format=json&date=2000:2020&per_page=2000"
response_growth = requests.get(gdp_growth_url)
data_growth = response_growth.json()

# Parse GDP Growth Data
gdp_growth_records = []
for entry in data_growth[1]:
    if entry["value"] is not None:
        gdp_growth_records.append({
            "Country": entry["country"]["value"],
            "Country Code": entry["country"]["id"],
            "Year": int(entry["date"]),
            "Indicator Name (Growth)": entry["indicator"]["value"],
            "Indicator Code (Growth)": entry["indicator"]["id"],
            "GDP Growth (%)": entry["value"]
        })

gdp_growth_df = pd.DataFrame(gdp_growth_records)

# Fetch GDP (Current US$) Data
gdp_current_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&date=2000:2020&per_page=2000"
response_current = requests.get(gdp_current_url)
data_current = response_current.json()

# Parse GDP (Current US$) Data
gdp_current_records = []
for entry in data_current[1]:
    if entry["value"] is not None:
        gdp_current_records.append({
            "Country": entry["country"]["value"],
            "Country Code": entry["country"]["id"],
            "Year": int(entry["date"]),
            "Indicator Name (Current US$)": entry["indicator"]["value"],
            "Indicator Code (Current US$)": entry["indicator"]["id"],
            "GDP (Current US$)": entry["value"]
        })

gdp_current_df = pd.DataFrame(gdp_current_records)

# Merge the DataFrames on Country and Year
merged_df = pd.merge(
    gdp_growth_df, gdp_current_df, on=["Country", "Country Code", "Year"], how="inner"
)

# Save the Merged Data
merged_df.to_csv("./data/merged_gdp_data.csv", index=False)

