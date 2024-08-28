from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import File


class FileRepository:
    """
    Repository class for handling file-related database operations.

    This class provides static methods for interacting with the `File` model in the database.
    It includes operations such as retrieving, adding, checking existence, and deleting file records.
    """

    @staticmethod
    def get_file_by_hash(file_hash: str) -> File:
        """
        Retrieves a file record from the database based on its hash.

        This method queries the database for a file record with the specified file hash.

        Args:
            file_hash (str): The hash of the file to retrieve.

        Returns:
            File: The file record if found, otherwise None.
        """
        return File.query.filter_by(file_hash=file_hash).first()

    @staticmethod
    def add_file(file_record: File) -> None:
        """
        Adds a new file record to the database.

        This method adds the provided file record to the database and commits the transaction.
        If an error occurs, it rolls back the transaction to maintain database integrity.

        Args:
            file_record (File): The file record to be added to the database.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation.

        Returns:
            None
        """
        try:
            db.session.add(file_record)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def file_exists(file_hash: str) -> bool:
        """
        Checks if a file record exists in the database based on its hash.

        This method queries the database to determine if a file with the specified hash exists.

        Args:
            file_hash (str): The hash of the file to check for existence.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return db.session.query(
            File.query.filter_by(file_hash=file_hash).exists()
        ).scalar()

    @staticmethod
    def delete_file(file_record: File) -> None:
        """
        Deletes a file record from the database.

        This method removes the specified file record from the database and commits the transaction.
        If an error occurs, it rolls back the transaction to maintain database integrity.

        Args:
            file_record (File): The file record to be deleted from the database.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation.

        Returns:
            None
        """
        try:
            db.session.delete(file_record)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
