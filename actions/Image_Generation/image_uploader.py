#%%
import boto3
import os
def upload(access_key, secret_access_key):
    client = boto3.client('s3',
                            aws_access_key_id = access_key,
                            aws_secret_access_key = secret_access_key)

    for file in os.listdir(f'{os.getcwd()}/actions/Image_Generation/Graphs'):
        with open(f"{f'{os.getcwd()}/actions/Image_Generation/Graphs/' + str(file)}", "rb") as f:
            upload_file_bucket = 'rasa-project-image-holder'
            upload_file_key = 'Graphs/' + str(file)
            client.upload_fileobj(f, Bucket= upload_file_bucket,Key= upload_file_key, ExtraArgs={'ACL':'public-read', 'ContentType':'image/jpg'})
