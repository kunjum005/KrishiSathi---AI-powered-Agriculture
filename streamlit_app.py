import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import tensorflow as tf
from PIL import Image
from services.weather_service import get_weather
from services.smart_diary import save_crop_history, save_fertilizer_history, get_diary_history
from services.yield_forecast_page import yield_forecast_page
from services.smart_diary import save_yield_history
from datetime import datetime





def smart_diary_page():
    st.title("📔 Smart Diary")

    st.write("Your complete farming activity history at one place.")

    history = get_diary_history()

    st.subheader("🌱 Crop Recommendation History")
    st.table(history["crop"])

    st.subheader("🧪 Fertilizer Suggestion History")
    st.table(history["fertilizer"])
    



# --- Yield Forecast History ---
    st.subheader("📈 Yield Forecast History")
    for row in history["yield"]:
       st.write(f"🌾 Crop: {row['crop_name']} | Region: {row['region']}")
       st.write(f"Predicted Yield: {row['predicted_yield']:.2f} tons/ha")
       st.write(f"Temp: {row['temperature']} | Rainfall: {row['rainfall']} | pH: {row['soil_ph']}")
       st.write(f"📅 Date: {row['date']}")
       st.write("---")

# Page configuration
st.set_page_config(
    page_title="KrishiSathi - Farmer's Companion",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication
def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""

def login_page():
    st.title("🔐 Login to KrishiSathi")
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("Farmer Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if username and password:
                    # Simple authentication (in real app, use proper auth)
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome {username}!")
                    st.rerun()
                else:
                    st.error("Please enter both username and password")
        
        st.markdown("---")
        st.info("**Demo Credentials:** Use any username and password")

# Introduction Page
def introduction_page():
    st.title("🌾 Welcome to KrishiSathi")
    st.markdown("### Your Digital Farming Companion")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **KrishiSathi** is an AI-powered agricultural assistant designed to help farmers 
        make informed decisions about their farming practices. Our platform provides:
        
        🌱 **Smart Crop Recommendations** - Get the best crop suggestions based on your soil and environment
        💧 **Fertilizer Advice** - Optimize your fertilizer usage for better yield
        🌤️ **Weather Insights** - Stay updated with real-time weather information
        📊 **Farm Analytics** - Monitor and analyze your farm's performance
        
        ### Why Choose KrishiSathi?
        
        ✅ **Scientific Approach** - Based on agricultural research and data
        ✅ **Region-Specific** - Tailored recommendations for Indian farming conditions  
        ✅ **Easy to Use** - Simple interface designed for farmers
        ✅ **Completely Free** - No hidden costs, forever free for farmers
        """)
    
    with col2:
        st.image("https://cdn.pixabay.com/photo/2017/06/10/07/18/plant-2389156_1280.png", 
                caption="Growing Together with Technology")
        
        st.markdown("""
        ### Our Mission
        To empower Indian farmers with technology-driven solutions for sustainable and profitable agriculture.
        """)
    
    st.markdown("---")
    
    # Features in cards
    st.subheader("🚀 Key Features")
    col3, col4, col5, col6, col7 = st.columns(5)
    
    with col3:
        st.info("**Crop Recommendation**\n\nAI-powered suggestions for optimal crops based on soil and climate")
    
    with col4:
        st.success("**Fertilizer Guide**\n\nPrecise fertilizer recommendations for healthy crops")
    
    with col5:
        st.warning("**Weather Forecast**\n\nReal-time weather updates and alerts")
    
    with col6:
        st.error("**Farm Management**\n\nTools to track and manage your farming activities")
        
    with col7:
        st.success("**Disease Detection**\n\nDetects the disease present in plants")
    

# Crop Recommendation Page (Your existing logic)
def crop_recommendation_page():
    st.title("🌱 Smart Crop Recommendation")
    st.markdown("Get the best crop suggestions based on your soil and environmental parameters")
    
    # Soil Parameters Section
    st.header("🌱 Soil Parameters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Nitrogen (N) content")
        N = st.slider("N", 0, 100, 70, key="n_slider")
        st.write(f"**Value:** {N}")
        
    with col2:
        st.subheader("Phosphorus (P) content")
        P = st.slider("P", 0, 100, 30, key="p_slider")
        st.write(f"**Value:** {P}")
        
    with col3:
        st.subheader("Potassium (K) content")
        K = st.slider("K", 0, 100, 40, key="k_slider")
        st.write(f"**Value:** {K}")
        
    with col4:
        st.subheader("Soil pH Level")
        pH = st.slider("pH", 4.0, 9.0, 7.8, 0.1, key="ph_slider")
        st.write(f"**Value:** {pH}")

    st.markdown("---")
    
    # Environmental Parameters Section
    st.header("🌤️ Environmental Parameters")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.subheader("Temperature (°C)")
        temperature = st.slider("Temperature", 0.0, 45.0, 30.0, 0.1, key="temp_slider")
        st.write(f"**Value:** {temperature}°C")
        
    with col6:
        st.subheader("Humidity (%)")
        humidity = st.slider("Humidity", 0.0, 100.0, 50.1, 0.1, key="humidity_slider")
        st.write(f"**Value:** {humidity}%")
        
    with col7:
        st.subheader("Rainfall (mm)")
        rainfall = st.slider("Rainfall", 0, 300, 90, 5, key="rainfall_slider")
        st.write(f"**Value:** {rainfall} mm")

    st.markdown("---")
    
    # Your existing region detection and crop recommendation functions
    def detect_region_strict(temperature, rainfall, humidity):
        # Default region detection based on environmental parameters
        if temperature >= 28 and rainfall <= 120 and humidity <= 70:
            return 'west'
        elif temperature >= 25 and rainfall >= 150 and humidity >= 70:
            return 'north'
        elif temperature >= 28 and rainfall >= 200:
            return 'south'
        elif temperature >= 26 and rainfall <= 100:
            return 'central'
        else:
            return 'north'  # default

    def get_north_india_crop(temperature, rainfall, N, P, pH, K, humidity):
        st.sidebar.info("🔍 Applying North India rules...")
        if temperature >= 28 and rainfall <= 120 and 70 <= N <= 85 and pH >= 6.5:
            return 'Cotton', "Highly Suitable - Ideal conditions for North Indian cotton"
        elif N >= 90 and rainfall >= 150 and 24 <= temperature <= 30 and K >= 40:
            return 'Sugarcane', "Highly Suitable - Optimal for sugarcane cultivation"
        elif 75 <= N <= 90 and 35 <= P <= 45 and 140 <= rainfall <= 180:
            return 'Maize', "Highly Suitable - Perfect maize growing conditions"
        elif temperature <= 22 and N >= 80 and P >= 30:
            return 'Wheat', "Highly Suitable - Ideal wheat season conditions"
        elif rainfall >= 180 and temperature >= 25 and humidity >= 70:
            return 'Rice', "Highly Suitable - Perfect paddy conditions"
        else:
            return 'Maize', "Moderately Suitable - Default North India crop"

    def get_west_india_crop(temperature, rainfall, N, P, pH, K, humidity):
        st.sidebar.info("🔍 Applying West India rules...")
        if temperature >= 28 and rainfall <= 120 and 65 <= N <= 80 and pH >= 6.5:
            return 'Cotton', "Highly Suitable - Ideal for West Indian cotton belt"
        elif N >= 85 and rainfall >= 100 and 24 <= temperature <= 32 and K >= 35:
            return 'Sugarcane', "Highly Suitable - Optimal for sugarcane"
        elif 25 <= temperature <= 32 and rainfall <= 100 and pH <= 7.5:
            return 'Mango', "Highly Suitable - Perfect for mango orchards"
        elif 60 <= N <= 75 and P >= 25 and rainfall <= 80 and temperature >= 26:
            return 'Groundnut', "Highly Suitable - Ideal groundnut conditions"
        elif rainfall <= 70 and temperature >= 28 and N <= 70:
            return 'Sorghum', "Highly Suitable - Drought resistant crop"
        else:
            return 'Cotton', "Moderately Suitable - Default West India cash crop"

    def get_south_india_crop(temperature, rainfall, N, P, pH, K, humidity):
        st.sidebar.info("🔍 Applying South India rules...")
        if rainfall >= 180 and temperature >= 24 and N >= 80:
            return 'Rice', "Highly Suitable - Ideal for paddy cultivation"
        elif temperature >= 27 and rainfall >= 150 and humidity >= 70:
            return 'Coconut', "Highly Suitable - Perfect coastal conditions"
        elif 15 <= temperature <= 25 and rainfall >= 150 and pH <= 6.5:
            return 'Coffee', "Highly Suitable - Ideal for coffee plantations"
        elif temperature <= 22 and rainfall >= 200 and humidity >= 75:
            return 'Tea', "Highly Suitable - Perfect for tea estates"
        elif 22 <= temperature <= 30 and 100 <= rainfall <= 180 and P >= 20:
            return 'Spices', "Highly Suitable - Good for spice cultivation"
        else:
            return 'Rice', "Moderately Suitable - Default South India staple"

    def get_east_india_crop(temperature, rainfall, N, P, pH, K, humidity):
        st.sidebar.info("🔍 Applying East India rules...")
        if rainfall >= 160 and temperature >= 22 and N >= 75:
            return 'Rice', "Highly Suitable - Ideal for paddy cultivation"
        elif temperature >= 25 and rainfall >= 150 and humidity >= 80:
            return 'Jute', "Highly Suitable - Perfect for jute cultivation"
        elif 18 <= temperature <= 25 and rainfall >= 200 and pH <= 5.5:
            return 'Tea', "Highly Suitable - Ideal tea growing conditions"
        elif temperature <= 20 and P >= 30 and K >= 40:
            return 'Potato', "Highly Suitable - Good for potato cultivation"
        elif rainfall <= 100 and 60 <= N <= 75 and temperature >= 25:
            return 'Pulses', "Highly Suitable - Ideal for pulse crops"
        else:
            return 'Rice', "Moderately Suitable - Default East India staple"

    def get_central_india_crop(temperature, rainfall, N, P, pH, K, humidity):
        st.sidebar.info("🔍 Applying Central India rules...")
        if 22 <= temperature <= 30 and 80 <= rainfall <= 120 and P >= 25:
            return 'Soybean', "Highly Suitable - Ideal for soybean cultivation"
        elif temperature <= 22 and N >= 75 and P >= 30:
            return 'Wheat', "Highly Suitable - Good wheat growing conditions"
        elif rainfall <= 90 and 60 <= N <= 75 and temperature >= 25:
            return 'Pulses', "Highly Suitable - Ideal for pulse crops"
        elif 25 <= temperature <= 32 and rainfall <= 100 and P >= 20:
            return 'Oilseeds', "Highly Suitable - Good for oilseed crops"
        elif 70 <= N <= 85 and 35 <= P <= 45 and 100 <= rainfall <= 140:
            return 'Maize', "Highly Suitable - Ideal maize conditions"
        else:
            return 'Soybean', "Moderately Suitable - Default Central India crop"

    def get_region_crops(region):
        region_crops = {
            'north': ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"],
            'west': ["Cotton", "Sugarcane", "Mango", "Groundnut", "Sorghum"],
            'south': ["Rice", "Coconut", "Coffee", "Tea", "Spices"],
            'east': ["Rice", "Jute", "Tea", "Potato", "Pulses"],
            'central': ["Soybean", "Wheat", "Pulses", "Oilseeds", "Maize"]
        }
        return region_crops.get(region, ["Multiple crops"])

    def get_region_name(region):
        region_names = {
            'north': "North India",
            'west': "West India", 
            'south': "South India",
            'east': "East India",
            'central': "Central India"
        }
        return region_names.get(region, "India")
    
    # Detect region and display information
    region = detect_region_strict(temperature, rainfall, humidity)
    region_name = get_region_name(region)
    common_crops = get_region_crops(region)
    
    st.header("📍 Detected Region Information")
    st.write(f"**Region:** {region_name}")
    st.write(f"**Common crops in this region:** {', '.join(common_crops)}")
    
    st.markdown("---")
    
    # Recommendation Button
    if st.button("**Get Crop Recommendation**", type="primary", use_container_width=True):
        # Get crop recommendation based on region
        if region == 'north':
            crop, reason = get_north_india_crop(temperature, rainfall, N, P, pH, K, humidity)
        elif region == 'west':
            crop, reason = get_west_india_crop(temperature, rainfall, N, P, pH, K, humidity)
        elif region == 'south':
            crop, reason = get_south_india_crop(temperature, rainfall, N, P, pH, K, humidity)
        elif region == 'east':
            crop, reason = get_east_india_crop(temperature, rainfall, N, P, pH, K, humidity)
        elif region == 'central':
            crop, reason = get_central_india_crop(temperature, rainfall, N, P, pH, K, humidity)
        else:
            crop, reason = "Multiple Crops", "Consult local agricultural expert"
        
        # Display recommendation
        st.success(f"**Recommended Crop:** {crop}")
        from services.smart_diary import save_crop_history
        from datetime import datetime

        prediction = f"Recommended crop based on inputs"

        save_crop_history({
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "nitrogen": N,
    "phosphorus": P,
    "potassium": K,
    "pH": pH,
    "rainfall": rainfall,
    "temperature": temperature,
    "humidity": humidity,
    "prediction": prediction
})



        st.info(f"**Reason:** {reason}")
        
        # Show additional insights
        with st.expander("📈 Regional Farming Insights"):
            insights = {
                'north': """
                **North India Farming Insights:**
                • Ideal for wheat-rice rotation systems
                • Suitable for maize and cotton cultivation  
                • Monitor water usage during dry seasons
                • Good for sugarcane in suitable areas
                """,
                'west': """
                **West India Farming Insights:**
                • Perfect for cash crops like cotton and sugarcane
                • Excellent for horticulture (mangoes, fruits)
                • Water conservation practices recommended
                • Good for drought-resistant crops like sorghum
                """,
                'south': """
                **South India Farming Insights:**
                • Excellent for plantation crops (coffee, tea, spices)
                • Ideal for coconut and rubber cultivation
                • High rainfall supports multiple paddy seasons
                • Good for horticulture and floriculture
                """,
                'east': """
                **East India Farming Insights:**
                • Traditional paddy cultivation area
                • Suitable for jute and tea plantations  
                • Rich alluvial soil benefits multiple crops
                • Good for potato and vegetable cultivation
                """,
                'central': """
                **Central India Farming Insights:**
                • Major soybean and pulses growing region
                • Suitable for oilseed cultivation
                • Balanced climate for diverse crops
                • Good for wheat and maize cultivation
                """
            }
            st.write(insights.get(region, "Consult local agricultural authorities for specific guidance."))

# Fertilizer Recommendation Page
def fertilizer_recommendation_page():
    st.title("💧 Smart Fertilizer Recommendation")
    st.markdown("Get precise fertilizer recommendations for your crops")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Crop Information")
        crop_type = st.selectbox(
            "Select Your Crop",
            ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Pulses", "Oilseeds", "Vegetables", "Fruits"]
        )
        
        growth_stage = st.selectbox(
            "Growth Stage",
            ["Pre-sowing", "Seedling", "Vegetative", "Flowering", "Fruiting", "Maturity"]
        )
        
        st.subheader("Soil Test Results")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            current_N = st.slider("Current Nitrogen (kg/ha)", 0, 200, 50)
        with col4:
            current_P = st.slider("Current Phosphorus (kg/ha)", 0, 100, 25)
        with col5:
            current_K = st.slider("Current Potassium (kg/ha)", 0, 150, 30)
        
        soil_type = st.selectbox(
            "Soil Type",
            ["Sandy", "Loamy", "Clayey", "Sandy Loam", "Clay Loam"]
        )
        
        if st.button("Get Fertilizer Recommendation", type="primary"):

            # Simple fertilizer calculation logic
            if crop_type == "Rice":
                N_req = 120 - current_N
                P_req = 60 - current_P
                K_req = 60 - current_K
            elif crop_type == "Wheat":
                N_req = 100 - current_N
                P_req = 50 - current_P
                K_req = 40 - current_K
            elif crop_type == "Cotton":
                N_req = 150 - current_N
                P_req = 70 - current_P
                K_req = 80 - current_K
            else:
                N_req = 80 - current_N
                P_req = 40 - current_P
                K_req = 40 - current_K

            # ✅ Create actual recommendation text
            recommendation_text = f"""
Nitrogen (N): {max(0, N_req)} kg/ha
Phosphorus (P₂O₅): {max(0, P_req)} kg/ha
Potassium (K₂O): {max(0, K_req)} kg/ha

Application Advice:
• Split nitrogen application in 2–3 doses
• Apply phosphorus as basal dose
• Potassium can be applied in splits for long-duration crops
""".strip()

            # ✅ Display on UI
            st.success("**Fertilizer Recommendation:**")
            st.info(recommendation_text)

            # ✅ Save to DB
            from services.smart_diary import save_fertilizer_history
            save_fertilizer_history({
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "crop_name": crop_type,
    "soil_type": soil_type,
    "nitrogen": current_N,
    "phosphorus": current_P,
    "potassium": current_K,
    "recommendation": recommendation_text
})



    with col2:
        st.image(
            "https://cdn.pixabay.com/photo/2018/10/30/16/06/fertilizer-3784224_1280.jpg",
            caption="Right Fertilizer, Right Time"
        )
        
        st.markdown("""
        ### 💡 Tips for Better Results
        
        • Test soil every season  
        • Use organic manure along with fertilizers  
        • Follow proper irrigation schedule  
        • Monitor crop health regularly  
        """)


# Weather Page with API
def weather_page():
    st.title("🌤️ Real-Time Weather & Forecast")
    st.markdown("Get current weather conditions and forecasts for your location")
    
    # Weather API integration (using OpenWeatherMap as example)
    col1, col2 = st.columns([2, 1])
    weather_data = None
    
    with col1:
        st.subheader("Location Details")
        city = st.text_input("Enter City Name", "Delhi")
                
        if st.button("Get Weather Information", type="primary"):
            try:
                import sys
                import os
                # Add the backend services directory to Python path
                sys.path.append(r"C:\Users\Hp\Documents\KrishiSathi\backend\services")
                from weather_service import get_weather
            except ImportError as e:
                st.error(f"Could not import weather service: {e}")
                return
            
            try:                
                weather_data = get_weather(city)
                
                if "error" in weather_data:
                    st.error(f"Could not fetch weather data: {weather_data['error']}")
                    st.info("**Demo weather data shown**")
                    
                    # Show demo data as fallback
                    show_demo_weather(city)
                else:
                    st.success(f"Weather information for {city}")
                    
                    col3, col4, col5 = st.columns(3)
                    
                    with col3:
                        st.metric("Temperature", f"{weather_data['temperature']}°C")
                    with col4:
                        st.metric("Humidity", f"{weather_data['humidity']}%")
                    with col5:
                        st.metric("Rainfall", f"{weather_data.get('rainfall', 0)} mm")
                    
                    st.info(f"**Temperature:** {weather_data['temperature']}°C")
                    st.info(f"**Humidity:** {weather_data['humidity']}%")
                    st.info(f"**Rainfall:** {weather_data.get('rainfall', 0)} mm")
                    
            except Exception as e:
                st.error(f"Error fetching weather data: {e}")
                st.info("**Demo weather data shown**")
                show_demo_weather(city)
    
    with col2:
        st.subheader("Weather Alerts")
    
        # Always show content - no blank space
        if weather_data and isinstance(weather_data, dict) and "temperature" in weather_data:
            # DYNAMIC CONTENT - when we have real weather data
            temp = weather_data['temperature']
            humidity = weather_data['humidity']
            rainfall = weather_data.get('rainfall', 0)
        
            # Temperature alerts
            if temp > 35:
                st.error("🔥 **Heat Alert**\n\nHigh temperature risk for crops")
            elif temp < 10:
                st.warning("❄️ **Cold Alert**\n\nLow temperature may affect growth")
            else:
                st.success("🌡️ **Temperature**\n\nIdeal for crop growth")
        
            # Rainfall alerts
            if rainfall > 20:
                st.warning("🌧️ **Heavy Rain Alert**\n\nPotential flooding risk")
            elif rainfall > 5:
                st.info("🌦️ **Rain Alert**\n\nLight to moderate showers expected")
            else:
                st.info("☀️ **Dry Conditions**\n\nNo rainfall expected")
        
            # Humidity alerts
            if humidity > 80:
                st.warning("💧 **High Humidity**\n\nIncreased fungal disease risk")
            elif humidity < 40:
                st.warning("🏜️ **Low Humidity**\n\nPlants may need more water")
            else:
                st.success("💨 **Humidity**\n\nOptimal for plant health")
            
        else:
            # STATIC CONTENT - always show this when no real data (including first load)
            st.warning("🌧️ **Rain Alert**\n\nLight showers expected in next 24 hours")
            st.info("🌡️ **Temperature**\n\nIdeal for crop growth")
            st.success("💨 **Wind Conditions**\n\nNormal wind speed")
    
        st.markdown("---")
        st.subheader("Farming Suggestions")
    
    # Always show farming suggestions
        if weather_data and isinstance(weather_data, dict) and "temperature" in weather_data:
            # DYNAMIC SUGGESTIONS
            temp = weather_data['temperature']
            humidity = weather_data['humidity']
            rainfall = weather_data.get('rainfall', 0)
        
            suggestions = []
        
            if temp > 30:
                suggestions.extend([
                    "• Water crops in early morning/late evening",
                    "• Use shade nets for sensitive crops"
                ])
            elif temp < 15:
                suggestions.extend([
                    "• Protect seedlings from cold stress",
                    "• Consider greenhouse cultivation"
                ])
        
            if rainfall > 15:
                suggestions.extend([
                    "• Delay irrigation to save water", 
                    "• Check field drainage systems"
                ])
            elif rainfall == 0:
                suggestions.extend([
                    "• Schedule regular irrigation",
                    "• Use mulch to conserve moisture"
                ])
        
            # Always include these general suggestions
            suggestions.extend([
                "• Monitor for pest activities",
                "• Continue regular farming activities",
                "• Check soil moisture regularly"
            ])
        
            for suggestion in suggestions:
                st.write(suggestion)
            
        else:
            # STATIC SUGGESTIONS - always show when no real data
            st.write("• Good time for irrigation")
            st.write("• Suitable for fertilizer application") 
            st.write("• Monitor for pest activities")
            st.write("• Continue regular farming activities")
            st.write("• Check weather forecast regularly")
            
# ADDED: Helper function for demo data
def show_demo_weather(city):
    """Display demo weather data when API fails"""
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("Temperature", "28°C")
    with col4:
        st.metric("Humidity", "65%")
    with col5:
        st.metric("Rainfall", "0 mm")
    
    st.info("**Conditions:** Partly Cloudy")
    st.info("**Note:** Demo data shown - real weather data unavailable")


#Tensorflow Model prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model(r'C:\Users\Hp\Documents\KrishiSathi\backend\notebooks\trained_disease.keras')
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
    input_arr= tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])   #convert single image to a batch
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

def disease_detection_page():
    st.header("Disease Detection")
    st.markdown("Upload an image of your crop to identify potential diseases and get recommendations.")
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        test_image = st.file_uploader("Choose an Image:", type=['jpg', 'jpeg', 'png'])
        # Display image preview
        if test_image is not None:
            st.subheader("📸 Image Preview")
            image = Image.open(test_image)
            st.image(image, use_container_width=True, caption="Uploaded Image")
            
    with col2:
        if test_image is not None:
            # Prediction section with better styling
            st.subheader("🔍 Analysis Results")
            
            # Add a loading spinner for better UX
            if st.button("🔮 Predict Disease", type="primary", use_container_width=True):
                with st.spinner("Analyzing image... This may take a few seconds."):
                    result_index = model_prediction(test_image)
                #Define class
                class_name = ['Apple_Apple_scab',
 'Apple_Black_rot',
 'Apple_Cedar_apple_rust',
 'Apple_healthy',
 'Blueberry_healthy',
 'Cherry_including_sour_Powdery_mildew',
 'Cherry_including_sour_healthy',
 'Corn_maize_Cercospora_leaf_spot_Gray_leaf_spot',
 'Corn_maize_Common_rust_',
 'Corn_maize_Northern_Leaf_Blight',
 'Corn_maize_healthy',
 'Grape_Black_rot',
 'Grape_Esca_Black_Measles',
 'Grape_Leaf_blight_Isariopsis_Leaf_Spot',
 'Grape_healthy',
 'Orange_Haunglongbing_Citrus_greening',
 'Peach_Bacterial_spot',
 'Peach_healthy',
 'Pepper_bell_Bacterial_spot',
 'Pepper_bell_healthy',
 'Potato_Early_blight',
 'Potato_Late_blight',
 'Potato_healthy',
 'Raspberry_healthy',
 'Soybean_healthy',
 'Squash_Powdery_mildew',
 'Strawberry_Leaf_scorch',
 'Strawberry_healthy',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites_Two-spotted_spider_mite',
 'Tomato_Target_Spot',
 'Tomato_Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato_Tomato_mosaic_virus',
 'Tomato_healthy']
                predicted_disease = class_name[result_index]
                # Display result with appropriate styling
                st.success("✅ **Prediction Complete!**")
                uploaded_image_path = f"uploaded_images/{test_image.name}"
                crop_name = "Tomato"  # (replace dynamically if needed)
                confidence_score = 0.95  # Placeholder confidence score
                

                # Create a nice result card
                with st.container():
                    st.markdown("---")
                    st.subheader("📊 Prediction Result")
                    
                    # Split the class name for better display
                    if "_" in predicted_disease:
                        crop, disease = predicted_disease.split("_", 1)
                        disease = disease.replace("_", " ").title()
                    else:
                        crop = predicted_disease
                        disease = "Healthy"
                    
                    # Display result with icons
                    if "healthy" in predicted_disease.lower():
                        st.success(f"🌱 **Crop:** {crop.replace('_', ' ').title()}")
                        st.success(f"💚 **Status:** {disease}")
                        st.info("🎉 Your crop appears to be healthy! Continue with good farming practices.")
                    else:
                        st.warning(f"🌱 **Crop:** {crop.replace('_', ' ').title()}")
                        st.error(f"⚠️ **Disease Detected:** {disease}")
                        st.warning("🔍 Consider consulting with an agricultural expert for treatment options.")
                    
                    st.markdown("---")
        
        else:
            # Instructions when no image is uploaded
            st.info("👆 **How to use:**")
            st.markdown("""
            1. **Upload** a clear image of your crop leaves
            2. **Preview** the image to ensure quality
            3. **Click Predict** to analyze for diseases
            4. **Review** the results and recommendations
            """)
            
            # Tips for better results
            with st.expander("💡 Tips for better detection"):
                st.markdown("""
                - Use clear, well-lit images
                - Focus on affected leaves/areas
                - Avoid blurry or dark photos
                - Include multiple angles if possible
                - Ensure the plant occupies most of the frame
                """)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick help section
    with st.expander("❓ Need Help?"):
        st.markdown("""
        **Common Questions:**
        - **Accuracy:** Our model is trained on thousands of crop images but may not be 100% accurate
        - **Supported Crops:** Apples, Blueberries, Cherries, Corn, Grapes, Oranges, Peaches, Peppers, Potatoes, and more
        - **Image Requirements:** JPG, JPEG, or PNG format, max 200MB
        - **For serious infections:** Always consult with local agricultural experts
        """)

# Thank You Page
def thank_you_page():
    st.title("🙏 Thank You for Using KrishiSathi!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Your Trust Means Everything to Us!
        
        We're grateful that you chose **KrishiSathi** as your farming companion. 
        Together, we're building a brighter future for Indian agriculture.
        
        ### 📞 Need Help?
        - **Agricultural Experts:** Contact your local Krishi Vigyan Kendra
        - **Technical Support:** support@krishisathi.com
        - **Emergency:** Dial Kisan Call Center - 1551
        
        ### 🔄 Continue Your Journey
        Feel free to explore other features of our app:
        - Get new crop recommendations
        - Check fertilizer requirements  
        - Monitor weather conditions
        - Plan your farming activities
        
        **Happy Farming! 🚜**
        """)
    
    with col2:
        st.image("https://cdn.pixabay.com/photo/2017/09/23/19/33/farmer-2779150_1280.jpg", 
                caption="Together We Grow")
        
        st.balloons()
        
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = "Introduction"

# Main App Logic
def main():
    check_login()
    
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar navigation
    st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
    st.sidebar.markdown("---")
    
    # Page selection
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Introduction"
    
    page = st.sidebar.radio(
        "Navigate to:",
        ["Introduction", "Yield Forecast", "Crop Recommendation", "Fertilizer Recommendation", "Weather", "Disease Detection", "Smart Diary", "Thank You"],
        index=["Introduction", "Yield Forecast", "Crop Recommendation", "Fertilizer Recommendation", "Weather", "Disease Detection", "Smart Diary", "Thank You"].index(st.session_state.current_page)
    )
    
    st.session_state.current_page = page
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    
    
    # Display selected page
    if page == "Introduction":
        introduction_page()
    elif page == "Yield Forecast":
        yield_forecast_page()
    elif page == "Crop Recommendation":
        crop_recommendation_page()
    elif page == "Fertilizer Recommendation":
        fertilizer_recommendation_page()
    elif page == "Weather":
        weather_page()
    elif page == "Disease Detection":
        disease_detection_page()
    elif page == "Smart Diary":
        smart_diary_page()
    elif page == "Thank You":
        thank_you_page()

if __name__ == "__main__":
    main()