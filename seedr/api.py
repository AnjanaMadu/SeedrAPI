import json
import requests
from typing import Optional, Callable, Any, Dict
from .models import (
    SeedrFolderResponse,
    SeedrFileDetails,
    SeedrArchiveResponse
)
from .errors import InvalidLogin, InvalidToken, LoginRequired


class SeedrAPI:
    """Modern Seedr API client with token refresh and device authentication.
    
    This class provides a comprehensive interface to interact with the Seedr.cc API.
    It handles authentication, automatic token refresh, and provides methods for all
    common API operations.
    
    Args:
        email (str, optional): The user's Seedr account email. Defaults to None.
        password (str, optional): The user's Seedr account password. Defaults to None.
        token (str, optional): An existing access token. Defaults to None.
        refresh_token (str, optional): An existing refresh token. Defaults to None.
    
    Raises:
        InvalidLogin: If the provided email and password are not valid.
        InvalidToken: If the provided token is not valid.
        LoginRequired: If no authentication credentials are provided.
    """

    def __init__(self, email=None, password=None, token=None, refresh_token=None):
        """Initialize the SeedrAPI client and authenticate if credentials are provided.
        
        Args:
            email (str, optional): The user's Seedr account email. Defaults to None.
            password (str, optional): The user's Seedr account password. Defaults to None.
            token (str, optional): An existing access token. Defaults to None.
            refresh_token (str, optional): An existing refresh token. Defaults to None.
        
        Raises:
            InvalidLogin: If the provided email and password are not valid.
            InvalidToken: If the provided token is not valid.
            LoginRequired: If no authentication credentials are provided.
        """
        self.username: Optional[str] = email
        self.password: Optional[str] = password
        self.token: Optional[str] = token
        self.access_token: Optional[str] = token  # Backward compatibility
        self.rft: Optional[str] = refresh_token
        self.devc: Optional[str] = None
        self.usc: Optional[str] = None
        self.on_token_refresh: Optional[Callable[[str, str], None]] = None
        
        # Auto-authenticate if credentials provided
        if email and password:
            self.login(email, password)
        elif token:
            req = requests.get(f"https://www.seedr.cc/api/folder?access_token={token}")
            if "invalid_token" in req.text:
                raise InvalidToken("Invalid access token.")
            self.token = token
            self.access_token = token
        elif not token and not email:
            raise LoginRequired("Account login required.")

    def login(self, username: str, password: str) -> str:
        """Authenticate with Seedr using username and password credentials.
        
        Args:
            username: Seedr account username/email
            password: Seedr account password
            
        Returns:
            Access token string
            
        Raises:
            InvalidLogin: If credentials are invalid
        """
        self.username = username
        
        url = 'https://www.seedr.cc/oauth_test/token.php'
        data = {
            'grant_type': 'password',
            'client_id': 'seedr_chrome',
            'type': 'login',
            'username': username,
            'password': password
        }
        
        response = requests.post(url, data=data)
        json_data = response.json()
        
        if 'error' in json_data:
            error_msg = json_data.get('error_description', json_data.get('error', 'Unknown error'))
            raise InvalidLogin(f"{json_data['error']}: {error_msg}")
        
        self.token = json_data.get('access_token')
        self.access_token = self.token  # Backward compatibility
        self.rft = json_data.get('refresh_token')
        
        if not self.token:
            raise InvalidLogin('Login failed: No access token received.')
        
        return self.token

    def get_device_code(self) -> str:
        """Retrieve a device code and user code for device-based authentication.
        
        Returns:
            User code string to be used for authorization
        """
        url = 'https://www.seedr.cc/oauth_test/device.php'
        response = requests.get(url)
        data = response.json()
        
        self.devc = data['device_code']
        return data['user_code']

    def get_token(self, device_code: str) -> str:
        """Retrieve an access token using a device code.
        
        Args:
            device_code: Device code obtained from get_device_code()
            
        Returns:
            Access token string
            
        Raises:
            Exception: If token retrieval fails
        """
        url = 'https://www.seedr.cc/oauth_test/token.php'
        data = {
            'grant_type': 'device_code',
            'client_id': 'seedr_chrome',
            'device_code': device_code
        }
        
        response = requests.post(url, data=data)
        json_data = response.json()
        
        if 'error' in json_data:
            raise Exception(f"Failed to get token: {json_data.get('error')}")
        
        self.token = json_data.get('access_token')
        self.access_token = self.token  # Backward compatibility
        return self.token

    def refresh_token(self) -> None:
        """Refresh the access token using the refresh token.
        
        Raises:
            Exception: If no refresh token is available or refresh fails
        """
        if not self.rft:
            raise Exception('No refresh token available.')
        
        url = 'https://www.seedr.cc/oauth_test/token.php'
        data = {
            'grant_type': 'refresh_token',
            'client_id': 'seedr_chrome',
            'refresh_token': self.rft
        }
        
        response = requests.post(url, data=data)
        json_data = response.json()
        
        if 'access_token' in json_data:
            self.token = json_data['access_token']
            self.access_token = self.token  # Backward compatibility
            if 'refresh_token' in json_data:
                self.rft = json_data['refresh_token']
            
            if self.on_token_refresh:
                self.on_token_refresh(self.token, self.rft)
        else:
            error = json_data.get('error', 'Unknown error')
            raise Exception(f'Failed to refresh token: {error}')

    def _with_token_retry(self, action: Callable[[], Any]) -> Any:
        """Helper to retry an operation if the token is expired.
        
        Args:
            action: Function to execute with retry logic
            
        Returns:
            Result from the action
        """
        try:
            result = action()
            
            # Check if result indicates expired token
            if isinstance(result, dict):
                if result.get('error') in ['expired_token', 'invalid_token']:
                    self.refresh_token()
                    return action()
            
            return result
        except Exception as e:
            error_str = str(e).lower()
            if any(word in error_str for word in ['expired', 'token', '401']):
                try:
                    self.refresh_token()
                    return action()
                except Exception:
                    raise e
            raise

    def add_magnet(self, magnet: str) -> Dict[str, Any]:
        """Add a torrent to Seedr using a magnet link.
        
        Args:
            magnet: Magnet link or torrent URL
            
        Returns:
            Dictionary with result information
        """
        def _add():
            url = 'https://www.seedr.cc/oauth_test/resource.php'
            data = {
                'access_token': self.token,
                'func': 'add_torrent',
                'torrent_magnet': magnet
            }
            response = requests.post(url, data=data)
            return response.json()
        
        return self._with_token_retry(_add)

    def add_torrent(self, torrent: str) -> Dict[str, Any]:
        """Add a torrent to Seedr (legacy method name).
        
        Args:
            torrent: Magnet link or torrent URL
            
        Returns:
            Dictionary with result information
        """
        return self.add_magnet(torrent)

    def get_folder_contents(self, folder_id: Optional[int] = None) -> SeedrFolderResponse:
        """Retrieve the contents of a specific folder or the root folder.
        
        Args:
            folder_id: ID of the folder to retrieve. None for root folder.
            
        Returns:
            SeedrFolderResponse object with folder contents
            
        Raises:
            InvalidToken: If token is invalid and refresh fails
        """
        def _get():
            if folder_id is None:
                url = f'https://www.seedr.cc/api/folder?access_token={self.token}'
            else:
                url = f'https://www.seedr.cc/api/folder/{folder_id}?access_token={self.token}'
            
            response = requests.get(url)
            json_data = response.json()
            
            if isinstance(json_data, dict):
                if json_data.get('error') in ['expired_token', 'invalid_token']:
                    raise InvalidToken('Token expired')
            
            return SeedrFolderResponse.from_json(json_data)
        
        return self._with_token_retry(_get)

    def get_drive(self) -> dict:
        """Retrieve information about the user's account (legacy method).
        
        Returns:
            Dictionary containing account information
        """
        folder = self.get_folder_contents()
        return folder.to_dict()

    def get_folder(self, folder_id: int) -> dict:
        """Retrieve information about a specific folder (legacy method).
        
        Args:
            folder_id: ID of the folder to retrieve
            
        Returns:
            Dictionary containing folder information
        """
        folder = self.get_folder_contents(folder_id)
        return folder.to_dict()

    def get_file(self, folder_file_id: int) -> dict:
        """Fetch information about a specific file by its ID.
        
        Args:
            folder_file_id: ID of the file to retrieve
            
        Returns:
            Dictionary with file information and download URL
        """
        def _get():
            url = 'https://www.seedr.cc/oauth_test/resource.php'
            data = {
                'access_token': self.token or '',
                'func': 'fetch_file',
                'folder_file_id': str(folder_file_id)
            }
            response = requests.post(url, data=data)
            file_details = SeedrFileDetails.from_json(response.json())
            return file_details.to_dict()
        
        return self._with_token_retry(_get)

    def get_file_details(self, folder_file_id: int) -> SeedrFileDetails:
        """Fetch detailed file information as typed object.
        
        Args:
            folder_file_id: ID of the file to retrieve
            
        Returns:
            SeedrFileDetails object
        """
        def _get():
            url = 'https://www.seedr.cc/oauth_test/resource.php'
            data = {
                'access_token': self.token or '',
                'func': 'fetch_file',
                'folder_file_id': str(folder_file_id)
            }
            response = requests.post(url, data=data)
            return SeedrFileDetails.from_json(response.json())
        
        return self._with_token_retry(_get)

    def delete_file(self, file_id: Any) -> Dict[str, Any]:
        """Delete a file from your Seedr account.
        
        Args:
            file_id: ID of the file to delete (int or str)
            
        Returns:
            Dictionary with result information
        """
        def _delete():
            url = 'https://www.seedr.cc/oauth_test/resource.php'
            
            # Handle both int and string IDs
            if isinstance(file_id, str):
                parsed_id = int(file_id) if file_id.isdigit() else file_id
            else:
                parsed_id = file_id
            
            data = {
                'access_token': self.token or '',
                'func': 'delete',
                'delete_arr': json.dumps([{'type': 'file', 'id': parsed_id}])
            }
            response = requests.post(url, data=data)
            return response.json()
        
        return self._with_token_retry(_delete)

    def delete_folder(self, folder_id: Any) -> Dict[str, Any]:
        """Delete a folder from your Seedr account.
        
        Args:
            folder_id: ID of the folder to delete (int or str)
            
        Returns:
            Dictionary with result information
        """
        def _delete():
            url = 'https://www.seedr.cc/oauth_test/resource.php'
            
            # Handle both int and string IDs
            if isinstance(folder_id, str):
                parsed_id = int(folder_id) if folder_id.isdigit() else folder_id
            else:
                parsed_id = folder_id
            
            data = {
                'access_token': self.token or '',
                'func': 'delete',
                'delete_arr': json.dumps([{'type': 'folder', 'id': parsed_id}])
            }
            response = requests.post(url, data=data)
            return response.json()
        
        return self._with_token_retry(_delete)

    def delete_torrent(self, torrent_id: Any) -> Dict[str, Any]:
        """Delete a torrent from your Seedr account.
        
        Args:
            torrent_id: ID of the torrent to delete (int or str)
            
        Returns:
            Dictionary with result information
        """
        def _delete():
            url = 'https://www.seedr.cc/oauth_test/resource.php'
            
            # Handle both int and string IDs
            if isinstance(torrent_id, str):
                parsed_id = int(torrent_id) if torrent_id.isdigit() else torrent_id
            else:
                parsed_id = torrent_id
            
            data = {
                'access_token': self.token or '',
                'func': 'delete',
                'delete_arr': json.dumps([{'type': 'torrent', 'id': parsed_id}])
            }
            response = requests.post(url, data=data)
            return response.json()
        
        return self._with_token_retry(_delete)

    def create_archive(self, folder_id: Any) -> SeedrArchiveResponse:
        """Create an archive from a folder.
        
        Args:
            folder_id: ID of the folder to archive (int or str)
            
        Returns:
            SeedrArchiveResponse object with archive information and URL
        """
        def _create():
            url = 'https://www.seedr.cc/oauth_test/resource.php'
            
            # Handle both int and string IDs
            if isinstance(folder_id, str):
                parsed_id = int(folder_id) if folder_id.isdigit() else folder_id
            else:
                parsed_id = folder_id
            
            data = {
                'access_token': self.token or '',
                'func': 'create_empty_archive',
                'archive_arr': json.dumps([{'type': 'folder', 'id': parsed_id}])
            }
            response = requests.post(url, data=data)
            return SeedrArchiveResponse.from_json(response.json())
        
        return self._with_token_retry(_create)
