from load import *
import pandas as pd


def add_listen_history(df,conn): # проверку на соглосовоность типов данных прошел почти работает

    starts = df[df["event_type"] == "play"].copy()
    ends = df[df["event_type"].isin(['complete','next','privius'])].copy()

    starts = starts.sort_values(by=["user_id", "song_id", "timestamp"]).reset_index(drop=True)
    ends = ends.sort_values(by=["user_id", "song_id", "timestamp"]).reset_index(drop=True)

    starts["listen_id"] = starts.groupby(["user_id", "song_id"]).cumcount()
    ends["listen_id"] = ends.groupby(["user_id", "song_id"]).cumcount()

    merged = pd.merge(
        starts[["user_id", "song_id", "timestamp", "listen_id"]],
        ends[["user_id", "song_id", "timestamp", "listen_id"]],
        on=["user_id", "song_id", "listen_id"],
        suffixes=("_start", "_end")
    )
    merged['timestamp_end'] = pd.to_datetime(merged['timestamp_end'])
    merged['timestamp_start'] = pd.to_datetime(merged['timestamp_start'])
    # 6. Расчёт продолжительности в секундах
    merged["duration_sec"] = (merged["timestamp_end"] - merged["timestamp_start"]).dt.total_seconds()

    # 7. Вывод результата
    result = merged[["user_id", "song_id", "timestamp_start", "duration_sec"]].rename(columns={'timestamp_start':'played_at'}).replace({"": None})
    bulk_upsert(result, 'listen_history' , conn,)

def add_likes(df,conn): # проверку на соглосовоность типов данных прошел
    likes_df = (
        df[df["event_type"] == 'like'][['user_id', 'song_id', 'timestamp']]
        .rename(columns={'timestamp':'liked_at'})
        .replace({"": None})
        .drop_duplicates(subset=['user_id', 'song_id'])
        .assign(
            user_id=lambda df: df['user_id'].astype(int),
            song_id=lambda df: df['song_id'].astype(int)
        )
    )
    bulk_upsert(likes_df, 'likes' , conn, ['user_id','song_id'], ['liked_at'] )

    unlikes_df = (
        df[df["event_type"] == 'unlike'][['user_id', 'song_id', 'timestamp']]
        .rename(columns={'timestamp':'liked_at'})
        .replace({"": None})
        .drop_duplicates(subset=['user_id', 'song_id'])
        .assign(
            user_id=lambda df: df['user_id'].astype(int),
            song_id=lambda df: df['song_id'].astype(int)
        )
    )
    bulk_delete(conn, 'likes' , ['user_id', 'song_id'],unlikes_df)

def add_dislikes(df,conn): # проверку на соглосовоность типов данных прошел
    dislake = (
        df[df["event_type"] == 'dislike'][['user_id', 'song_id', 'timestamp']]
        .rename(columns={'timestamp': 'disliked_at'})
        .replace({"": None})
        .drop_duplicates(subset=['user_id', 'song_id'])
        .assign(
            user_id=lambda x: x['user_id'].astype(int),
            song_id=lambda x: x['song_id'].astype(int)
        )
    )
    bulk_upsert(dislake, 'dislikes' , conn, ['user_id','song_id'], ['disliked_at'] )

    undislake = (
        df[df["event_type"] == 'undislike'][['user_id', 'song_id', 'timestamp']]
        .rename(columns={'timestamp': 'disliked_at'})
        .replace({"": None})
        .drop_duplicates(subset=['user_id', 'song_id'])
        .assign(
            user_id=lambda x: x['user_id'].astype(int),
            song_id=lambda x: x['song_id'].astype(int)
        )
    )
    bulk_delete(conn, 'dislikes' , ['user_id', 'song_id'],undislake)

def add_playlists(df,conn): # проверку на согласованость не прошел нету position
    add_song_df = (
        df[df['event_type'] == 'add-playlist'][['playlist_id', 'song_id', 'position']]
        .replace({"": None})
        .dropna(subset=['playlist_id', 'song_id'])
    )
    bulk_upsert(add_song_df, 'playlist_songs', conn)

    delete_song_df = (
        df[df['event_type'] == 'delete-playlist'][['playlist_id', 'song_id', 'position']]
        .replace({"": None})
        .dropna(subset=['playlist_id', 'song_id'])
    )
    bulk_delete(conn, 'playlist_songs' , ['playlist_id', 'song_id'],delete_song_df)


def add_user_song_aggregate(df,conn): #  # проверку на соглосовоность типов данных прошел
    user_song_agg_df = df[df['event_type']=='play'].groupby(['user_id','song_id']).size().reset_index(name='playcount').rename(columns={'playcount':'plays'}).replace({"": None}) #для таблиув user-song-agg убрать столбец like
    bulk_upsert(user_song_agg_df, 'user_song_aggregates' , conn, ['user_id','song_id'], ['plays'] )

def add_song_stats(df, conn): # проверку на соглосовоность типов данных прошел
    song_stats_df =df[df['event_type'].isin(['play', 'like', 'dislile'])].value_counts(subset=['song_id', 'event_type']).unstack(fill_value=0).reset_index().rename(columns={'like':'total_likes','play':'total_plays'}).replace({"": None}) # для таблицы song_stats
    bulk_upsert(song_stats_df, 'song_stats' , conn, ['song_id'], ['total_plays','total_likes'])

def aggregate_stream_events():
    print('Aggregating Stream Events')