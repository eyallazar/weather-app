import requests
from datetime import datetime, timedelta
import json

class WeatherApp:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        
    def get_user_location(self):
        """Get user's location via IP-based geolocation"""
        try:
            response = requests.get("https://ipapi.co/json/")
            if response.status_code == 200:
                data = response.json()
                return data.get('latitude'), data.get('longitude'), data.get('city')
            else:
                return None, None, None
        except Exception as e:
            print(f"Error getting location: {e}")
            return None, None, None
    
    def get_weather(self, latitude, longitude):
        """Fetch weather data for today and tomorrow"""
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
                "timezone": "auto"
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print("Error fetching weather data")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_weather_description(self, code):
        """Convert WMO weather code to description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail"
        }
        return weather_codes.get(code, "Unknown")
    
    def get_clothing_tips(self, temp_max, temp_min, weather_code, precipitation):
        """Generate clothing recommendations based on weather"""
        tips = []
        
        avg_temp = (temp_max + temp_min) / 2
        
        # Temperature-based recommendations
        if avg_temp < 0:
            tips.append("🧥 Wear heavy winter coat, thermal underwear, and insulated boots")
            tips.append("🧤 Don't forget gloves, scarf, and winter hat")
        elif avg_temp < 10:
            tips.append("🧥 Wear a winter coat or thick sweater")
            tips.append("🧤 Bring gloves and scarf")
        elif avg_temp < 15:
            tips.append("🧥 Wear a light jacket or sweater")
            tips.append("👖 Long pants recommended")
        elif avg_temp < 20:
            tips.append("👕 Light layers - long-sleeve shirt with light jacket")
            tips.append("👖 Jeans or casual pants")
        elif avg_temp < 25:
            tips.append("👕 T-shirt or short-sleeve shirt")
            tips.append("👖 Shorts or light pants")
        else:
            tips.append("👕 Light t-shirt or tank top")
            tips.append("👖 Shorts or summer dress")
            tips.append("☀️ Apply sunscreen!")
        
        # Precipitation-based recommendations
        if precipitation > 0:
            tips.append("☔ Bring an umbrella or rain jacket")
        
        # Weather condition recommendations
        if weather_code in [95, 96, 99]:  # Thunderstorm
            tips.append("⚡ Thunderstorm expected - stay indoors if possible")
        
        if weather_code in [71, 73, 75, 77, 85, 86]:  # Snow
            tips.append("❄️ Snow expected - wear waterproof boots")
        
        if weather_code in [0, 1]:  # Clear sky
            tips.append("😎 Sunny weather - wear sunglasses")
        
        return tips
    
    def run(self):
        """Main application flow"""
        print("=" * 60)
        print("🌤️  WEATHER APP - Today & Tomorrow Forecast 🌤️")
        print("=" * 60)
        
        # Get user location
        print("\n📍 Getting your location...")
        lat, lon, city = self.get_user_location()
        
        if lat is None:
            print("❌ Could not determine your location")
            print("Please enter location manually:")
            city = input("Enter city name: ")
            # For manual input, use a fixed location or ask for coordinates
            print("Please enter latitude and longitude:")
            lat = float(input("Latitude: "))
            lon = float(input("Longitude: "))
        else:
            print(f"✅ Location detected: {city}")
        
        # Get weather data
        print("\n📡 Fetching weather data...")
        weather_data = self.get_weather(lat, lon)
        
        if weather_data is None:
            print("❌ Could not fetch weather data")
            return
        
        print("\n" + "=" * 60)
        print(f"📍 Weather for: {city}")
        print("=" * 60)
        
        daily_data = weather_data['daily']
        dates = daily_data['time'][:2]
        temps_max = daily_data['temperature_2m_max'][:2]
        temps_min = daily_data['temperature_2m_min'][:2]
        weather_codes = daily_data['weathercode'][:2]
        precipitation = daily_data.get('precipitation_sum', [0, 0])[:2]
        
        for i in range(2):
            date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
            day_name = "TODAY" if i == 0 else "TOMORROW"
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
            
            print(f"\n🗓️  {day_name} - {formatted_date}")
            print("-" * 60)
            print(f"🌡️  Temperature: {temps_max[i]}°C (max) / {temps_min[i]}°C (min)")
            print(f"☁️  Condition: {self.get_weather_description(weather_codes[i])}")
            print(f"💧 Precipitation: {precipitation[i]}mm")
            
            print(f"\n👕 WHAT TO WEAR:")
            tips = self.get_clothing_tips(
                temps_max[i], 
                temps_min[i], 
                weather_codes[i], 
                precipitation[i]
            )
            for tip in tips:
                print(f"  {tip}")
        
        print("\n" + "=" * 60)
        print("Have a great day! ☀️")
        print("=" * 60)

if __name__ == "__main__":
    app = WeatherApp()
    app.run()

