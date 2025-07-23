-- Создаем базы данных для сервисов
CREATE DATABASE auth_db;
CREATE DATABASE user_db;
CREATE DATABASE music_db;
CREATE DATABASE analytics_db;
CREATE DATABASE playlist_db;

-- Создаем пользователей с паролями
CREATE USER auth_user WITH PASSWORD 'auth_password';
CREATE USER user_user WITH PASSWORD 'user_password';
CREATE USER music_user WITH PASSWORD 'music_password';
CREATE USER analytics_user WITH PASSWORD 'analytics_password';
CREATE USER playlist_user WITH PASSWORD 'playlist_password';

-- AUTH_DB
\c auth_db

GRANT CONNECT ON DATABASE auth_db TO auth_user;

-- Даем права на public-схему
GRANT USAGE ON SCHEMA public TO auth_user;
GRANT CREATE ON SCHEMA public TO auth_user;

-- Даем права на все таблицы и по умолчанию на новые
ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO auth_user;
ALTER DEFAULT PRIVILEGES GRANT ALL ON SEQUENCES TO auth_user;

-- USER_DB
\c user_db

GRANT CONNECT ON DATABASE user_db TO user_user;

GRANT USAGE ON SCHEMA public TO user_user;
GRANT CREATE ON SCHEMA public TO user_user;

ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO user_user;
ALTER DEFAULT PRIVILEGES GRANT ALL ON SEQUENCES TO user_user;

-- MUSIC_DB
\c music_db

GRANT CONNECT ON DATABASE music_db TO music_user;

GRANT USAGE ON SCHEMA public TO music_user;
GRANT CREATE ON SCHEMA public TO music_user;

ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO music_user;
ALTER DEFAULT PRIVILEGES GRANT ALL ON SEQUENCES TO music_user;

-- ANALYTICS_DB
\c analytics_db

GRANT CONNECT ON DATABASE analytics_db TO analytics_user;

GRANT USAGE ON SCHEMA public TO analytics_user;
GRANT CREATE ON SCHEMA public TO analytics_user;

ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO analytics_user;
ALTER DEFAULT PRIVILEGES GRANT ALL ON SEQUENCES TO analytics_user;

-- PLAYLIST_DB
\c playlist_db

GRANT CONNECT ON DATABASE playlist_db TO playlist_user;

GRANT USAGE ON SCHEMA public TO playlist_user;
GRANT CREATE ON SCHEMA public TO playlist_user;

ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO playlist_user;
ALTER DEFAULT PRIVILEGES GRANT ALL ON SEQUENCES TO playlist_user;

-- KONG
CREATE DATABASE kong;
CREATE USER kong_user WITH PASSWORD 'kong_password';

GRANT CONNECT ON DATABASE kong TO kong_user;

\c kong

GRANT USAGE ON SCHEMA public TO kong_user;
GRANT CREATE ON SCHEMA public TO kong_user;

ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO kong_user;
ALTER DEFAULT PRIVILEGES GRANT ALL ON SEQUENCES TO kong_user;














