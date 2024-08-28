import hashlib

from flask import current_app, jsonify


def hash_file(file_content: bytes) -> str:
    """
    Computes the SHA-256 hash of the given file content.

    This function takes the content of a file as bytes and returns its SHA-256 hash as a hexadecimal string.

    Args:
        file_content (bytes): The content of the file to hash.

    Returns:
        str: The hexadecimal representation of the SHA-256 hash of the file content.
    """
    return hashlib.sha256(file_content).hexdigest()


def json_response(message: dict, status_code: int) -> tuple:
    """
    Creates a JSON response with a given message and status code.

    This function formats the message as a JSON object and sets the appropriate HTTP status code.

    Args:
        message (dict): The message to include in the JSON response.
        status_code (int): The HTTP status code for the response.

    Returns:
        tuple: A tuple containing the JSON response and status code.
    """
    return jsonify(message), status_code


def handle_error(message: str, status_code: int, log_message: str = None) -> tuple:
    """
    Creates a JSON response for an error message and logs the error if a log message is provided.

    This function formats the error message as a JSON object and sets the appropriate HTTP status code.
    If a log message is provided, it is logged at the error level.

    Args:
        message (str): The error message to include in the JSON response.
        status_code (int): The HTTP status code for the response.
        log_message (str, optional): A message to log at the error level. Defaults to None.

    Returns:
        tuple: A tuple containing the JSON response and status code.
    """
    if log_message:
        current_app.logger.error(log_message)
    return json_response({"error": message}, status_code)
