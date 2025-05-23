from django.core.exceptions import ValidationError
def validate_file_size(file):
    max_size = 10 * 1024 * 1024  # 10 MB limit
    if file.size > max_size:
        raise ValidationError(f"File size exceeds the limit of {max_size / (1024 * 1024)} MB")