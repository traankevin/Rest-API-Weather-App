import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import requests


# Function to fetch and display weather data
def get_weather():
    city = search_bar.get()
    url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                city_data = data['results'][0]
                lat = city_data['latitude']
                lon = city_data['longitude']
                
                # Fetch weather data using latitude and longitude
                weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,rain,snowfall,cloud_cover,wind_speed_10m'
                weather_response = requests.get(weather_url)
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    temp_c = weather_data['hourly']['temperature_2m'][0]
                    cloudcover = weather_data['hourly']['cloud_cover'][0]
                    windspeed_kmh = weather_data['hourly']['wind_speed_10m'][0]
                    humidity_percent = weather_data['hourly']['relative_humidity_2m'][0]
                    snowfall = weather_data['hourly']['snowfall'][0]
                    rainfall = weather_data['hourly']['rain'][0]
                    
                    # Convert temperature to Fahrenheit
                    temp_f = (temp_c * 9/5) + 32
                    # Convert windspeed to mph
                    windspeed_mph = windspeed_kmh * 0.621371
                    
                    temperature.config(text=f"{temp_f:.1f} °F")
                    humidity.config(text=f"Humidity\n{humidity_percent:.1f}%")
                    windspeed_text.config(text=f"Windspeed\n{windspeed_mph:.1f} mph")
                    
                    if rainfall > 0:
                        weather_label.config(image=rain_img)
                        weatherCondition.config(text="Rain")
                    elif snowfall > 0:
                        weather_label.config(image=snow_img)
                        weatherCondition.config(text="Snow")
                    elif cloudcover > 50:
                        weather_label.config(image=weather_img)
                        weatherCondition.config(text="Cloudy")
                    else:
                        weather_label.config(image=sunny_img)
                        weatherCondition.config(text="Sunny")

                        
            else:
                print("City not found")
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)


# Main window
win = tk.Tk()
win.geometry('350x500')
win.eval('tk::PlaceWindow . center')
win.title("Weather App")
icon_path = 'sunny.ico'
win.iconbitmap(icon_path)
win.resizable(False,False)

# Search bar
search_bar = tk.Entry(win, width=30, font=('Roboto', 12))
search_bar.insert(0, "Enter City")
search_bar.grid(row=0, column=1, padx=10, pady=20)

# Resize image
original_image = Image.open('search.png')
resized_image = original_image.resize((25, 25), Image.LANCZOS)
click_btn = ImageTk.PhotoImage(resized_image)

# Search button with resized image
search_btn = tk.Button(win, image=click_btn, command=get_weather)
search_btn.grid(row=0, column=2, padx=0, pady=0)

#default image for weather
weather_img = PhotoImage(file="cloudy.png")
sunny_img = PhotoImage(file="clear.png")
rain_img = PhotoImage(file="rain.png")
snow_img = PhotoImage(file="snow.png")
weather_label = tk.Label(win, image=weather_img)
weather_label.place(relx=0.5, rely=0.33, anchor='center')

#display text for temperature
temperature = tk.Label(text = "10 F")
temperature.config(font=("Roboto", 30))
temperature.place(relx=0.5, rely=0.65,anchor='center')

#display weather condition
weatherCondition = tk.Label(text= "Cloudy")
weatherCondition.config(font=("Roboto",20))
weatherCondition.place(relx=0.5,rely=0.73,anchor='center')

#Resize humidity image
original_image = Image.open('humidity.png')
resized_image = original_image.resize((55, 55), Image.LANCZOS)
humidity_img = ImageTk.PhotoImage(resized_image)

#display the humidity image
humidity_label = tk.Label(win, image=humidity_img)
humidity_label.place(relx=0.15,rely=0.9,anchor='center')

#display text for humidity
humidity = tk.Label(text = "Humidity\n100%")
humidity.config(font=("Roboto", 10,"bold"))
humidity.place(relx=0.3, rely=0.9,anchor='center')

#Resize windspeed image
original_image = Image.open('windspeed.png')
resized_image = original_image.resize((55, 55), Image.LANCZOS)
windspeed_img = ImageTk.PhotoImage(resized_image)

#display the windspeed image
windspeed_label = tk.Label(win, image=windspeed_img)
windspeed_label.place(relx=0.59,rely=0.9,anchor='center')

#display text for windspeed
windspeed_text = tk.Label(text = "Windspeed\n15mph")
windspeed_text.config(font=("Roboto", 10,"bold"))
windspeed_text.place(relx=0.8, rely=0.9,anchor='center')



win.mainloop()

