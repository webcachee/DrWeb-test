import os


class Config:
    """
    Configuration class for the Flask application.

    This class contains various configuration settings for the Flask app, including
    database settings, storage paths, and user credentials. It provides the necessary
    configuration for running the app in different environments.

    Attributes:
        STORAGE_FOLDER (str): The directory path for storing uploaded files.
        SQLALCHEMY_DATABASE_URI (str): The URI for connecting to the SQLite database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to disable or enable SQLAlchemy event system.
        USERS (dict): A dictionary containing user credentials with usernames as keys and passwords as values.
        DEBUG (bool): Flag to enable or disable debug mode in Flask.
    """

    STORAGE_FOLDER = os.path.join(os.getcwd(), "store")
    SQLALCHEMY_DATABASE_URI = "sqlite:///files.db"
    SQLACLHEMY_TRACK_MODIFICATIONS = False
    USERS = {
        "user1": os.getenv("USER1_PASSWORD", "password1"),
        "user2": os.getenv("USER2_PASSWORD", "password2"),
    }
    DEBUG = os.getenv("DEBUG", False)
