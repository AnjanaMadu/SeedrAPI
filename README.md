# <img src="https://graph.org/file/567afbf357f1ecbe98376.png" alt="seedr" height=50> Seedr API

### Unofficial API wrapper for seedr.cc <br> Inspired by [theabbie](https://github.com/theabbie)'s [**seedr-api**](https://github.com/theabbie/seedr-api)

Powered by [**@harp_tech**](https://github.com/harptechorg) ([_Telegram_](https://t.me/harp_tech))

## How to use

- You can install lib via [github](https://github.com/AnjanaMadu/SeedrAPI.git) or [pypi](https://pypi.org/project/seedr).
```
pip install seedr
```

- Examples
```py
# Import the lib
from seedr import SeedrAPI

# Login to account. You can login to your account by email and password or via access token.
# After login an access token will retrieve. Don't care, It's for devs.
seedr = SeedrAPI(email='example@email.com', password='example')

# Get all files and folders in your account
files = seedr.get_drive()

# Add magnet to your account
tor = seedr.add_torrent('magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a')
print(tor) # This may retrieve some info about torrent etc...

# Go to a dir and get details
dir = seedr.get_folder('folder_id')

# Get direct link for a file
file = seedr.get_file('file_id')

# Delete a folder
seedr.delete_folder('folder_id')

# Delete a file
seedr.delete_file('file_id')

# Rename a file
seedr.rename('file_id', 'new_name')
```

## Credits
- [theabbie](https://github.com/theabbie) for his [seedr-api](https://github.com/theabbie/seedr-api)
- [me](https://github.com/AnjanaMadu) for nothing

### No dev contacts here. [Support chat](https://t.me/harp_chat)
