"""
Quick test for live prediction function
"""

from app import LivePredictionInput, make_live_prediction

def test_prediction():
    """Test live prediction with sample data"""
    
    # Sample forest data
    sample_input = LivePredictionInput(
        elevation=2500,
        aspect=180,
        slope=15,
        horizontal_distance_to_hydrology=250,
        vertical_distance_to_hydrology=30,
        horizontal_distance_to_roadways=1500,
        hillshade_9am=220,
        hillshade_noon=235,
        hillshade_3pm=150,
        horizontal_distance_to_fire_points=800
    )
    
    print("🧪 Testing live prediction...")
    print(f"Input data: {sample_input}")
    
    result = make_live_prediction(sample_input)
    print(f"🎯 Prediction result: {result}")

if __name__ == "__main__":
    test_prediction()
