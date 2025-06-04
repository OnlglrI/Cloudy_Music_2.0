-- Создаем схемы
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS "user";
CREATE SCHEMA IF NOT EXISTS music;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Создаем пользователей с паролями
CREATE USER auth_user WITH PASSWORD 'auth_password';
CREATE USER user_user WITH PASSWORD 'user_password';
CREATE USER music_user WITH PASSWORD 'music_password';
CREATE USER analytics_user WITH PASSWORD 'analytics_password';

-- Даем права на использование схем (USAGE) и все привилегии на таблицы (ALL PRIVILEGES)
GRANT USAGE ON SCHEMA auth TO auth_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA auth TO auth_user;

GRANT USAGE ON SCHEMA "user" TO user_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "user" TO user_user;

GRANT USAGE ON SCHEMA music TO music_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA music TO music_user;

GRANT USAGE ON SCHEMA analytics TO analytics_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO analytics_user;

-- Даем права на создание объектов (включая таблицы) в своих схемах
GRANT CREATE ON SCHEMA auth TO auth_user;
GRANT CREATE ON SCHEMA "user" TO user_user;
GRANT CREATE ON SCHEMA music TO music_user;
GRANT CREATE ON SCHEMA analytics TO analytics_user;

-- Настраиваем права по умолчанию для новых таблиц, создаваемых этими пользователями
ALTER DEFAULT PRIVILEGES IN SCHEMA auth GRANT ALL ON TABLES TO auth_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA "user" GRANT ALL ON TABLES TO user_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA music GRANT ALL ON TABLES TO music_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT ALL ON TABLES TO analytics_user;
