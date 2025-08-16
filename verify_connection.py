import sys
import os
from src.forest.components.data_ingestion import DataIngestion
from src.forest.entity.config_entity import DataIngestionConfig

def test_data_ingestion():
    """Test the data ingestion pipeline"""
    try:
        print("🔍 Starting data ingestion verification...")
        
        # Initialize configuration
        config = DataIngestionConfig()
        print(f"✅ Configuration loaded")
        
        # Create data ingestion instance
        data_ingestion = DataIngestion(data_ingestion_config=config)
        print(f"✅ DataIngestion instance created")
        
        # Run the full pipeline
        artifact = data_ingestion.initiate_data_ingestion()
        
        print("\n🎉 Data ingestion completed successfully!")
        print(f"📁 Training file: {artifact.trained_file_path}")
        print(f"📁 Test file: {artifact.test_file_path}")
        
        # Verify files exist
        if os.path.exists(artifact.trained_file_path):
            print("✅ Training file created successfully")
        else:
            print("❌ Training file not found")
            
        if os.path.exists(artifact.test_file_path):
            print("✅ Test file created successfully")
        else:
            print("❌ Test file not found")
            
        return True
        
    except Exception as e:
        print(f"❌ Data ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_ingestion()
    sys.exit(0 if success else 1)
