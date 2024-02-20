import tkinter as tk
import customtkinter as ctk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTkImage
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dotenv import load_dotenv
import os
from utils.colors import colors
# ---- all pages ----#
from .dashboard import DashboardPage
#from .analysis import AnalysisPage
#from .calculate import CalculatePage
#from .about import AboutPage
#from .settings import SettingsPage


#load environment variables from .env file
load_dotenv()

FINGRID_API_KEY = os.getenv('FINGRID_API_KEY')



# Appearance
ctk.set_appearance_mode('light')
appearance_mode = ctk.get_appearance_mode()

# Themes:
ctk.set_default_color_theme('blue')


class View(ctk.CTk):
    def __init__(self, model, controller):
        super().__init__()

        # configure window
        self.title("Electricity Consumption Analyzer")
        self.geometry(f"{1400}x{900}")
        self.model = model
        self.controller = controller

    def set_controller(self, controller, model):
        self.controller = controller 
        self.dashboard_view = DashboardPage(self, model)
        #self.show_calculate_view = CalculatePage(self, model)

    

        # ---- configure grid layout ---- #
        self.grid_columnconfigure(1, weight=1)  
        self.grid_columnconfigure((2, 3), weight=0) 
        self.grid_rowconfigure(0, weight=1)

        # ---- left sidebar frame nav links ---- #
        self.sidebar_frame = ctk.CTkFrame(
            self, width=140, corner_radius=0, fg_color=("#010626"))  # width=332 according figma prototype #2d4af1
        self.sidebar_frame.grid(
            row=0, column=0, padx=0, pady=0, sticky="news")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # right side content frame
        self.right_content_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="#010626")
        self.right_content_frame.grid(
            row=0, column=1, padx=0, pady=0, sticky="news")

        # top frame inside left sidebar frame to contain both logo and user avatar
        self.top_frame = ctk.CTkFrame(
            self.sidebar_frame, corner_radius=0, fg_color=("#010626"))
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)

        # ---- logo frame inside top frame ---- #
        self.logo_frame = ctk.CTkFrame(
            self.top_frame, corner_radius=0, fg_color=("#010626"))
        self.logo_frame.grid(row=0, column=0, sticky="n")
        self.logo_image = ctk.CTkImage(light_image=Image.open(
            "./assets/dark_logo.png"), dark_image=Image.open("./assets/light_logo.png"), size=(200, 200))
        self.logo_image_label = ctk.CTkLabel(
            self.logo_frame, image=self.logo_image, text="", text_color="#dedede", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_image_label.pack(padx=0, pady=0)

        # nav frame
        self.nav_frame = ctk.CTkFrame(
            self.sidebar_frame, width=500, corner_radius=0, fg_color=("#010626"))
        self.nav_frame.grid(row=2, column=0, padx=20, pady=0, sticky="news")

        # customTkinter image

   # button containing nav page home

        self.button_nav_home = ctk.CTkButton(
            self.nav_frame, text="Dashboard", text_color="#fff", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#010626",
            corner_radius=10,
            hover_color="#011140",
            image=ctk.CTkImage(light_image=Image.open(
                "./assets/home_light.png"), dark_image=Image.open("./assets/home_light.png"), size=(30, 30)),
            compound="left",
            anchor="w",
            command=lambda: self.controller.handle_tab_change("Dashboard",),
        )
        self.button_nav_home.grid(row=0, column=0, pady=(10, 10), sticky="ew")
        """
        # Estimate/calculate Button
        self.button_nav_about = ctk.CTkButton(
            self.nav_frame, text="Calculate", text_color="#fff", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#010626",
            corner_radius=10,
            hover_color="#011140",
            image=ctk.CTkImage(light_image=Image.open(
                "./assets/calculate.png"), dark_image=Image.open("./assets/calculate.png"), size=(30, 30)),
            command=lambda: self.controller.handle_tab_change("Calculate"),
            compound="left",
            anchor="w",
        )
        self.button_nav_about.grid(row=1, column=0, pady=(10, 10), sticky="ew")
        
        
        # About page button
        self.button_nav_settings = ctk.CTkButton(
            self.nav_frame, text="Settings", text_color="#fff", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#010626",
            corner_radius=10,
            hover_color="#011140",
            image=ctk.CTkImage(light_image=Image.open(
                "./assets/settings.png"), dark_image=Image.open("./assets/settings.png"), size=(30, 30)),
            command=lambda: self.controller.handle_tab_change("About"),
            compound="left",
            anchor="w",
        )
        self.button_nav_settings.grid(
            row=3, column=0, pady=(10, 10), sticky="ew"),
        
       """

        self.show_home_content()
    # navigation functions

    def show_home_content(self):
        for widget in self.right_content_frame.winfo_children():
            widget.destroy()
            # load the home page from home.py
        home_page_content = DashboardPage(self.right_content_frame, self.model)
        home_page_content.pack(fill="both", expand=True)

    """
    def show_calculate_content(self):
        for widget in self.right_content_frame.winfo_children():
            widget.destroy()
            # load the Calculate page from Calculate.py
        calculate_page_content = CalculatePage(self.right_content_frame, self.model)
        calculate_page_content.pack(fill="both", expand=True)

    def show_analysis_content(self):
        for widget in self.right_content_frame.winfo_children():
            widget.destroy()
            # load the analysis page from analysis.py
        analysis_page_content = AnalysisPage(self.right_content_frame, self.model)
        analysis_page_content.pack(fill="both", expand=True)


    def show_settings_content(self):
        for widget in self.right_content_frame.winfo_children():
            widget.destroy()
            # load the settings page from settings.py
        #settings_page_content = SettingsPage(self.right_content_frame, self.model)
        #settings_page_content.pack(fill="both", expand=True)


    def show_about_content(self):
        for widget in self.right_content_frame.winfo_children():
            widget.destroy()
            # load the about page from about.py
        about_page_content = AboutPage(self.right_content_frame, self.model)
        about_page_content.pack(fill="both", expand=True)

    def navigate_settings(self):
        self.show_settings_content()

    def navigate_Dashboard(self):
        self.controller.handle_tab_change("Dashboard")

     def navigate_analysis(self):
        self.controller.handle_tab_change("Analysis") 

    def navigate_calculate(self):
        self.controller.handle_tab_change("Calculate")

    def navigate_about(self):
        self.controller.handle_tab_change("About")

"""
