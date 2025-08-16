"""
Verification script to check model requirements and test prediction
"""

import boto3
import tempfile
import os
import pandas as pd
import numpy as np
from src.forest.utils.main_utils import load_object

def verify_model_features():
    """Verify what features the model expects"""
    try:
        print("🔍 Starting model feature verification...")
        
        # Connect to S3 and download model
        s3_client = boto3.client('s3', region_name='eu-north-1')
        response = s3_client.list_objects_v2(Bucket="shayanforest")
        
        model_key = None
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                if '.pkl' in key and 'model' in key.lower():
                    model_key = key
                    break
        
        if not model_key:
            print("❌ No model file found in S3")
            return False
        
        print(f"✅ Found model at: {model_key}")
        
        # Download model
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
        temp_file.close()
        temp_model_path = temp_file.name
        s3_client.download_file("shayanforest", model_key, temp_model_path)
        
        # Load model and inspect
        model = load_object(temp_model_path)
        print(f"✅ Model loaded successfully")
        
        # Check model properties
        if hasattr(model, 'n_features_in_'):
            print(f"📊 Model expects {model.n_features_in_} features")
        
        if hasattr(model, 'feature_names_in_'):
            print(f"📋 Expected feature names: {list(model.feature_names_in_)}")
        
        # Test with sample training data structure
        print("\n🧪 Testing with complete feature set...")
        
        # Create sample data with all features
        sample_data = {
            'Id': 999999,
            'Elevation': 2500,
            'Aspect': 180,
            'Slope': 15,
            'Horizontal_Distance_To_Hydrology': 250,
            'Vertical_Distance_To_Hydrology': 30,
            'Horizontal_Distance_To_Roadways': 1500,
            'Hillshade_9am': 220,
            'Hillshade_Noon': 235,
            'Hillshade_3pm': 150,
            'Horizontal_Distance_To_Fire_Points': 800
        }
        for i in range(1, 5):
            sample_data[f'Wilderness_Area{i}'] = 0
        
        # Add all soil type features
        for i in range(1, 41):
            sample_data[f'Soil_Type{i}'] = 0
        
        # Add wilderness area features
        
        
        # Create DataFrame
        sample_df = pd.DataFrame([sample_data])
        print(f"📏 Created sample DataFrame with shape: {sample_df.shape}")
        
        # Apply same preprocessing as training
        columns_to_drop = ['Soil_Type7', 'Soil_Type8', 'Soil_Type15', 'Soil_Type36']
        for col in columns_to_drop:
            if col in sample_df.columns:
                sample_df = sample_df.drop(col, axis=1)
        
        print(f"📏 After dropping columns, shape: {sample_df.shape}")
        print(f"📋 Final columns: {list(sample_df.columns)}")
        
        # Test prediction
        features = sample_df.values
        prediction = model.predict(sample_df)
        
        cover_types = {
            1: "Spruce/Fir", 2: "Lodgepole Pine", 3: "Ponderosa Pine",
            4: "Cottonwood/Willow", 5: "Aspen", 6: "Douglas-fir", 7: "Krummholz"
        }
        
        cover_type = cover_types.get(int(prediction), f"Unknown ({prediction})")
        print(f"🎯 Test prediction successful: {cover_type}")
        
        # Clean up
        os.unlink(temp_model_path)
        
        print("\n✅ Verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_training_data_schema():
    """Test the actual training data schema"""
    try:
        print("\n🔍 Checking training data schema...")
        
        from src.forest.data_access.forest_data import ForestData
        
        # Get sample from training data
        forest_data = ForestData()
        df = forest_data.export_collection_as_dataframe(collection_name="forest")
        
        print(f"📊 Training data shape: {df.shape}")
        print(f"📋 Training data columns: {list(df.columns)}")
        
        # Apply same preprocessing
        cols_to_drop = ['Soil_Type7', 'Soil_Type8', 'Soil_Type15', 'Soil_Type36']
        existing_cols = [col for col in cols_to_drop if col in df.columns]
        if existing_cols:
            df = df.drop(existing_cols, axis=1)
        
        print(f"📏 After preprocessing shape: {df.shape}")
        print(f"📋 Final training columns: {list(df.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Training data check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Forest Cover Model Verification")
    print("=" * 50)
    
    # Verify model features
    model_ok = verify_model_features()
    
    # Check training data schema
    training_ok = test_training_data_schema()
    
    print("\n" + "=" * 50)
    if model_ok and training_ok:
        print("🎉 All verifications passed! Your model should work correctly.")
    else:
        print("❌ Some verifications failed. Check the errors above.")
