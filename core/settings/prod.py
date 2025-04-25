from .base import *

INSTALLED_APPS  += [
    'storages'
]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_ACCESS_KEY"),
            "secret_key": os.getenv("AWS_SECRET_KEY"),
            "bucket_name": os.getenv("AWS_S3_BUCKET_NAME"),
            "custom_domain": f"{os.getenv("AWS_S3_BUCKET_NAME")}.s3.amazonaws.com",
            "file_overwrite": False,
            "location": "media",
        },
    },
    'staticfiles': {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_ACCESS_KEY"),
            "secret_key": os.getenv("AWS_SECRET_KEY"),
            "bucket_name": os.getenv("AWS_S3_BUCKET_NAME"),
            "custom_domain": f"{os.getenv("AWS_S3_BUCKET_NAME")}.s3.amazonaws.com",
            "file_overwrite": False,
            "location": "static",
        },
    },
}

# Email Config
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SES_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_SES_REGION_NAME = os.getenv("AWS_SES_REGION_NAME")
AWS_SES_REGION_ENDPOINT = os.getenv("AWS_SES_REGION_ENDPOINT")
