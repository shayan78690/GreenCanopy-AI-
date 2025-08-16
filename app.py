from fastapi import FastAPI, Request, Form
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, HTMLResponse
from pydantic import BaseModel

from src.forest.constant.application import APP_HOST, APP_PORT
from src.forest.pipeline.train_pipeline import TrainPipeline
from src.forest.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()
TEMPLATES = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount static files for serving CSS, JS, and images
origins = ["*"]

# This is to allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for live prediction input
class LivePredictionInput(BaseModel):
    elevation: float
    aspect: float
    slope: float
    horizontal_distance_to_hydrology: float
    vertical_distance_to_hydrology: float
    horizontal_distance_to_roadways: float
    hillshade_9am: float
    hillshade_noon: float
    hillshade_3pm: float
    horizontal_distance_to_fire_points: float

# ✅ YOUR ORIGINAL ROUTES (UNCHANGED)
@app.get("/", status_code=200, response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def index(request: Request):
    return TEMPLATES.TemplateResponse(name='index.html', context={"request": request, "prediction": None})

@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("<h1>Training successful !!<h1>")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predictRouteClient():
    try:
        prediction_pipeline = PredictionPipeline()
        prediction_pipeline.initiate_prediction()
        return Response(
            "<h1>Prediction successful and predictions are stored in s3 bucket !!<h1>"
        )
    except Exception as e:
        return Response(f"Error Occurred! {e}")

# ✅ NEW LIVE PREDICTION ROUTE (ADDED)
@app.post("/predict_live", response_class=HTMLResponse)
async def predict_live(
    request: Request,
    elevation: float = Form(...),
    aspect: float = Form(...),
    slope: float = Form(...),
    horizontal_distance_to_hydrology: float = Form(...),
    vertical_distance_to_hydrology: float = Form(...),
    horizontal_distance_to_roadways: float = Form(...),
    hillshade_9am: float = Form(...),
    hillshade_noon: float = Form(...),
    hillshade_3pm: float = Form(...),
    horizontal_distance_to_fire_points: float = Form(...)
):
    try:
        # Create input data for your model
        input_data = LivePredictionInput(
            elevation=elevation,
            aspect=aspect,
            slope=slope,
            horizontal_distance_to_hydrology=horizontal_distance_to_hydrology,
            vertical_distance_to_hydrology=vertical_distance_to_hydrology,
            horizontal_distance_to_roadways=horizontal_distance_to_roadways,
            hillshade_9am=hillshade_9am,
            hillshade_noon=hillshade_noon,
            hillshade_3pm=hillshade_3pm,
            horizontal_distance_to_fire_points=horizontal_distance_to_fire_points
        )
        
        # Make live prediction
        prediction_result = make_live_prediction(input_data)
        
        return TEMPLATES.TemplateResponse("index.html", {
            "request": request, 
            "prediction": prediction_result
        })
        
    except Exception as e:
        return TEMPLATES.TemplateResponse("index.html", {
            "request": request, 
            "prediction": f"Error: {str(e)}"
        })

def make_live_prediction(input_data: LivePredictionInput):
    """
    Make live prediction using your trained model from S3 with pandas DataFrame
    """
    try:
        import boto3
        import tempfile
        import os
        import pandas as pd
        from src.forest.utils.main_utils import load_object
        import numpy as np
        
        # Create S3 client
        s3_client = boto3.client('s3', region_name='eu-north-1')
        
        # Find and download model from S3
        response = s3_client.list_objects_v2(Bucket="shayanforest")
        model_key = None
        
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                if '.pkl' in key and 'model' in key.lower():
                    model_key = key
                    break
        
        if not model_key:
            return "No model file found in S3 bucket shayanforest"
        
        # Download model
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
        temp_file.close()
        temp_model_path = temp_file.name
        s3_client.download_file("shayanforest", model_key, temp_model_path)
        
        try:
            # Load the model
            model = load_object(temp_model_path)
            
            # Create complete feature vector with all expected columns
            feature_dict = {
                'Id': 999999,  # Dummy ID for prediction
                'Elevation': input_data.elevation,
                'Aspect': input_data.aspect,
                'Slope': input_data.slope,
                'Horizontal_Distance_To_Hydrology': input_data.horizontal_distance_to_hydrology,
                'Vertical_Distance_To_Hydrology': input_data.vertical_distance_to_hydrology,
                'Horizontal_Distance_To_Roadways': input_data.horizontal_distance_to_roadways,
                'Hillshade_9am': input_data.hillshade_9am,
                'Hillshade_Noon': input_data.hillshade_noon,
                'Hillshade_3pm': input_data.hillshade_3pm,
                'Horizontal_Distance_To_Fire_Points': input_data.horizontal_distance_to_fire_points
            }
            
            # Add all 4 Wilderness Area features
            for i in range(1, 5):
                feature_dict[f'Wilderness_Area{i}'] = 0
            
            # Add all 40 Soil Type features
            for i in range(1, 41):
                feature_dict[f'Soil_Type{i}'] = 0
            
            # Create DataFrame
            input_df = pd.DataFrame([feature_dict])
            
            # Remove the columns that were dropped during training
            columns_to_drop = ['Soil_Type7', 'Soil_Type8', 'Soil_Type15', 'Soil_Type36']
            for col in columns_to_drop:
                if col in input_df.columns:
                    input_df = input_df.drop(col, axis=1)
            
            print(f"Input DataFrame shape: {input_df.shape}")
            print(f"Columns: {list(input_df.columns)}")
            
            # ✅ FIXED: Pass DataFrame directly to model.predict() - NOT numpy array
            prediction = model.predict(input_df)[0]
            
            # Map prediction to cover type name
            cover_types = {
                1: "Spruce/Fir",
                2: "Lodgepole Pine", 
                3: "Ponderosa Pine",
                4: "Cottonwood/Willow",
                5: "Aspen",
                6: "Douglas-fir",
                7: "Krummholz"
            }
            
            cover_type_name = cover_types.get(int(prediction), f"Unknown Type ({prediction})")
            return f"🌲 {cover_type_name} (Cover Type {int(prediction)})"
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_model_path):
                try:
                    os.unlink(temp_model_path)
                except Exception as e:
                    print(f"Warning: Could not delete temp file {temp_model_path}: {e}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Prediction failed: {str(e)}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 80))
    uvicorn.run(app, host="0.0.0.0", port=port)

