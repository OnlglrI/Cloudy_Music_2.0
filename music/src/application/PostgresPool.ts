import {Pool} from 'pg';




export const pool = new Pool({
    user: 'music_user',
    host: process.env.POSTGRES_HOST || 'localhost',
    database: "music_db",
    password: process.env.USER_DB_PASS || 'music_password',
    port: parseInt(process.env.POSTGRES_PORT||'5432' ,10),
});


