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

-- Даем права на базы и схемы

-- Подключаемся к каждой базе и создаем схемы и права, например для auth_db:
\c auth_db

CREATE SCHEMA IF NOT EXISTS auth;

GRANT USAGE ON SCHEMA auth TO auth_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA auth TO auth_user;
GRANT CREATE ON SCHEMA auth TO auth_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA auth GRANT ALL ON TABLES TO auth_user;

-- Аналогично для других баз:

\c user_db
CREATE SCHEMA IF NOT EXISTS "user";
GRANT USAGE ON SCHEMA "user" TO user_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "user" TO user_user;
GRANT CREATE ON SCHEMA "user" TO user_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA "user" GRANT ALL ON TABLES TO user_user;

\c music_db
CREATE SCHEMA IF NOT EXISTS music;
GRANT USAGE ON SCHEMA music TO music_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA music TO music_user;
GRANT CREATE ON SCHEMA music TO music_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA music GRANT ALL ON TABLES TO music_user;

\c analytics_db
CREATE SCHEMA IF NOT EXISTS analytics;
GRANT USAGE ON SCHEMA analytics TO analytics_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO analytics_user;
GRANT CREATE ON SCHEMA analytics TO analytics_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT ALL ON TABLES TO analytics_user;

\c playlist_db
CREATE SCHEMA IF NOT EXISTS playlist;
GRANT USAGE ON SCHEMA playlist TO playlist_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA playlist TO playlist_user;
GRANT CREATE ON SCHEMA playlist TO playlist_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA playlist GRANT ALL ON TABLES TO playlist_user;

-- Создаем базу данных и пользователя для Kong
-- 1. Создаём базу и пользователя
CREATE USER kong_user WITH PASSWORD 'kong_password';

-- 2. Даем доступ к базе (это делается до подключения!)
GRANT ALL PRIVILEGES ON DATABASE kong TO kong_user;

-- 3. Подключаемся к базе
\c kong

-- 4. Даем права на схему public и будущие объекты
GRANT USAGE ON SCHEMA public TO kong_user;
GRANT CREATE ON SCHEMA public TO kong_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO kong_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO kong_user;
