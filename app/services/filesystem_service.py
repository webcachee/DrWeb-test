import os

from flask import current_app


class FileSystemService:
    """
    Service class for handling file operations in the file system.

    This class provides static methods for file management tasks such as
    retrieving file paths, saving files, deleting files, and checking if a file exists.
    """

    @staticmethod
    def get_file_path(file_hash: str) -> str:
        """
        Constructs the file path for a given file hash.

        This method generates a file path by combining the storage folder, a subdirectory
        derived from the first two characters of the file hash, and the file hash itself.

        Args:
            file_hash (str): The hash of the file used to determine the file path.

        Returns:
            str: The complete file path for the given file hash.
        """
        return os.path.join(
            current_app.config["STORAGE_FOLDER"], file_hash[:2], file_hash
        )

    @staticmethod
    def save_file(file_content: bytes, file_hash: str) -> bool:
        """
        Saves file content to the file system.

        This method writes the provided file content to a file at the path determined
        by the file hash. It ensures that the necessary directories are created.

        Args:
            file_content (bytes): The content of the file to be saved.
            file_hash (str): The hash of the file used to determine the file path.

        Returns:
            bool: True if the file was saved successfully, False otherwise.
        """
        file_path = FileSystemService.get_file_path(file_hash)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
            return True
        except IOError as e:
            current_app.logger.error(f"Failed to save file {file_hash}: {str(e)}.")
            return False

    @staticmethod
    def delete_file(file_hash: str) -> None:
        """
        Deletes a file from the file system.

        This method removes the file specified by the file hash if it exists.

        Args:
            file_hash (str): The hash of the file used to determine the file path.

        Returns:
            None
        """
        file_path = FileSystemService.get_file_path(file_hash)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError as e:
            current_app.logger.error(f"Failed to delete file {file_hash}: {str(e)}.")

    @staticmethod
    def file_exists(file_hash: str) -> bool:
        """
        Checks if a file exists in the file system.

        This method determines whether a file exists at the path specified by the file hash.

        Args:
            file_hash (str): The hash of the file used to determine the file path.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        file_path = FileSystemService.get_file_path(file_hash)
        return os.path.isfile(file_path)
