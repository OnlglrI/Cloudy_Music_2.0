import pandas as pd
import psycopg2  #

PG_HOST = 'postgres'
PG_PORT = 5432
PG_DB = 'music'
PG_USER = 'admin'
PG_PASSWORD = 'admin'

conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    dbname=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD
)

def process_messages():

        # Создаём DataFrame из собранных данных
        df = pd.DataFrame(all_data)
        transform_and_store(df)



def transform_and_store(df: pd.DataFrame):
    print("записи прочтены и переданы в виде dataframe")
    add_likes(df,conn) #работает
    add_dislikes(df,conn)  #работает
    add_playlists(df,conn) #работает
    add_listen_history(df,conn) #почти работает нету duration
    add_user_song_aggregate(df,conn) #рабоатет
    add_song_stats(df,conn) #рабоатет



if __name__ == "__main__":
    df = process_messages()