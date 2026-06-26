import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="🌤️ Weather App", layout="centered")

st.title("🌤️ Weather App")
st.markdown("Get today's and tomorrow's forecast with clothing recommendations!")

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
            st.error(f"Error getting location: {e}")
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
                return None
        except Exception as e:
            st.error(f"Error: {e}")
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

# Create app instance
app = WeatherApp()

# Initialize session state for location
if "location_set" not in st.session_state:
    st.session_state.location_set = False
    st.session_state.lat = None
    st.session_state.lon = None
    st.session_state.city = None

# Get location
if not st.session_state.location_set:
    st.warning("⚠️ Could not detect your location automatically. Please enter it manually:")
    
    # Dropdown for quick selection of popular cities
    st.markdown("**Or select a city from the list:**")
    popular_cities = {
        # Israel - All Major Cities
        "Tel Aviv, Israel": (32.0853, 34.7818),
        "Jerusalem, Israel": (31.7683, 35.2137),
        "Haifa, Israel": (32.8188, 35.0045),
        "Beer Sheva, Israel": (31.2518, 34.7914),
        "Ashdod, Israel": (31.8073, 34.6452),
        "Ashkelon, Israel": (31.6703, 34.5703),
        "Netanya, Israel": (32.3197, 34.8604),
        "Ramat Gan, Israel": (32.0789, 34.8286),
        "Givatayim, Israel": (32.0677, 34.8128),
        "Bat Yam, Israel": (32.0104, 34.7577),
        "Holon, Israel": (31.9768, 34.7614),
        "Rishon LeZion, Israel": (31.9454, 34.7837),
        "Petah Tikva, Israel": (32.0873, 34.8864),
        "Herzliya, Israel": (32.1617, 34.7689),
        "Rehovot, Israel": (31.8969, 34.8144),
        "Kiryat Gat, Israel": (31.6049, 34.7691),
        "Ramla, Israel": (31.9236, 34.8525),
        "Lod, Israel": (31.9454, 34.8987),
        "Beit Shemesh, Israel": (31.7383, 35.1903),
        "Modiin, Israel": (31.8903, 35.1903),
        "Nahariya, Israel": (33.0063, 35.0978),
        "Kiryat Shmona, Israel": (33.2092, 35.4222),
        "Eilat, Israel": (29.5581, 34.9516),
        "Safed, Israel": (32.9726, 35.4907),
        "Jaffa, Israel": (32.0545, 34.7604),
        "Carmiel, Israel": (32.9226, 35.2857),
        "Afula, Israel": (32.6141, 35.2831),
        "Tiberias, Israel": (32.7940, 35.5300),
        "Nazareth, Israel": (32.7004, 35.2975),
        "Acre, Israel": (32.9226, 35.0685),
        "Metula, Israel": (33.2440, 35.5750),
        "Karmiel, Israel": (32.9226, 35.2857),
        
        # USA
        "New York, USA": (40.7128, -74.0060),
        "Los Angeles, USA": (34.0522, -118.2437),
        "Chicago, USA": (41.8781, -87.6298),
        "Houston, USA": (29.7604, -95.3698),
        "Miami, USA": (25.7617, -80.1918),
        "San Francisco, USA": (37.7749, -122.4194),
        "Seattle, USA": (47.6062, -122.3321),
        "Denver, USA": (39.7392, -104.9903),
        
        # Europe
        "London, UK": (51.5074, -0.1278),
        "Paris, France": (48.8566, 2.3522),
        "Berlin, Germany": (52.5200, 13.4050),
        "Rome, Italy": (41.9028, 12.4964),
        "Madrid, Spain": (40.4168, -3.7038),
        "Amsterdam, Netherlands": (52.3676, 4.9041),
        "Barcelona, Spain": (41.3851, 2.1734),
        "Vienna, Austria": (48.2082, 16.3738),
        "Prague, Czech Republic": (50.0755, 14.4378),
        "Moscow, Russia": (55.7558, 37.6173),
        "Istanbul, Turkey": (41.0082, 28.9784),
        "Athens, Greece": (37.9838, 23.7275),
        "Dublin, Ireland": (53.3498, -6.2603),
        "Lisbon, Portugal": (38.7223, -9.1393),
        "Zurich, Switzerland": (47.3769, 8.5472),
        
        # Asia
        "Tokyo, Japan": (35.6762, 139.6503),
        "Beijing, China": (39.9042, 116.4074),
        "Shanghai, China": (31.2304, 121.4737),
        "Hong Kong": (22.3193, 114.1694),
        "Singapore": (1.3521, 103.8198),
        "Bangkok, Thailand": (13.7563, 100.5018),
        "Jakarta, Indonesia": (6.1751, 106.8650),
        "Manila, Philippines": (14.5995, 120.9842),
        "Seoul, South Korea": (37.5665, 126.9780),
        "Dubai, UAE": (25.2048, 55.2708),
        "Mumbai, India": (19.0760, 72.8777),
        "Delhi, India": (28.6139, 77.2090),
        "Hanoi, Vietnam": (21.0285, 105.8542),
        "Ho Chi Minh City, Vietnam": (10.7769, 106.6869),
        "Kuala Lumpur, Malaysia": (3.1390, 101.6869),
        "Karachi, Pakistan": (24.8607, 67.0011),
        
        # Australia & Pacific
        "Sydney, Australia": (-33.8688, 151.2093),
        "Melbourne, Australia": (-37.8136, 144.9631),
        "Brisbane, Australia": (-27.4698, 153.0251),
        "Auckland, New Zealand": (-37.0882, 174.7674),
        "Wellington, New Zealand": (-41.2865, 174.7762),
        "Fiji": (-17.7997, 178.0655),
        
        # South America
        "São Paulo, Brazil": (-23.5505, -46.6333),
        "Rio de Janeiro, Brazil": (-22.9068, -43.1729),
        "Buenos Aires, Argentina": (-34.6037, -58.3816),
        "Lima, Peru": (-12.0464, -77.0428),
        "Bogotá, Colombia": (4.7110, -74.0721),
        "Cartagena, Colombia": (10.3910, -75.4794),
        "Santiago, Chile": (-33.8688, -51.2093),
        "Mexico City, Mexico": (19.4326, -99.1332),
        
        # Africa
        "Cairo, Egypt": (30.0444, 31.2357),
        "Lagos, Nigeria": (6.5244, 3.3792),
        "Johannesburg, South Africa": (-26.2023, 28.0436),
        "Cape Town, South Africa": (-33.9249, 18.4241),
        "Nairobi, Kenya": (-1.2865, 36.8172),
        "Casablanca, Morocco": (33.5731, -7.5898),
        "Dar es Salaam, Tanzania": (-6.8000, 39.2833),
        "Addis Ababa, Ethiopia": (9.0320, 38.7469),
        "Accra, Ghana": (5.6037, -0.1870),
        "Algiers, Algeria": (36.7538, 3.0588),
        
        # Middle East
        "Beirut, Lebanon": (33.8547, 35.5017),
        "Baghdad, Iraq": (33.3128, 44.3615),
        "Tehran, Iran": (35.6892, 51.3890),
        "Riyadh, Saudi Arabia": (24.7136, 46.6753),
        "Kuwait City, Kuwait": (29.3759, 47.9774),
        
        # Canada
        "Toronto, Canada": (43.6532, -79.3832),
        "Vancouver, Canada": (49.2827, -123.1207),
        "Montreal, Canada": (45.5017, -73.5673),
        
        # Custom
        "Custom Location": ("custom", "custom")
    }
    
    selected_city = st.selectbox("Select a city:", list(popular_cities.keys()))
    
    if selected_city == "Custom Location":
        col1, col2, col3 = st.columns(3)
        with col1:
            city = st.text_input("City name:", value="Tel Aviv", key="city_input")
        with col2:
            lat = st.number_input("Latitude:", value=32.0853, format="%.4f", key="lat_input")
        with col3:
            lon = st.number_input("Longitude:", value=34.7818, format="%.4f", key="lon_input")
    else:
        lat, lon = popular_cities[selected_city]
        city = selected_city
        st.success(f"✅ Location selected: **{city}**")
    
    # Show location preview
    st.info(f"📍 **Location Preview:** {city} (Lat: {lat}, Lon: {lon})")
    
    if st.button("✅ Confirm Location", type="primary", use_container_width=True):
        st.session_state.lat = lat
        st.session_state.lon = lon
        st.session_state.city = city
        st.session_state.location_set = True
        st.rerun()
else:
    st.success(f"📍 Location: **{st.session_state.city}**")
    if st.button("🔄 Change Location", type="secondary", use_container_width=True):
        st.session_state.location_set = False
        st.session_state.lat = None
        st.session_state.lon = None
        st.session_state.city = None
        st.rerun()

if st.session_state.location_set:
    lat = st.session_state.lat
    lon = st.session_state.lon
    city = st.session_state.city

# Get weather data
if st.session_state.location_set:
    if st.button("🔄 Get Weather", type="primary", use_container_width=True):
        with st.spinner("📡 Fetching weather data..."):
            weather_data = app.get_weather(lat, lon)
        
        if weather_data is None:
            st.error("Could not fetch weather data")
        else:
            st.markdown("---")
            st.markdown(f"## Weather for {city}")
            
            daily_data = weather_data['daily']
            dates = daily_data['time'][:2]
            temps_max = daily_data['temperature_2m_max'][:2]
            temps_min = daily_data['temperature_2m_min'][:2]
            weather_codes = daily_data['weathercode'][:2]
            precipitation = daily_data.get('precipitation_sum', [0, 0])[:2]
            
            for i in range(2):
                date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
                day_name = "📅 TODAY" if i == 0 else "📅 TOMORROW"
                formatted_date = date_obj.strftime("%A, %B %d, %Y")
                
                with st.container(border=True):
                    st.markdown(f"### {day_name} - {formatted_date}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🌡️ Max Temp", f"{temps_max[i]}°C")
                    with col2:
                        st.metric("❄️ Min Temp", f"{temps_min[i]}°C")
                    with col3:
                        st.metric("💧 Precipitation", f"{precipitation[i]}mm")
                    
                    st.markdown(f"**☁️ Condition:** {app.get_weather_description(weather_codes[i])}")
                    
                    st.markdown("#### 👕 What to Wear:")
                    tips = app.get_clothing_tips(
                        temps_max[i], 
                        temps_min[i], 
                        weather_codes[i], 
                        precipitation[i]
                    )
                    for tip in tips:
                        st.markdown(f"- {tip}")
            
            st.markdown("---")
            st.success("Have a great day! ☀️")
            
            # Add button to change location
            if st.button("🔄 Change Location", type="secondary", use_container_width=True, key="change_location_btn"):
                st.session_state.location_set = False
                st.session_state.lat = None
                st.session_state.lon = None
                st.session_state.city = None
                st.rerun()

st.markdown("---")
st.markdown("**How to share this app:**")
st.info("This app is ready to be deployed! Share it with others using Streamlit Cloud.")
