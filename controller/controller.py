class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # self.view.render_main_window(self.model.get_main_window_configs())
        # self.view.render_screen(self.model.get_sidebar_configs())
        # self.view.render_sidebar()

        # Register event handlers for user interactions
        #self.view.bind_daily_button(self.fetch_and_display_daily_data)
        #self.view.bind_monthly_button(self.fetch_and_display_monthly_data)
        #self.view.bind_yearly_button(self.fetch_and_display_yearly_data)
        #self.view.bind_login_button(self.handle_login)
        #self.view.bind_settings_button(self.handle_settings)

    # When user chooses the Daily View, handler calls data fetching and then displays the result
    # This should maybe be Weekly instead of Daily?
    '''def fetch_and_display_electricity_price(self, city):
        price_data = self.model.fetch_day_ahead_prices(city)
        self.view.display_electricity_price(price_data)'''

    def fetch_and_display_daily_data(self):
        start_date, end_date = self.calculate_start_end_dates("daily")
        power_data = self.model.fetch_power_consumption_data(start_date, end_date)
        weather_data = self.model.fetch_weather_data(start_date, end_date)
        self.view.display_data(power_data, weather_data)

    # When user chooses the Monthly View, handler calls data fetching and then displays the result
    def fetch_and_display_monthly_data(self):
        start_date, end_date = self.calculate_start_end_dates("monthly")
        power_data = self.model.fetch_power_consumption_data(start_date, end_date)
        weather_data = self.model.fetch_weather_data(start_date, end_date)
        self.view.display_data(power_data, weather_data)

    # When user chooses the Yearly View, handler calls data fetching and then displays the result
    def fetch_and_display_yearly_data(self):
        start_date, end_date = self.calculate_start_end_dates("yearly")
        power_data = self.model.fetch_power_consumption_data(start_date, end_date)
        weather_data = self.model.fetch_weather_data(start_date, end_date)
        self.view.display_data(power_data, weather_data)

    def calculate_start_end_dates(self, view_type):
        # TODO
        # Calculate start and end dates based on the selected view_type (daily, monthly, yearly)
        # Requires the View to have the different graph settings implemented
        pass

    def handle_settings(self):
        # TODO
        # Implement user settings saving logic here. Requires the database
        pass
    # method to handle tabs changes in the main window
    def handle_tab_change(self, tab_name):
        # Logic to switch to the appropriate view based on the tab name
        if tab_name == 'Dashboard':
            self.view.show_home_content()
        elif tab_name == 'Calculate':
            self.view.show_calculate_content()
        #elif tab_name == 'Analysis':
        #   self.view.show_analysis_content()
        elif tab_name == 'Settings':
            self.view.show_settings_content()
        else:
            print(f"Unknown tab: {tab_name}")
    
    def fetch_and_display_day_ahead_prices(self):
        prices_df = self.model.fetch_day_ahead_prices()
        self.view.display_day_ahead_prices(prices_df)
    
    def fetch_and_display_weekly_prices(self):
        weekly_prices = self.model.fetch_weekly_prices()
        self.view.display_weekly_prices(weekly_prices)
        
    def fetch_and_display_monthly_prices(self):
        monthly_prices = self.model.fetch_monthly_prices()
        self.view.display_monthly_prices(monthly_prices)