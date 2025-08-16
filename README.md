# GreenCanopy AI 

Welcome to **GreenCanopy**, an intelligent machine learning application designed to predict forest cover types based on environmental parameters.

## Description
GreenCanopy leverages satellite and geographical data to classify forest cover types such as Spruce/Fir, Lodgepole Pine, Ponderosa Pine, and more. This solution supports batch predictions and real-time live predictions through an easy-to-use web interface.

## Features
- Train models on real forest data
- Batch prediction with storage on AWS S3
- Live prediction with instant results
- Containerized with Docker for easy deployment
- Responsive UI with Bootstrap for a modern look

## Technologies Used
- Python (FastAPI, Scikit-learn, Pandas, Numpy)
- AWS S3 for model storage
- MongoDB Atlas for data storage
- Docker for containerization

## How to Run

1. Clone the repository
2. Build the Docker image:
   ```
docker build -t forest-cover-app .
```
3. Run the container:
   ```
docker run -p 8080:80 --env-file .env forest-cover-app
```
4. Open your browser at `http://localhost:8080`

## Deployment
This project can be deployed easily on Render.com. Follow their instructions to link your GitHub repository and get your app running online.

## Environment Variables
Use a `.env` file to store your environment variables:

```
PORT=80
AWS_DEFAULT_REGION=eu-north-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
MONGODB_URL=your_mongodb_connection_string
```

## License
This project is open-source and free to use.
