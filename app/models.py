from app import db


class File(db.Model):
    """
    SQLAlchemy model for storing file metadata.

    This model represents a file stored in the database with attributes such as
    a unique hash, filename, and a primary key ID.

    Attributes:
        id (int): Primary key identifier for the file.
        file_hash (str): SHA-256 hash of the file, unique across all records.
        filename (str): Original name of the file.

    Methods:
        __repr__(): Provides a string representation of the File instance.
    """

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(64), unique=True, nullable=False)
    filename = db.Column(db.String(64), nullable=False)
    username =  db.Column(db.String(80), nullable=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the File instance.

        This method provides a human-readable string representation of the File
        instance, showing the filename and file hash.

        Returns:
            str: A string representation of the File instance, e.g., "<File filename with hash file_hash>".
        """
        return f"<File {self.filename} with hash {self.file_hash}"
