from azure.storage.blob import BlobServiceClient
import string, random

class AzureBlobStorageManager:
    def __init__(self, sas_token: str, account_url: str):
        self.blob_service_client = BlobServiceClient(account_url, credential=sas_token)


    def upload_blob_stream(self, container_name: str, file):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        return blob_client.upload_blob(file, blob_type="BlockBlob")
    
    def does_blob_exist(self, container_name, blob_name):
        container_client = self.blob_service_client.get_container_client(container_name)

        try:
            blob_client = container_client.get_blob_client(blob_name)
            properties = blob_client.get_blob_properties()
            return True  # Blob exists
        except Exception as e:
            if "BlobNotFound" in str(e):
                return False  # Blob does not exist
            else:
                raise  # Other error

    def generate_random_filename(self, lenght, filename):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=lenght)) + filename
    
    
