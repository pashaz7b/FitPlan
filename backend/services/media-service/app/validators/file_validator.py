from fastapi import HTTPException
from PIL import Image
import io

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_image_file(file) -> None:
    """
    Validate the uploaded file for:
    1. File size (max 10 MB)
    2. Image type validation (must be a valid image)
    """
    # Check file size
    file_size = len(file.file.read())  # Read the file content to determine size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB limit"
        )

    # Reset the file cursor after reading
    file.file.seek(0)

    # Check if the file is an image
    try:
        image = Image.open(io.BytesIO(file.file.read()))
        image.verify()  # Verify that it is a valid image
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image"
        )

    # Reset the file cursor again after verifying the image
    file.file.seek(0)
