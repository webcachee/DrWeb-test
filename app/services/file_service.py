from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.models import File
from app.repositories.file_repository import FileRepository
from app.services.filesystem_service import FileSystemService
from app.utils import hash_file


class FileService:
    """
    Service class for managing file operations, including uploading, downloading, and deleting files.

    This class provides methods for handling file operations by interacting with both the file system
    and the database. It uses the FileRepository for database operations and the FileSystemService
    for file system interactions.
    """

    @staticmethod
    def upload_file(file, username: str) -> dict:
        """
        Uploads a file to the system and saves its metadata to the database.

        This method reads the content of the file, computes its hash, and checks if the file already
        exists in the database. If not, it saves the file to the file system and adds its metadata
        to the database.

        Args:
            file (FileStorage): The file object to be uploaded. This should be an instance of Flask's
                                FileStorage, which has methods like `read()` and `seek()`.

        Returns:
            dict: A dictionary containing either the file hash with a success message or an error message
                  if the file could not be saved.
        """
        file_content = file.read()
        file_hash = hash_file(file_content)
        file.seek(0)

        if FileRepository.file_exists(file_hash):
            return {"message": "File already exists.", "file_hash": file_hash}

        if not FileSystemService.save_file(file_content, file_hash):
            current_app.logger.error(f"Error saving file: {str(e)}.")
            return {"error": "Could not save file."}

        try:
            new_file = File(file_hash=file_hash, filename=file.filename, username=username)
            FileRepository.add_file(new_file)
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error while adding file: {str(e)}.")
            FileSystemService.delete_file(file_hash)
            return {"error": "Could not save file metadata."}

        return {"file_hash": file_hash}

    @staticmethod
    def download_file(file_hash: str) -> tuple:
        """
        Retrieves a file from the system based on its hash.

        This method checks if the file metadata exists in the database and if the file exists in the file
        system. If both checks pass, it returns the file record and file path.

        Args:
            file_hash (str): The hash of the file to be downloaded.

        Returns:
            tuple: A tuple containing the file record and the file path if the file is found, otherwise None.
        """
        file_record = FileRepository.get_file_by_hash(file_hash)
        if not file_record:
            current_app.logger.error(
                f"File not found in database for hash: {file_hash}."
            )
            return None

        file_path = FileSystemService.get_file_path(file_hash)

        if not FileSystemService.file_exists(file_hash):
            current_app.logger.error(f"File not found on disk for hash: {file_hash}.")
            return None

        return file_record, file_path

    @staticmethod
    def delete_file(file_hash: str, username: str) -> bool:
        """
        Deletes a file from the system and its metadata from the database.

        This method removes the file from the file system and deletes its metadata from the database.
        It handles errors by logging and returning a failure status.

        Args:
            file_hash (str): The hash of the file to be deleted.

        Returns:
            bool: True if the file and metadata were successfully deleted, False otherwise.
        """
        file_record = FileRepository.get_file_by_hash(file_hash)
        if not file_record or file_record.username != username:
            current_app.logger.error(
                f"File not found in database for hash: {file_hash} by user: {username}."
            )
            return False

        try:
            FileSystemService.delete_file(file_hash)
            FileRepository.delete_file(file_record)
            return True
        except (OSError, SQLAlchemyError) as e:
            current_app.logger.error(
                f"Error deleting file or database record: {str(e)}."
            )
            return False
