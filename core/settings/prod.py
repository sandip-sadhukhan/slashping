from .base import *

INSTALLED_APPS  += [
    'storages'
]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_S3_ACCESS_KEY"),
            "secret_key": os.getenv("AWS_S3_SECRET_KEY"),
            "bucket_name": os.getenv("AWS_S3_BUCKET_NAME"),
            "custom_domain": f"{os.getenv("AWS_S3_BUCKET_NAME")}.s3.amazonaws.com",
            "file_overwrite": False,
            "location": "media",
        },
    },
    'staticfiles': {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_S3_ACCESS_KEY"),
            "secret_key": os.getenv("AWS_S3_SECRET_KEY"),
            "bucket_name": os.getenv("AWS_S3_BUCKET_NAME"),
            "custom_domain": f"{os.getenv("AWS_S3_BUCKET_NAME")}.s3.amazonaws.com",
            "file_overwrite": False,
            "location": "static",
        },
    },
}
