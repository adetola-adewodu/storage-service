from fastapi import FastAPI

app = FastAPI(
    title="Storage Service",
    description="Demonstrates procedures that can be used to access AWS S3 bucket",
    version="0.0.1"
)

@app.get("/", summary="Checks if API is running", description="returns a message to make sure service is up and running")
def read_root():
    return {"Data Query Service": "Running"}