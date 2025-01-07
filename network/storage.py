from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = ''  # Files will be stored at bucket root
    file_overwrite = False
    default_acl = None 