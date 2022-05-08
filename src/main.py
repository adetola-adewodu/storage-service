import os

import requests
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, File, Response, UploadFile, status
from fastapi.responses import JSONResponse
from loguru import logger


app = FastAPI(
    title="Storage Service",
    description="Demonstrates procedures that can be used to access AWS S3 bucket",
    version="0.0.1"
)
load_dotenv()

OBJECT_BUCKET = os.getenv('S3_BUCKET_NAME')

@app.get("/", summary="Checks if API is running", description="returns a message to make sure service is up and running")
def read_root():
    return {"Data Query Service": "Running"}

# def get_s3_object():
#     try:
#         session = boto3.Session(
#             aws_access_key_id=os.getenv('AWS_ID'),
#             aws_secret_access_key=os.getenv('AWS_KEY')
#         )
#         return session.resource('s3')
#     except ConfigNotFound as cnf:
#         logger.error(cnf)
#         return Response(cnf)
#     except ClientError as ce:
#         logger.error(ce)
#         return Response(ce)

# @app.post("/write/", tags=["custom path"], summary="Write a file to a s3 bucket", description="Write a file to a s3 bucket")
# async def write(file: UploadFile = File(...)):
#     data = None
#     file_name = file.filename
#     s3 = get_s3_object()
#     try:
#         s3_object = s3.Object(OBJECT_BUCKET, 'inbox/'+file_name)
#         data = await file.read()
#         if data:
#             s3_object.put(Body=data)
#     except ClientError as e:
#         FILE_NAME_ERROR = "/write file-name{} could not write to S3 \n".format(file_name)
#         logger.error(FILE_NAME_ERROR, e)
#         return Response(FILE_NAME_ERROR, status_code=status.HTTP_400_BAD_REQUEST)

#     return Response(
#         status_code=status.HTTP_201_CREATED,
#         content="/write {} successfully written to S3".format(file.filename)
#     )

@app.get("/show/", 
    summary="Return shows the file given the s3 file path", description="Returns s3file data for a given the s3 file path")
def read(s3file: str):
    bucket, key = get_bucket_and_key(s3file)
    try:      
        s3_response = get_presigned_url_response(bucket, key)
    except Exception as e:
        logger.error(e)
        logger.error("Problem reading file from S3")
        return JSONResponse(status_code=500, content="Problem reading file from S3")
    return Response(
        status_code=200,
        content=s3_response.content
    )

# Return s3 presigned url given a bucket and key
def get_presigned_url_response(bucket: str, key: str): 
    url = get_created_presigned_url(bucket, key)
    return requests.get(url)

# Return s3 presigned url given a bucket and key
def get_created_presigned_url(bucket: str, key: str): 
    s3_client = boto3.client('s3')
    url = s3_client.generate_presigned_url('get_object', 
            Params={'Bucket': bucket, 'Key': key})
    logger.info(url)
    return url

def get_bucket_and_key(s3file):
    file = s3file.replace("s3://", "").split("/")
    bucket = file[0]
    key = "/".join(file[1:])
    return bucket,key

@app.get("/presigned/", 
    summary="Return presigned url for a given the s3 file path", description="Return presigned url for a given the s3 file path")
def get_presigned_url(s3file: str):
    bucket, key = get_bucket_and_key(s3file)
    url = get_created_presigned_url(bucket, key)
    
    return JSONResponse(status_code=200, content={"url": url})
