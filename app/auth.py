from functools import wraps

from flask import Response, current_app, request


def check_auth(username, password):
    """
    Checks if the provided username and password are valid.

    This function verifies whether the provided credentials match any in the
    configured user dictionary.

    Args:
        username (str): The username to verify.
        password (str): The password to verify.

    Returns:
        bool: True if the username exists and the password matches, False otherwise.
    """
    return (
        username in current_app.config["USERS"]
        and current_app.config["USERS"][username] == password
    )


def authenticate() -> Response:
    """
    Returns a response indicating that authentication is required.

    This function creates a response with a 401 Unauthorized status code
    and a header prompting the client to provide proper credentials.

    Returns:
        Response: A Flask Response object with a 401 status code and an authentication header.
    """
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def requires_auth(f):
    """
    A decorator to enforce authentication on Flask routes.

    This decorator checks if the request contains valid credentials using
    Basic Authentication. If the credentials are valid, the decorated function
    is called with the username as the first argument. Otherwise, a 401 response
    is returned prompting the user to authenticate.

    Args:
        f (function): The function to decorate. It should accept a username as the first argument.

    Returns:
        function: The decorated function or the authentication response.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(auth.username, *args, **kwargs)

    return decorated
