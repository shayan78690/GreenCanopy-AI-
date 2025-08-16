from src.forest.data_access.forest_data import ForestData
from src.forest.configuration.mongo_db_connection import MongoDBClient
def check_mongodb_data():
    try:
        # Check database connection
        client = MongoDBClient()
        database = client.database
        
        print(f"✅ Connected to database: {client.database_name}")
        
        # List all collections
        collections = database.list_collection_names()
        print(f"📁 Available collections: {collections}")
        
        # Check each collection's document count
        for collection_name in collections:
            collection = database[collection_name]
            count = collection.count_documents({})
            print(f"📊 Collection '{collection_name}': {count} documents")
        
        # Test ForestData export
        forest_data = ForestData()
        
        # Try with first available collection
        if collections:
            test_collection = collections[0]
            print(f"\n🔍 Testing ForestData with collection: {test_collection}")
            df = forest_data.export_collection_as_dataframe(collection_name=test_collection)
            print(f"✅ ForestData export successful! Shape: {df.shape}")
        else:
            print("❌ No collections found in database")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_mongodb_data()
