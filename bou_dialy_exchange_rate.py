# OOP WITH PYTHON ASSIGNMENT 3

# *** QUESTION 6 ***
print("\n\n*** QUESTION 6 ***\n\n")


import requests
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class ExchangeRatePipeline:
    def __init__(self, currencies=['USD','GBP','EUR'], local_file='exchange_rates.json', api_url=None):
        
 #       Initialize the pipeline.
 #       - currencies: list of currency codes to track (against UGX).
 #       - local_file: path to JSON file to load/save raw or processed data.
 #       - api_url: optional URL to fetch live data.
        
        self.currencies = currencies
        self.local_file = local_file
        self.api_url = api_url
        self.raw_data = None
        self.df = None

    def fetch_data(self):
        
  #      Try to fetch data from API URL; if fails, fall back to local file.
        
        try:
            if self.api_url:
                resp = requests.get(self.api_url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                print("Fetched data from API.")
            else:
                raise ValueError("No API URL provided; using local file only.")
        except (requests.RequestException, ValueError) as e:
            print(f"Warning: API fetch failed ({e}); attempting to load local file.")
            if os.path.exists(self.local_file):
                with open(self.local_file, 'r') as f:
                    data = json.load(f)
                print("Loaded data from local file.")
            else:
                raise FileNotFoundError(f"Local file {self.local_file} not found, and API fetch failed.")
        self.raw_data = data
        return data

    def clean_transform(self):
        
   #     Clean and transform raw JSON into a pandas DataFrame with columns:
   #     date, currency, rate_ugx.
        
        if self.raw_data is None:
            raise ValueError("No raw data available. Call fetch_data() first.")

        records = []
        # assume raw_data structure: list of dicts or dict of dates → currency rates
        # We will attempt a plausible parsing logic; user may adapt to actual structure.
        for entry in self.raw_data.get('data', []) if 'data' in self.raw_data else self.raw_data:
            try:
                date_str = entry.get('date') or entry.get('Date') or entry.get('day')
                date = pd.to_datetime(date_str)
                for cur in self.currencies:
                    if cur in entry:
                        rate = float(entry[cur])
                        records.append({'date': date, 'currency': cur, 'rate_ugx': rate})
            except Exception as e:
                print(f"Skipped entry due to parse error: {entry} → {e}")

        if not records:
            raise ValueError("No valid currency records extracted from raw data.")

        df = pd.DataFrame(records)
        df = df.sort_values('date')
        self.df = df
        print("Data cleaned and transformed into DataFrame.")
        return df

    def compute_monthly_averages(self):
        """
        Using numpy/pandas, compute monthly average rates for each currency.
        """
        if self.df is None:
            raise ValueError("Dataframe not prepared. Call clean_transform() first.")

        self.df['year_month'] = self.df['date'].dt.to_period('M')
        monthly = self.df.groupby(['year_month','currency'])['rate_ugx'].mean().reset_index()
        monthly['year_month'] = monthly['year_month'].dt.to_timestamp()
        print("Computed monthly averages.")
        return monthly

    def plot_trends(self, monthly_df):
        """
        Plot exchange rate trends (monthly averages) for each currency.
        """
        plt.figure(figsize=(10,6))
        for cur in self.currencies:
            subset = monthly_df[monthly_df['currency']==cur]
            plt.plot(subset['year_month'], subset['rate_ugx'], marker='o', label=cur)
        plt.title("Monthly Average Exchange Rates (UGX per unit)")
        plt.xlabel("Month")
        plt.ylabel("Rate (UGX)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        print("Plotted trends.")

    def export(self, monthly_df, csv_file='processed_rates.csv', json_file='processed_rates.json'):
        """
        Export the processed monthly averages to CSV and JSON.
        """
        try:
            monthly_df.to_csv(csv_file, index=False)
            print(f"Exported CSV to {csv_file}")
        except Exception as e:
            print(f"CSV export failed: {e}")

        try:
            monthly_df.to_json(json_file, orient='records', date_format='iso')
            print(f"Exported JSON to {json_file}")
        except Exception as e:
            print(f"JSON export failed: {e}")

    def run_pipeline(self):
        """
        Full pipeline: fetch → clean/transform → compute monthly averages → plot → export.
        """
        self.fetch_data()
        df = self.clean_transform()
        monthly = self.compute_monthly_averages()
        self.plot_trends(monthly)
        self.export(monthly)

# Example usage
if __name__ == "__main__":
    # Replace api_url with actual endpoint if available
    API_URL = "https://cb-uganda.opendataforafrica.org/dajnqbb/exchange-rates"  # example dataset endpoint :contentReference[oaicite:1]{index=1}
    #API_URL = "https://api.exchangerate.host/timeseries?start_date=2023-01-01&end_date=2023-03-31&base=UGX&symbols=USD,GBP,EUR"  
    pipeline = ExchangeRatePipeline(currencies=['USD','GBP','EUR'], local_file='exchange_rates.json', api_url=API_URL)
    try:
        pipeline.run_pipeline()
    except Exception as err:
        print(f"Pipeline failed: {err}")
