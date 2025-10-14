# Seedr API

[![PyPI version](https://badge.fury.io/py/seedr.svg)](https://badge.fury.io/py/seedr)

An unofficial API wrapper for [seedr.cc](https://www.seedr.cc/). This library provides a simple and convenient way to interact with the Seedr API from your Python applications.

## Installation

You can install the package using pip:

```bash
pip install seedr
```

## Usage

First, you need to create an instance of the `SeedrAPI` class. You can authenticate using your email and password, or by providing an existing access token.

```python
from seedr import SeedrAPI

# Authenticate with email and password
seedr = SeedrAPI(email='your_email@example.com', password='your_password')

# Or, authenticate with an access token
# seedr = SeedrAPI(token='your_access_token')
```

### Get Drive Information

To get information about your account, including space usage and root folders:

```python
drive_info = seedr.get_drive()
print(drive_info)
```

### Get Folder Contents

To get the contents of a specific folder:

```python
folder_contents = seedr.get_folder('folder_id')
print(folder_contents)
```

### Get File Information

To get information about a specific file, including a download link:

```python
file_info = seedr.get_file('file_id')
print(file_info)
```

### Add a Torrent

To add a torrent to your account using a magnet link or a direct link to a .torrent file:

```python
torrent_info = seedr.add_torrent('magnet:?xt=urn:btih:...')
print(torrent_info)
```

### Delete a Folder

To delete a folder from your account:

```python
seedr.delete_folder('folder_id')
```

### Delete a File

To delete a file from your account:

```python
seedr.delete_file('file_id')
```

## Error Handling

The library raises specific exceptions for different types of errors:

- `InvalidLogin`: Raised for incorrect username or password.
- `InvalidToken`: Raised for an invalid or expired access token.
- `LoginRequired`: Raised when no authentication credentials are provided.

You can handle these exceptions using a `try...except` block:

```python
from seedr.errors import InvalidLogin

try:
    seedr = SeedrAPI(email='wrong@example.com', password='wrong_password')
except InvalidLogin:
    print("Invalid login credentials.")
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on the [GitHub repository](https://github.com/AnjanaMadu/SeedrAPI/issues).

If you'd like to contribute code, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a descriptive message.
4. Push your changes to your fork.
5. Open a pull request to the main repository.

## Credits

- Inspired by [theabbie](https://github.com/theabbie)'s [seedr-api](https://github.com/theabbie/seedr-api).
