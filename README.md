# storage-service

# create .env
1. Create .env file
2. Add `S3_BUCKET_NAME = '[your bucket name]'`

# export AWS environment varibles 
1. set up local environment variables, either by running `export` command or adding permanently to bash/zsh profile (preferred)
    - `export AWS_SECRET_ACCESS_KEY=<aws-secret-key>`
    - `export AWS_ACCESS_KEY_ID=<aws-id>`

## Initial Run
1. `python3 -m venv env`
2. `source env/bin/activate`
3. `python -m pip install --upgrade pip`
4. `pip install -r requirements.txt`
5. `python -m uvicorn src.main:app --reload`