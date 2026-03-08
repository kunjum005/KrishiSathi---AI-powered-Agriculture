
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


# Load enhanced model and encoder
model = joblib.load("C:\\Users\\Hp\\Documents\\KrishiSathi\\backend\\models\\crop_xgboost_enhanced.pkl")
le = joblib.load("C:\\Users\\Hp\\Documents\\KrishiSathi\\backend\\models\\label_encoder_enhanced.pkl")

def recommend_crop(N, P, K, temperature, humidity, ph, rainfall):
    """
    Recommend crop using enhanced model with geographical awareness
    """
    # Add regional features automatically
    is_north_india = 1 if (15 <= temperature <= 30 and rainfall <= 250 and ph >= 6.5) else 0
    is_south_india = 1 if (temperature >= 25 and rainfall >= 200 and humidity >= 70) else 0
    is_west_india = 1 if (temperature >= 28 and rainfall <= 150) else 0
    is_east_india = 1 if (humidity >= 75 and rainfall >= 250) else 0
    
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall, 
                         is_north_india, is_south_india, is_west_india, is_east_india]])
    
    prediction = model.predict(features)
    crop_name = le.inverse_transform(prediction)[0]
    
    return crop_name

def test_enhanced_service():
    """Test the enhanced service with problematic cases"""
    test_cases = [
        (75, 35, 45, 30, 60, 7.5, 100),  # Should be cotton
        (95, 48, 50, 26, 72, 7.1, 180),  # Should be sugarcane  
        (80, 38, 42, 25, 70, 7.0, 150),  # Should be maize
        (90, 42, 43, 20.5, 80, 6.5, 200), # Should be rice
    ]
    
    print("🧪 Enhanced Service Test Results:")
    print("=" * 45)
    for i, params in enumerate(test_cases, 1):
        crop = recommend_crop(*params)
        print(f"Test {i}: {params[:3]}... → {crop}")
    
    return True

if __name__ == "__main__":
    # Run tests
    test_enhanced_service()
    
    # Example usage
    crop = recommend_crop(90, 42, 43, 20.5, 80, 6.5, 200)
    print(f"\n🌾 Example Recommendation: {crop}")
