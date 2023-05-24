from botocore.exceptions import ClientError
from django.core.exceptions import ValidationError
from django_social.settings import s3

from aws.config import AWS_STORAGE_BUCKET_NAME


def upload_image(request, serializer, field_name: str, field_storage_name: str) -> None:
    image = request.FILES.get(field_name)
    if image:
        file_format = image.content_type.split('/')[-1].lower()
        allowed_formats = ['png', 'svg', 'jpeg', 'jpg']
        if file_format not in allowed_formats:
            raise ValidationError("Invalid file format. Only PNG, SVG, and JPEG are allowed.")

        key = f'{field_name}/{field_storage_name}'

        try:
            s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, key)
        except ClientError as e:
            raise ValidationError("An error occurred while uploading the profile photo.")

        serializer.validated_data['image'] = f'http://localstack/{AWS_STORAGE_BUCKET_NAME}/{key}'
