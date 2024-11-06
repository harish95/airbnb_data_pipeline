import boto3
from botocore.exceptions import NoCredentialsError, ParamValidationError

def upload_file_to_s3(file_name, bucket_name, object_name=None, aws_access_key_id=None, aws_secret_access_key=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket_name: S3 bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :param aws_access_key_id: AWS access key ID
    :param aws_secret_access_key: AWS secret access key
    :return: True if file was uploaded, else False
    """
    # Validate file existence
    try:
        with open(file_name, 'rb'):
            pass
    except FileNotFoundError:
        print("The specified file does not exist.")
        return False

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Initialize the S3 client with access keys
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File '{file_name}' uploaded to '{bucket_name}/{object_name}'")
        return True
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except ParamValidationError as e:
        print(f"Parameter validation error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

