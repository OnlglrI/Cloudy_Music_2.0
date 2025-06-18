from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Column, DateTime, func
from pydantic import BaseModel


metadata = MetaData(schema="playlist")

playlist_table = Table(
    "playlist_songs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("playlist_id", Integer, index=True),
    Column("song_id", Integer),
    Column("added_at", DateTime(timezone=True), server_default=func.now()),
)

user_table = Table(
    "user_playlist",
    metadata,
    Column("playlist_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, index=True),
    Column("playlist_name", String),
    # Column("playlist_url", String),
    Column("added_at", DateTime(timezone=True), server_default=func.now()),
)

favorite_table = Table(
    "favorite_songs",
    metadata,
    Column("favorite_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, index=True),
    Column("song_id", Integer),
    Column("added_at", DateTime(timezone=True), server_default=func.now()),
)

disliked_table = Table(
    "disliked_songs",
    metadata,
    Column("disliked_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, index=True),
    Column("song_id", Integer),
    Column("added_at", DateTime(timezone=True), server_default=func.now()),
)

class PlaylistAddDelEvent(BaseModel):
    playlist_id: str
    song_id: str

class PlaylistCreate(BaseModel):
    user_id: str
    playlist_name: str
    # playlist_url: str

class PlaylistDelete(BaseModel):
    playlist_id: int

class PlaylistUpdate(BaseModel):
    user_id: str
    playlist_id: str
    playlist_name: str

class SongLikeDisEvent(BaseModel):
    user_id: str
    song_id: str

