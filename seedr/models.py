"""Data models for Seedr API responses."""

from typing import List, Optional


class SeedrTorrent:
    """Represents a torrent in Seedr."""

    def __init__(self, id: int, name: str, folder: str, size: int, hash: str, 
                 progress: str, last_update: str):
        self.id = id
        self.name = name
        self.folder = folder
        self.size = size
        self.hash = hash
        self.progress = progress
        self.last_update = last_update

    @classmethod
    def from_json(cls, data: dict) -> 'SeedrTorrent':
        """Create SeedrTorrent from JSON response."""
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            folder=data.get('folder', ''),
            size=data.get('size', 0),
            hash=data.get('hash', ''),
            progress=str(data.get('progress', '0')),
            last_update=data.get('last_update', '')
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'folder': self.folder,
            'size': self.size,
            'hash': self.hash,
            'progress': self.progress,
            'last_update': self.last_update
        }


class SeedrFolder:
    """Represents a folder in Seedr."""

    def __init__(self, id: int, name: str, fullname: str, size: int, last_update: str):
        self.id = id
        self.name = name
        self.fullname = fullname
        self.size = size
        self.last_update = last_update

    @classmethod
    def from_json(cls, data: dict) -> 'SeedrFolder':
        """Create SeedrFolder from JSON response."""
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            fullname=data.get('fullname', ''),
            size=data.get('size', 0),
            last_update=data.get('last_update', '')
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'fullname': self.fullname,
            'size': self.size,
            'last_update': self.last_update
        }


class SeedrFile:
    """Represents a file in Seedr."""

    def __init__(self, name: str, size: int, hash: str, folder_id: int, 
                 folder_file_id: int, file_id: int, last_update: str, 
                 play_video: bool, video_progress: str):
        self.name = name
        self.size = size
        self.hash = hash
        self.folder_id = folder_id
        self.folder_file_id = folder_file_id
        self.file_id = file_id
        self.last_update = last_update
        self.play_video = play_video
        self.video_progress = video_progress

    @classmethod
    def from_json(cls, data: dict) -> 'SeedrFile':
        """Create SeedrFile from JSON response."""
        return cls(
            name=data.get('name', ''),
            size=data.get('size', 0),
            hash=data.get('hash', ''),
            folder_id=data.get('folder_id', 0),
            folder_file_id=data.get('folder_file_id', 0),
            file_id=data.get('file_id', 0),
            last_update=data.get('last_update', ''),
            play_video=data.get('play_video', False),
            video_progress=data.get('video_progress', '0.00')
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'size': self.size,
            'hash': self.hash,
            'folder_id': self.folder_id,
            'folder_file_id': self.folder_file_id,
            'file_id': self.file_id,
            'last_update': self.last_update,
            'play_video': self.play_video,
            'video_progress': self.video_progress
        }


class SeedrFolderResponse:
    """Represents a folder response with all its contents."""

    def __init__(self, space_max: int, space_used: int, folder_id: int, 
                 fullname: str, name: str, parent: Optional[int], 
                 folders: List[SeedrFolder], files: List[SeedrFile], 
                 torrents: List[SeedrTorrent]):
        self.space_max = space_max
        self.space_used = space_used
        self.folder_id = folder_id
        self.fullname = fullname
        self.name = name
        self.parent = parent
        self.folders = folders
        self.files = files
        self.torrents = torrents

    @classmethod
    def from_json(cls, data: dict) -> 'SeedrFolderResponse':
        """Create SeedrFolderResponse from JSON response."""
        parent = data.get('parent')
        if parent == -1:
            parent = None
            
        folders = [SeedrFolder.from_json(f) for f in data.get('folders', [])]
        files = [SeedrFile.from_json(f) for f in data.get('files', [])]
        torrents = [SeedrTorrent.from_json(t) for t in data.get('torrents', [])]

        return cls(
            space_max=data.get('space_max', 0),
            space_used=data.get('space_used', 0),
            folder_id=data.get('folder_id', 0),
            fullname=data.get('fullname', ''),
            name=data.get('name', ''),
            parent=parent,
            folders=folders,
            files=files,
            torrents=torrents
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'space_max': self.space_max,
            'space_used': self.space_used,
            'folder_id': self.folder_id,
            'fullname': self.fullname,
            'name': self.name,
            'parent': self.parent if self.parent is not None else -1,
            'folders': [f.to_dict() for f in self.folders],
            'files': [f.to_dict() for f in self.files],
            'torrents': [t.to_dict() for t in self.torrents]
        }


class SeedrFileDetails:
    """Represents detailed file information including download URL."""

    def __init__(self, url: str, name: str, result: bool):
        self.url = url
        self.name = name
        self.result = result

    @classmethod
    def from_json(cls, data: dict) -> 'SeedrFileDetails':
        """Create SeedrFileDetails from JSON response."""
        return cls(
            url=data.get('url', ''),
            name=data.get('name', ''),
            result=data.get('result', False)
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'url': self.url,
            'name': self.name,
            'result': self.result
        }


class SeedrArchiveResponse:
    """Represents an archive creation response."""

    def __init__(self, result: bool, archive_id: int, archive_url: str):
        self.result = result
        self.archive_id = archive_id
        self.archive_url = archive_url

    @classmethod
    def from_json(cls, data: dict) -> 'SeedrArchiveResponse':
        """Create SeedrArchiveResponse from JSON response."""
        return cls(
            result=data.get('result', False),
            archive_id=data.get('archive_id', 0),
            archive_url=data.get('archive_url', '')
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'result': self.result,
            'archive_id': self.archive_id,
            'archive_url': self.archive_url
        }
