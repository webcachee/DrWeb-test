from flask import Blueprint, Response, current_app, request, send_file

from app.auth import requires_auth
from app.services.file_service import FileService
from app.utils import handle_error, json_response

main = Blueprint("main", __name__)


@main.route("/upload", methods=["POST"])
@requires_auth
def upload_file(username: str) -> Response:
    """
    Handles file upload requests.

    This endpoint allows authenticated users to upload files. The file must be included in the request under
    the 'file' key. If no file is provided or the file has no name, an error response will be returned.
    On successful upload, the service will return a success response with details of the uploaded file.

    Args:
        username (str): The username of the authenticated user making the request.

    Returns:
        Response: A Flask Response object containing the result of the upload operation or an error message.
    """
    if "file" not in request.files:
        return handle_error("No file part.", 400, "No file part in the request.")

    file = request.files["file"]
    if file.filename == "":
        return handle_error("No selected file.", 400, "No selected file.")

    result = FileService.upload_file(file, username)

    if "error" in result:
        return handle_error(result["error"], 400, f"Upload error: {result['error']}")

    current_app.logger.info(f"File uploaded successfully: {result}.")
    return json_response(result, 201)


@main.route("/download/<file_hash>", methods=["GET"])
def download_file(file_hash: str) -> Response:
    """
    Handles file download requests.

    This endpoint allows users to download files using a unique file hash. If the file is found, it will be
    sent to the client as an attachment. If the file is not found, an error response will be returned.

    Args:
        file_hash (str): The hash of the file to be downloaded.

    Returns:
        Response: A Flask Response object for the file download or an error message if the file is not found.
    """
    result = FileService.download_file(file_hash)

    if result is None:
        return handle_error(
            "File not found.", 404, f"File not found for hash: {file_hash}."
        )

    file_record, file_path = result

    try:
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=file_record.filename,
            mimetype="application/octet-stream",
        )
        current_app.logger.info(
            f"File downloaded: {file_record.filename} (hash: {file_hash})."
        )
        return response
    except Exception as e:
        current_app.logger.error(
            f"Error during file download for hash {file_hash}: {str(e)}"
        )
        return handle_error("Internal Server Error", 500)


@main.route("/delete/<file_hash>", methods=["DELETE"])
@requires_auth
def delete_file(username: str, file_hash: str) -> Response:
    """
    Handles file deletion requests.

    This endpoint allows authenticated users to delete files using a unique file hash. If the file is successfully
    deleted, a success message is returned. If the file is not found or the user is unauthorized, an error response
    will be returned.

    Args:
        username (str): The username of the authenticated user making the request.
        file_hash (str): The hash of the file to be deleted.

    Returns:
        Response: A Flask Response object indicating the result of the deletion operation.
    """
    success = FileService.delete_file(file_hash, username)

    if not success:
        return handle_error(
            "File not found or unauthorized.",
            404,
            f"Delete failed for hash: {file_hash}.",
        )

    current_app.logger.info(f"File deleted successfully for hash: {file_hash}.")
    return json_response({"message": "File deleted."}, 200)
