BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
API_KEY = '7f00b05b360761ff63776605f6f40a52'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast?'
BASE_URL_ONECALL = 'https://api.openweathermap.org/data/3.0/onecall/day_summary'
API_KEY_ONECALL = 'c8f27e89cbba235ff0109763faf939d6'


colors = {
    "primary": "#010626",
    "secondary": "#011140",
    "brown": "#A69992",
    "darkbrown": "#8C5845",
    "white": "#ffffff",
    "neutral1": "#fcfcfc",
    "neutral2": "#D9D5D2",
    "neutral3": "#C3C3C3",
    "neutral4": "#6F767E",
    "neutral5": "#33383F",
    "neutral6": "#272B30",
    "neutral7": "#1A1D1F",
    "neutral8": "#1A1D1F",
    "neutral9": "#111315",
    "shade1": "#9A9FA5",
    "shade2": "#6F767E",
    "shade3": "rgba(111, 118, 126, 0.40)",
    "shade4": "rgba(17, 19, 21, 0.50)",
    "black": "#000000",
    "blue": "#2A85FF",
    "green": "#00C853",
    "orage": "#FF6A55",
    "red": "#E44982",
    "purple": "#8E59FF",
}

CITY_COORDINATES = {
    "Tampere": (61.4978, 23.7610),
    "Helsinki": (60.1699, 24.9384),
    "Espoo": (60.2055, 24.6559),
    "Turku": (60.4518, 22.2666),
    "Oulu": (65.0121, 25.4651),
    "Lahti": (60.9827, 25.6612),
    "Kupio": (62.8980, 27.6782),
    "Jyväskylä": (62.2426, 25.7473),
    "Pori": (61.4851, 21.7974),
    "Lappeenranta" : (61.0550, 28.1897),
    "Kuopio": (62.8980, 27.6782)
}

LEFT_SIDEBAR_CONFIGS = {
    "width": 300,
    "corner_radius": 0,
    "fg_color": colors['primary']
}

MAIN_WINDOW_CONFIGS = {
    'title' : 'Energy Consuption Analyzer',
    'window_resolution': '1200x800'
}