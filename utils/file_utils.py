import os
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import uuid
import logging
from config import Config

logger = logging.getLogger(__name__)

def save_uploaded_file(file, upload_folder=None, allowed_extensions=None):
    """
    Safely processes and saves uploaded files with validation
    
    Args:
        file: Werkzeug FileStorage object
        upload_folder: Path to save directory
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        tuple: (unique_filename, absolute_save_path)
        
    Raises:
        ValueError: For invalid files or processing errors
    """
    # Set defaults if not provided
    upload_folder = upload_folder or Config.UPLOAD_FOLDER
    allowed_extensions = allowed_extensions or Config.ALLOWED_EXTENSIONS

    # Validate file object
    if not file or not hasattr(file, 'filename') or not hasattr(file, 'stream'):
        raise ValueError("Invalid file object provided")

    # Validate filename
    if not file.filename or file.filename.strip() == '':
        raise ValueError("No filename provided")

    # Get secure filename and extension
    filename = secure_filename(file.filename)
    if '.' not in filename:
        raise ValueError("File has no extension")
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"File type '{ext}' not allowed. Supported types: {', '.join(allowed_extensions)}")

    # Create paths
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.abspath(os.path.join(upload_folder, unique_filename))
    temp_path = f"{save_path}.tmp"

    try:
        # Ensure directory exists
        os.makedirs(upload_folder, exist_ok=True)

        # First save to temporary location
        file.stream.seek(0)  # Rewind file pointer
        file.save(temp_path)

        # Verify image
        try:
            with Image.open(temp_path) as img:
                img.verify()  # Verify file is an image
                img = Image.open(temp_path)  # Reopen for processing
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save final version
                img.save(save_path, quality=95)
                os.remove(temp_path)  # Clean up temp file
                
                logger.info(f"Successfully saved: {save_path}")
                return unique_filename, save_path

        except UnidentifiedImageError:
            raise ValueError("File is not a valid image")
        except Exception as img_error:
            raise ValueError(f"Image processing error: {str(img_error)}")

    except Exception as e:
        # Clean up any partial files
        for path in [temp_path, save_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
        logger.error(f"File processing failed: {str(e)}")
        raise ValueError(f"Failed to process file: {str(e)}")