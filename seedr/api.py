import json
import requests
from .errors import (
    InvalidLogin,
    InvalidToken,
    LoginRequired
)


class SeedrAPI:
    def __init__(self, email=None, password=None, token=None):
        """
        Initialize the SeedrAPI class. And login to account.
        :param `email`: Seedr account email.
        :param `password`: Seedr account password.
        :param `token`: Seedr access token. (don't use this if you have email and password)
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
        """
        Get the some information about the account. Including the space used, space max, and the list of folders.
        :return: A dict of the account information.
        """
        req = requests.get(f"https://www.seedr.cc/api/folder?access_token={self.access_token}")
        if "invalid_token" in req.text:
            raise InvalidToken("Invalid access token.")
        else:
            return json.loads(req.text)

    def get_folder(self, folder_id):
        """
        Get the some information about the folder. Including subfolders and files.
        :param `folder_id`: The folder id.
        :return: A dict of the folder information.
        """
        req = requests.get(f"https://www.seedr.cc/api/folder/{folder_id}?access_token={self.access_token}")
        if "access_denied" in req.text:
            raise Exception("Folder id invalid.")
        elif "invalid_token" in req.text:
            raise InvalidToken("Access token expired. Need to make new API Instance.")
        else:
            return json.loads(req.text)

    def get_file(self, folder_file_id):
        """
        Get the some information about the file. Including the file name, file size, file hash, and download link.
        :param `folder_file_id`: The file id.
        :return: A dict of the file information.
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
        """
        Add a torrent to the account.
        :param `torrent`: Direct link to .torrent or magnet uri.
        :return: A dict of the information about torrent.
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
        """
        Delete a folder from the account.
        :param `folder_id`: The folder id.
        """
        data = {"access_token": self.access_token, "func": "delete", "delete_arr": '[{"type":"folder","id":"' + folder_id + '"}]'}
        req = requests.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if "access_denied" in req.text:
            raise Exception("Folder id invalid.")
        elif "invalid_token" in req.text:
            raise InvalidToken("Access token expired. Need to make new API Instance.")

    def delete_file(self, folder_file_id):
        """
        Delete a file from the account.
        :param `folder_file_id`: The file id.
        """
        data = {"access_token": self.access_token, "func": "delete", "delete_arr": '[{"type":"folder","id":"' + folder_file_id + '"}]'}
        req = requests.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if "access_denied" in req.text:
            raise Exception("File id invalid.")
        elif "invalid_token" in req.text:
            raise InvalidToken("Access token expired. Need to make new API Instance.")
