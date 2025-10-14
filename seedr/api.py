import json
import requests
from .errors import (
    InvalidLogin,
    InvalidToken,
    LoginRequired
)


class SeedrAPI:
    """A wrapper for the Seedr.cc API.

    This class provides a simple interface to interact with the Seedr.cc API.
    It handles authentication and provides methods for common API operations.

    Args:
        email (str, optional): The user's Seedr account email. Defaults to None.
        password (str, optional): The user's Seedr account password. Defaults to None.
        token (str, optional): An existing access token. Defaults to None.

    Raises:
        InvalidLogin: If the provided email and password are not valid.
        InvalidToken: If the provided token is not valid.
        LoginRequired: If no authentication credentials are provided.
    """

    def __init__(self, email=None, password=None, token=None):
        """Initializes the SeedrAPI client and authenticates the user.

        Args:
            email (str, optional): The user's Seedr account email. Defaults to None.
            password (str, optional): The user's Seedr account password. Defaults to None.
            token (str, optional): An existing access token. Defaults to None.

        Raises:
            InvalidLogin: If the provided email and password are not valid.
            InvalidToken: If the provided token is not valid.
            LoginRequired: If no authentication credentials are provided.
        """
        if email and password:
            data = {"grant_type": "password", "client_id": "seedr_chrome", "type": "login", "username": email, "password": password}
            req = requests.post("https://www.seedr.cc/oauth_test/token.php", data=data)
            if "access_token" in req.text:
                self.access_token = json.loads(req.text)["access_token"]
            else:
                raise InvalidLogin("Invalid username and password combination.")
        elif token:
            req = requests.get(f"https://www.seedr.cc/api/folder?access_token={token}")
            if "invalid_token" in req.text:
                raise InvalidToken("Invalid access token.")
            else:
                self.access_token = token
        else:
            raise LoginRequired("Account login required.")

    def get_drive(self):
        """Retrieves information about the user's account.

        This includes the space used, maximum space, and a list of root folders.

        Returns:
            dict: A dictionary containing account information.

        Raises:
            InvalidToken: If the access token is invalid.
        """
        req = requests.get(f"https://www.seedr.cc/api/folder?access_token={self.access_token}")
        if "invalid_token" in req.text:
            raise InvalidToken("Invalid access token.")
        else:
            return json.loads(req.text)

    def get_folder(self, folder_id):
        """Retrieves information about a specific folder.

        This includes subfolders and files within the specified folder.

        Args:
            folder_id (str): The ID of the folder to retrieve.

        Returns:
            dict: A dictionary containing folder information.

        Raises:
            Exception: If the folder ID is invalid.
            InvalidToken: If the access token has expired.
        """
        req = requests.get(f"https://www.seedr.cc/api/folder/{folder_id}?access_token={self.access_token}")
        if "access_denied" in req.text:
            raise Exception("Folder id invalid.")
        elif "invalid_token" in req.text:
            raise InvalidToken("Access token expired. Need to make new API Instance.")
        else:
            return json.loads(req.text)

    def get_file(self, folder_file_id):
        """Retrieves information about a specific file.

        This includes the file name, size, hash, and a download link.

        Args:
            folder_file_id (str): The ID of the file to retrieve.

        Returns:
            dict: A dictionary containing file information.

        Raises:
            Exception: If the file ID is invalid.
            InvalidToken: If the access token has expired.
        """
        data = {"access_token": self.access_token, "func": "fetch_file", "folder_file_id": folder_file_id}
        req = requests.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if "access_denied" in req.text:
            raise Exception("File id invalid.")
        elif "invalid_token" in req.text:
            raise InvalidToken("Access token expired. Need to make new API Instance.")
        else:
            return json.loads(req.text)

    def add_torrent(self, torrent):
        """Adds a new torrent to the user's account.

        Args:
            torrent (str): The direct link to a .torrent file or a magnet URI.

        Returns:
            dict: A dictionary containing information about the added torrent.

        Raises:
            Exception: If there is an error adding the torrent.
        """
        data = {"access_token": self.access_token, "func": "add_torrent", "torrent_magnet": torrent}
        req = requests.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        x = json.loads(req.text)
        if "error" in req.text:
            raise Exception(x["error"])
        elif not x["result"]:
            raise Exception(x["result"])
        else:
            return x

    def delete_folder(self, folder_id):
        """Deletes a folder from the user's account.

        Args:
            folder_id (str): The ID of the folder to delete.

        Raises:
            Exception: If the folder ID is invalid.
            InvalidToken: If the access token has expired.
        """
        data = {"access_token": self.access_token, "func": "delete", "delete_arr": '[{"type":"folder","id":"' + folder_id + '"}]'}
        req = requests.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if "access_denied" in req.text:
            raise Exception("Folder id invalid.")
        elif "invalid_token" in req.text:
            raise InvalidToken("Access token expired. Need to make new API Instance.")

    def delete_file(self, folder_file_id):
        """Deletes a file from the user's account.

        Args:
            folder_file_id (str): The ID of the file to delete.

        Raises:
            Exception: If the file ID is invalid.
            InvalidToken: If the access token has expired.
        """
        data = {"access_token": self.access_token, "func": "delete", "delete_arr": '[{"type":"file","id":"' + folder_file_id + '"}]'}
        req = requests.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if "access_denied" in req.text:
            raise Exception("File id invalid.")
        elif "invalid_token" in req.text:
            raise InvalidToken("Access token expired. Need to make new API Instance.")
