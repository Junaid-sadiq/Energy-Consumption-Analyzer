import tkinter as tk
import customtkinter as ctk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTkImage
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pandas as pd
from entsoe import EntsoePandasClient
from utils.colors import colors
#load environment variables from .env file
load_dotenv()

FINGRID_API_KEY = os.getenv('FINGRID_API_KEY')

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, model):
        super().__init__(parent, corner_radius=0,
                         fg_color=(colors["neutral1"]))
        self.model = model
        #print("fetch day ahead data ", self.model.fetch_day_ahead_prices())
    
        # Right side main frame
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=(colors["neutral1"]))
        self.right_frame.pack(side="right", fill="both",
                              expand=True, padx=20, pady=20)
        
  
        # Initialize the tab view for electricity trend

        self.init_tab_view()
        self.ENTSOE_API_KEY = os.getenv("ENTSOE_API_KEY")
        prices_df = self.model.fetch_day_ahead_prices()
        weekly_prices_df = self.model.fetch_weekly_prices()
        monthly_prices_df = self.model.fetch_monthly_prices()

        # Initialize the tab view for prices and add tabs
        self.init_prices_tab_view(prices_df, weekly_prices_df, monthly_prices_df) 

        # configuration for even spacing
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)

        # List of Finnish cities
        self.cities = ["Tampere", "Helsinki", "Espoo", "Turku", "Oulu",
                       "Lahti", "Kuopio", "Jyväskylä", "Pori", "Lappeenranta"]

        # default temperature
        self.default_temp = 0
        # Dashboard title
        self.dashboard_label = ctk.CTkLabel(
            self.right_frame, text="Dashboard", font=ctk.CTkFont(size=34, weight="bold"), text_color="#000"
        )
        self.dashboard_label.grid(row=0, column=0, sticky="nw", padx=10)

        # fetch weather information for the currecnt city
        self.weather_info = model
        temp_celesius = self.weather_info.get_temperature_celcius()
        # fetch current date and time when the data is fetched
        current_datetime = self.weather_info.get_current_datatime()

        # Date and time
        self.last_update_label = ctk.CTkLabel(
            self.right_frame, text=f"Last Update: {current_datetime}", font=ctk.CTkFont(size=12), text_color="#000"
        )
        self.last_update_label.grid(row=0, column=1, sticky="ne", padx=10)

        # Creating the Combobox for cities
        self.city_combobox = ctk.CTkComboBox(
            self.right_frame,
            values=self.cities,
            command=self.on_city_selected,
            fg_color=colors["primary"],
            border_color="#dedede",
            corner_radius=5,
            text_color="#F2F2F2",
            font=ctk.CTkFont("San Serif", size=12, weight="bold"),
            dropdown_font=ctk.CTkFont("San Serif", size=12, weight="bold"),
            dropdown_fg_color="#F2F2F2",
            dropdown_hover_color=(colors["neutral3"]),
            dropdown_text_color="#011140",
        )
        self.city_combobox.grid(row=1, column=1, sticky="ne", padx=10)
        # default city = Tampere
        self.city_combobox.set("Tampere")
        # Fetch the default weather information for "Tampere"
        self.weather_info = model
        default_temp_celesius = self.weather_info.get_temperature_celcius()

        # Current location
        self.location_label = ctk.CTkLabel(
            self.right_frame, text="Current Location: Tampere, Finland", font=ctk.CTkFont(size=12), text_color="#000"
        )
        self.location_label.grid(row=2, column=1, sticky="ne", padx=10)
        self.weather_label = ctk.CTkLabel(
            self.right_frame, text=f"Temperature: {default_temp_celesius}°C", font=ctk.CTkFont(size=12), text_color="#000"
        )
        self.weather_label.grid(row=3, column=1, sticky="ne", padx=10)
        # tab view
        self.tab_view = ctk.CTkTabview(
            self.right_frame,
            width=480,
            height=600,
            corner_radius=10,
            border_color=(colors["neutral3"]),
            border_width=2,
            fg_color=(colors["neutral3"]),
            segmented_button_fg_color=(colors["neutral4"]),
            segmented_button_selected_color=(colors["primary"]),
            segmented_button_selected_hover_color=(colors["secondary"]),
            # segmented_button_unselected_color="transparent",
            segmented_button_unselected_hover_color=(colors["secondary"]),
            text_color=(colors["white"]),
            text_color_disabled=(colors["neutral2"]),
        )
        self.tab_view.grid(row=5, column=0, columnspan=2, sticky="nwes", padx=10, pady=10)
        # tab 1
        self.tab_view.add("Day")
        # tab 2
        self.tab_view.add("Week")
        # tab 3
        self.tab_view.add("Month")

        day_tab =self.tab_view.tab("Day")

        fig = self.model.get_weather_plot_day("Tampere,FI")
        canvas = FigureCanvasTkAgg(fig, master=day_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        fig_week = self.model.get_weekly_temperature_graph("Tampere")
        canvas_week = FigureCanvasTkAgg(fig_week, master=self.tab_view.tab("Week"))
        canvas_week.draw()
        canvas_week.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        fig_month = self.model.get_month_temperature_graph("Tampere")

        # Embed the new figure in the 'Week' tab
        canvas_month = FigureCanvasTkAgg(fig_month, master=self.tab_view.tab("Month"))
        canvas_month.draw()
        canvas_month.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#
        self.label_1 = ctk.CTkLabel(day_tab, text="Day", )
        self.label_1.pack(padx=10, pady=10)
        self_labe_2 = ctk.CTkLabel(self.tab_view.tab("Week"), text="Week")
        self_labe_2.pack(padx=10, pady=10)
        self.label_3 = ctk.CTkLabel(self.tab_view.tab("Month"), text="Month")
        self.label_3.pack(padx=10, pady=10)

    
      
    def on_city_selected(self, selected_city):
        print("City selected:", selected_city)

        # Update the location label
        self.location_label.configure(text=f"Current Location: {selected_city}, Finland")

        # Clear the existing graph in the "Day" tab
        for widget in self.tab_view.tab("Day").winfo_children():
            widget.destroy()

        # Fetch the new figure with updated weather data for the selected city
        fig_day = self.model.get_weather_plot_day(selected_city + ",FI")

        # Embed the new figure in the 'Day' tab
        canvas_day = FigureCanvasTkAgg(fig_day, master=self.tab_view.tab("Day"))
        canvas_day.draw()
        canvas_day.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Clear the existing graph in the "Week" tab
        for widget in self.tab_view.tab("Week").winfo_children():
            widget.destroy()

        # Fetch the new figure with updated weather data for the selected city for the "Week" tab
        fig_week = self.model.get_weekly_temperature_graph(selected_city)

        # Embed the new figure in the 'Week' tab
        canvas_week = FigureCanvasTkAgg(fig_week, master=self.tab_view.tab("Week"))
        canvas_week.draw()
        canvas_week.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for widget in self.tab_view.tab("Month").winfo_children():
            widget.destroy()
        
        fig_month = self.model.get_month_temperature_graph(selected_city)

        # Embed the new figure in the 'Week' tab
        canvas_month = FigureCanvasTkAgg(fig_month, master=self.tab_view.tab("Month"))
        canvas_month.draw()
        canvas_month.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Update the displayed temperature (assuming your model has such a method)
        temp_celsius = self.weather_info.get_temperature_celcius(selected_city)
        self.weather_label.configure(text=f"Temperature: {temp_celsius}°C")

    def on_filter_clicked(self):
        print("Filter clicked")

        # Tab view configuration
    def init_tab_view(self):    
        self.tab_view = ctk.CTkTabview(
            self.right_frame, width=480, height=270, corner_radius=20,
            border_color=colors["neutral3"], border_width=2, fg_color=colors["neutral2"],
            segmented_button_fg_color=colors["neutral4"],
            segmented_button_selected_color=colors["primary"],
            segmented_button_selected_hover_color=colors["secondary"],
            segmented_button_unselected_hover_color=colors["secondary"],
            text_color=colors["white"], text_color_disabled=colors["neutral2"]
        )
        self.tab_view.grid(row=4, column=0, sticky="nw", padx=10, pady=10)
           # Add tabs for energy graphs
        self.add_energy_graph_tabs()

        

    def init_prices_tab_view(self, prices_df, weekly_prices_df, monthly_prices_df):
        self.prices_tab_view = ctk.CTkTabview(
            self.right_frame, width=480, height=270, corner_radius=20,
            border_color=colors["neutral3"], border_width=2, fg_color=colors["neutral2"],
            segmented_button_fg_color=colors["neutral4"],
            segmented_button_selected_color=colors["primary"],
            segmented_button_selected_hover_color=colors["secondary"],
            segmented_button_unselected_hover_color=colors["secondary"],
            text_color=colors["white"], text_color_disabled=colors["neutral2"]
        )
        self.prices_tab_view.grid(row=4, column=1, sticky="nw", padx=10, pady=10)
        # Add tab for energy prices
        self.add_prices_graph_tab(prices_df, weekly_prices_df, monthly_prices_df) 

    def add_energy_graph_tabs(self):
        # Add tabs for energy graphs
        self.tab_view.add("Day")  # Add the tab with the title "Day"
        self.energy_graph_day = DailyEnergyGraph(self.tab_view.tab("Day"), self.model)
        self.energy_graph_day.pack(fill='both', expand=True)
        
        self.tab_view.add("Week")  # Add the tab with the title "Week"
        self.energy_graph_week = WeeklyEnergyGraph(self.tab_view.tab("Week"), self.model)
        self.energy_graph_week.pack(fill='both', expand=True)

        self.tab_view.add("Month")  # Add the tab with the title "Month"
        self.energy_graph_month = MonthlyEnergyGraph(self.tab_view.tab("Month"), self.model)
        self.energy_graph_month.pack(fill='both', expand=True)


    def add_prices_graph_tab(self, prices_df, weekly_prices_df, monthly_prices_df):
        # Add tab for daily prices
        self.prices_tab_view.add("Day")
        self.electricity_price_graph = ElectricityPriceGraph(self.prices_tab_view.tab("Day"), self.model)
        self.electricity_price_graph.pack(fill='both', expand=True)
        if prices_df is not None:
            self.electricity_price_graph.plot_prices(prices_df, 'day')

        # Add tab for weekly prices
        self.prices_tab_view.add("Week")
        self.weekly_price_graph = ElectricityPriceGraph(self.prices_tab_view.tab("Week"), self.model)
        self.weekly_price_graph.pack(fill='both', expand=True)
        if weekly_prices_df is not None:
            self.weekly_price_graph.plot_prices(weekly_prices_df, 'week')

        # Add tab for monthly prices
        self.prices_tab_view.add("Month")
        self.monthly_price_graph = ElectricityPriceGraph(self.prices_tab_view.tab("Month"), self.model)
        self.monthly_price_graph.pack(fill='both', expand=True)
        if monthly_prices_df is not None:
            self.monthly_price_graph.plot_prices(monthly_prices_df, 'month')

        if prices_df is not None:
            self.electricity_price_graph.plot_prices(prices_df, timeframe='day')
        if  weekly_prices_df is not None:
            self.weekly_price_graph.plot_prices(weekly_prices_df, timeframe='week')
        if monthly_prices_df is not None:
            self.monthly_price_graph.plot_prices(monthly_prices_df, timeframe='month')        
        

         
    def display_day_ahead_prices(self, prices_df):
        if prices_df is not None:
            self.energy_graph_price.plot_prices(prices_df)
        else:
            print("No data to display for day-ahead prices.")
    def display_weekly_prices(self, weekly_prices_df):
        if weekly_prices_df is not None:
            self.energy_graph_price.plot_prices(weekly_prices_df, 'week')

    def display_monthly_prices(self, monthly_prices_df):
        if monthly_prices_df is not None:
            self.energy_graph_month.plot_prices(monthly_prices_df, 'month')


#Daily Enegy Consumption forcast Graph class here
class DailyEnergyGraph(ctk.CTkFrame):
    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.time_range = "day"

        self.plot_daily_graph()

    def plot_daily_graph(self):
        # Fetch the data using the model
        timestamps, values = self.model.fetch_daily_data()
        if timestamps and values:
            self.plot_graph(timestamps, values)

    def plot_graph(self, timestamps, values):
        plt.close('all')
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(timestamps, values, label="Daily Consumption")
        ax.set_title("Daily Electricity Consumption Trend for Finland")
        ax.set_xlabel("Time")
        ax.set_ylabel("Consumption (MWh)")
        ax.legend()
        fig.autofmt_xdate()

        for widget in self.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=20)

#Weekly Energy Consumption forcast Graph class here
class WeeklyEnergyGraph(ctk.CTkFrame):

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.time_range = "week"

        self.plot_weekly_graph()
    
    def plot_weekly_graph(self):
        # Fetch the data using the model
        timestamps, values = self.model.fetch_weekly_data()
        if timestamps and values:
            self.plot_graph(timestamps, values)

 
    def plot_graph(self, timestamps, values):
        plt.close('all')  # Close previous plots to prevent memory leak
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(timestamps, values, label="Weekly Consumption")
        ax.set_title("Weekly Electricity Consumption Trend for Finland")
        ax.set_xlabel("Time")
        ax.set_ylabel("Consumption (EUR/kWh)")
        ax.legend()
        fig.autofmt_xdate()
        
        # Remove existing widgets in the frame
        for widget in self.winfo_children():
            widget.destroy()
        # Add the new plot to the frame    
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=20)

    def update_graph(self, time_range):
        # Update the method to fetch data according to the time_range
        end_time = datetime.now()
        if time_range == "day":
            start_time = end_time - timedelta(days=1)
            self.time_range = "day"
        elif time_range == "week":
            start_time = end_time - timedelta(weeks=1)
            self.time_range = "week"
        elif time_range == "month":
            start_time = end_time - timedelta(days=30)
            self.time_range = "month"
        else:
            print("Unknown time range specified:", time_range)
            return

        # Fetch the data
        timestamps, values = self.fetch_fingrid_data(self.api_key, start_time, end_time)
        if timestamps and values:
            # Plot the data
            self.plot_graph(timestamps, values)

# Monthly Energy Consumption forcast Graph
class MonthlyEnergyGraph(ctk.CTkFrame):
    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.time_range = "month"

        self.plot_monthly_graph()

    def plot_monthly_graph(self):
        timestamps, values = self.model.fetch_monthly_data()
        if timestamps and values:
            plt.close('all')
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(timestamps, values, label="Monthly Consumption")
            ax.set_title("Monthly Electricity Consumption Trend for Finland")
            ax.set_xlabel("Time")
            ax.set_ylabel("Consumption (EUR/kWh)")
            ax.legend()
            fig.autofmt_xdate()

            for widget in self.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=20)

class ElectricityPriceGraph(ctk.CTkFrame):
    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model

    def plot_prices(self, price_data, timeframe):
        if isinstance(price_data, str):
            print("Error:", price_data)
            return

        if isinstance(price_data, pd.Series):
            plt.close('all')
            fig, ax = plt.subplots(figsize=(7, 4))

            # Plotting directly from Pandas Series
            price_data.plot(kind='line', marker='o', ax=ax)
            
            title = f'{timeframe.capitalize()} Ahead Electricity Prices'
            ax.set_title(title)
            ax.set_xlabel('Time')
            ax.set_ylabel('Price (EUR/kWh)')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Remove existing widgets
            for widget in self.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill='both', expand=True)
        else:
            print("Invalid data format for plotting")
    
    # # pie chart graph
    # def add_pie_chart_to_tab(self, tab_name):
    #     """Add a sample pie chart to the specified tab."""
    #     # Sample data for the pie chart
    #     labels = ['A', 'B', 'C', 'D']
    #     sizes = [15, 30, 45, 10]

    #     fig, ax = plt.subplots()
    #     ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    #     # Equal aspect ratio ensures that pie is drawn as a circle.
    #     ax.axis('equal')
    #     ax.set_title(f"Sample Pie Chart for {tab_name}")

    #     # Embed the pie chart in the specified tab of the tabview
    #     canvas = FigureCanvasTkAgg(fig, master=self.tab_view.tab(tab_name))
    #     canvas.draw()
    #     canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
