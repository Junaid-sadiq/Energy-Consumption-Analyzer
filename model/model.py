import requests
import datetime
from .constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter, HourLocator
import json
import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from entsoe import EntsoePandasClient


# ----load environment variables from .env file ----#
load_dotenv()

# ---- FINGRID API key and Base URL ----#
FINGRID_API_KEY = os.getenv('FINGRID_API_KEY')
FINGRID_ENERGY_CONSUMPTION_DATA = os.getenv('FINGRID_ENERGY_CONSUMPTION_DATA')
# ---- OpenWeather API and Base URL ----#
BASE_URL = os.getenv("OPEN_WEATHER_BASE_URL")
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

# ---- IPSTACK API ---- #
IPSTACK_API_KEY = os.getenv("IPSTACK_API_KEY")



class Model():
    def __init__(self, city="Tampere"):
        self.temp_celcius = None
        self.temp_fahrenheit = None
        self.temp_kelvin = None
        self.feels_like_celcius = None
        self.feels_like_fahrenheit = None
        self.feels_like_kelvin = None
        self.humidity = None
        self.city = city
        self._fetch_temperature()

        # ---- Entsoe API ---- #
        self.ENTSOE_API_KEY = os.getenv("ENTSOE_API_KEY")

        #self.fetch_co2_data()

        user_location = self.fetch_user_location()
        if user_location and 'city' in user_location:
            self.city = user_location['city']
        self._fetch_temperature(self.city)

    def _kelvin_to_celcius_farenheit(self, kelvin):
        celcius = kelvin - 273.15
        farenheit = (celcius * 9 / 5) + 32
        return celcius, farenheit

    def _fetch_temperature(self, city = "Tampere"):
        url = BASE_URL + '&appid=' + API_KEY + '&q=' + f'{city}'
        response = requests.get(url).json()

        temp_kelvin = response['main']['temp']
        temp_celcius, temp_fahrenheit = self._kelvin_to_celcius_farenheit(temp_kelvin)
        self.temp_celcius = format(temp_celcius, '.2f')
        self.temp_fahrenheit = format(temp_fahrenheit, '.2f')

        feels_like_kelvin = response['main']['feels_like']
        feels_like_celcius, feels_like_fahrenheit = self._kelvin_to_celcius_farenheit(feels_like_kelvin)
        self.feels_like_celcius = format(feels_like_celcius, '.2f')
        self.feels_like_fahrenheit = format(feels_like_fahrenheit, '.2f')

        self.humidity = response['main']['humidity']
        self.description = response['weather'][0]['description']

    def get_weather_plot_day(self, city_name):
            params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',
             }

            response = requests.get(FORECAST_URL, params=params)
            data = response.json()

            one_day_later = datetime.now() + timedelta(hours=24 - datetime.now().hour + 1)

            # Extract date and temperature from the forecast data within the next 24 hours
            dates = []
            temperatures = []
            for item in data['list']:
                forecast_time = datetime.fromtimestamp(item['dt']) - timedelta(hours=datetime.now().hour + 1)
                if forecast_time <= one_day_later:
                    dates.append(forecast_time)
                    temperatures.append(item['main']['temp'])

            fig = Figure(figsize=(5, 2), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(dates, temperatures, marker='o', linestyle='-')

            ax.xaxis.set_major_locator(HourLocator())
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
            ax.set_xlabel('Time')
            ax.set_ylabel('Temperature (°C)')
            ax.grid(True)

            return fig

    def get_weekly_temperature_graph(self, city_name):
        
        LAT, LON = CITY_COORDINATES[city_name]
        FOLDER_PATH = './model/cached_jsons/'  # The local folder where JSON files are stored

        # Prepare to store min and max temperatures
        min_temps = []
        max_temps = []
        dates = []

        # Get data for the last 7 days
        for day in range(7):
            date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')
            file_path = os.path.join(FOLDER_PATH, f'{city_name}/{date}.json')

            # Check if data for the date is already present locally
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    weather_data = json.load(file)
            else:
                # Data not present, make an API call
                params = {
                    'lat': LAT,
                    'lon': LON,
                    'date': date,
                    'tz': '+03:00',
                    'appid': API_KEY_ONECALL,
                    'units': 'metric'  # Ensure temperatures are in Celsius
                }
                res = requests.get(BASE_URL_ONECALL, params=params)
                if res.status_code == 200:
                    weather_data = res.json()
                    # Save the data locally
                    with open(file_path, 'w') as file:
                        json.dump(weather_data, file)
                else:
                    continue  # Skip this date if the API call fails

            min_temps.append(weather_data['temperature']['min'])
            max_temps.append(weather_data['temperature']['max'])
            dates.append(date)

        # Reverse the lists to show the most recent date on the right
        dates.reverse()
        min_temps.reverse()
        max_temps.reverse()

        # Create the figure and plot the data
        fig = Figure(figsize=(5, 2))
        ax = fig.add_subplot(111)
        ax.plot(dates, max_temps, marker='o', linestyle='-', color='green', label='Max Temperature (°C)')
        ax.plot(dates, min_temps, marker='o', linestyle='-', color='red', label='Min Temperature (°C)')
        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(f'Min and Max Temperature for the Last 7 Days in {city_name}')
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)
        return fig

    def get_month_temperature_graph(self, city_name):
        
        LAT, LON = CITY_COORDINATES[city_name]
        FOLDER_PATH = './model/cached_jsons/'  # The local folder where JSON files are stored

        # Prepare to store min and max temperatures
        min_temps = []
        max_temps = []
        dates = []

        # Get data for the last 10 days
        for day in range(30):
            date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')
            file_path = os.path.join(FOLDER_PATH, f'{city_name}/{date}.json')

            # Check if data for the date is already present locally
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    weather_data = json.load(file)
            else:
                # Data not present, make an API call
                params = {
                    'lat': LAT,
                    'lon': LON,
                    'date': date,
                    'tz': '+03:00',
                    'appid': API_KEY_ONECALL,
                    'units': 'metric'  # Ensure temperatures are in Celsius
                }
                res = requests.get(BASE_URL_ONECALL, params=params)
                if res.status_code == 200:
                    weather_data = res.json()
                    # Save the data locally
                    with open(file_path, 'w') as file:
                        json.dump(weather_data, file)
                else:
                    continue  # Skip this date if the API call fails

            min_temps.append(weather_data['temperature']['min'])
            max_temps.append(weather_data['temperature']['max'])
            dates.append(date)

        # Reverse the lists to show the most recent date on the right
        dates.reverse()
        min_temps.reverse()
        max_temps.reverse()

        # Create the figure and plot the data
        fig = Figure(figsize=(5, 2))
        ax = fig.add_subplot(111)
        ax.plot(dates, max_temps, marker='o', linestyle='-', color='green', label='Max Temperature (°C)')
        ax.plot(dates, min_temps, marker='o', linestyle='-', color='red', label='Min Temperature (°C)')
        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(f'Min and Max Temperature for the Last 30 Days in {city_name}')
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)
        return fig



    def get_temperature_celcius(self, city ="Tampere"):
        self._fetch_temperature(city)
        return self.temp_celcius

    def get_temperature_farenheit(self):
        return self.temp_fahrenheit

    def get_current_datatime(self):
        return datetime.now().strftime("%b %d, %Y %H:%M")
    
    def fetch_user_location(self):
        try:
            response = requests.get(f"http://api.ipstack.com/check?access_key={IPSTACK_API_KEY}")
            if response.status_code == 200:
                return response.json()
            else:
                print("Error fetching location: HTTP", response.status_code)
                return None
        except Exception as e:
            print("An error occurred:", e)
            return None
        
    # ---- day Ahead prices for a day, week and month ---- #
    def fetch_day_ahead_prices(self):
        client = EntsoePandasClient(api_key=self.ENTSOE_API_KEY)
        start = pd.Timestamp.now(tz='Europe/Helsinki').floor('d')
        end = start + pd.Timedelta(days=1)
        # 'FI' is the bidding zone code for Finland
        bidding_zone = 'FI'
        try:
            df = client.query_day_ahead_prices(bidding_zone, start=start, end=end)
            return df
        except Exception as e:
            print(f"Error fetching day ahead prices: {e}")
            return None  
    
    def fetch_weekly_prices(self):
        client = EntsoePandasClient(api_key=self.ENTSOE_API_KEY)
        end = pd.Timestamp.now(tz='Europe/Helsinki').floor('d')  # Current date
        start = end - pd.Timedelta(days=7)  # One week ago
        bidding_zone = 'FI'
        try: 
            df = client.query_day_ahead_prices(bidding_zone, start=start, end=end)
            return df
            
        except Exception as e:
            print(f"Error fetching weekly prices: {e}")
            return None
                                      
    def fetch_monthly_prices(self):
        client = EntsoePandasClient(api_key=self.ENTSOE_API_KEY)
        end = pd.Timestamp.now(tz='Europe/Helsinki').floor('d')  # Current date
        start = end - pd.Timedelta(days=30)  # One month ago
        bidding_zone = 'FI'
        try: 
            df = client.query_day_ahead_prices(bidding_zone, start=start, end=end)
            return df
        except Exception as e:
            print(f"Error fetching monthly prices: {e}")
            return None

    def fetch_electricity_price(self, city):
        if city.lower() != 'tampere':
            return "Currently, only Tampere is supported."

        # Replace with the actual bidding zone for Finland
        bidding_zone = 'FI'
        url = f"https://api.entsoe.eu/market-data/day-ahead-prices?biddingZone={bidding_zone}&apikey={ENTSOE_API_KEY}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("API Response:", response.text)
                prices = self.parse_electricity_prices(response.json())
                return self.calculate_final_prices(prices)
            else:
                print(f"Failed to retrieve data: HTTP Status {response.status_code}")
                return f"Failed to retrieve data: HTTP Status {response.status_code}"
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
    
    def calculate_final_prices(self, prices):
        vat_rate = 0.24  # VAT for Finland
        final_prices = [(time, price * (1 + vat_rate)) for time, price in prices]
        return final_prices
    def parse_electricity_prices(self, response_data):
        # Implement the logic to parse the electricity prices from the response
        # Assuming JSON format for simplicity
        prices = []
        for entry in response_data['prices']:
            # Example: {'time': '2023-01-01T00:00:00Z', 'price': 50.0}
            prices.append((entry['time'], entry['price']))
        return prices
    
    def fetch_daily_data(self): 
        #Set the time range to the last 24 hours
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)
        url = FINGRID_ENERGY_CONSUMPTION_DATA
        params = {
            'start_time': start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'end_time': end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        headers = {
            "x-api-key": FINGRID_API_KEY,
            "Accept": "text/csv"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            timestamps = [datetime.strptime(line.split(",")[1], "%Y-%m-%dT%H:%M:%S%z") for line in lines[1:]]
            values = [float(line.split(",")[2]) for line in lines[1:]]
            return timestamps, values
        else:
            print("Failed to fetch data from FINGRID API")
            return None, None
         
    def fetch_weekly_data(self): 
        #Set the time range to the last 7 days
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        url = FINGRID_ENERGY_CONSUMPTION_DATA
        params = {
            'start_time': start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'end_time': end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        headers = {
            "x-api-key": FINGRID_API_KEY,
            "Accept": "text/csv"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            timestamps = [datetime.strptime(line.split(",")[1], "%Y-%m-%dT%H:%M:%S%z") for line in lines[1:]]
            values = [float(line.split(",")[2]) for line in lines[1:]]
            return timestamps, values
        else:
            print("Failed to fetch data from FINGRID API")
            return None, None
    def fetch_monthly_data(self): 
        # Set the time range to the last 30 days
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
        url = FINGRID_ENERGY_CONSUMPTION_DATA
        params = {
            'start_time': start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'end_time': end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        headers = {
            "x-api-key": FINGRID_API_KEY,
            "Accept": "text/csv"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            timestamps = [datetime.strptime(line.split(",")[1], "%Y-%m-%dT%H:%M:%S%z") for line in lines[1:]]
            values = [float(line.split(",")[2]) for line in lines[1:]]
            return timestamps, values
        else:
            print("Failed to fetch data from FINGRID API")
            return None, None  