import {Pool} from 'pg';




export const pool = new Pool({
    user: 'user_user',
    host: process.env.POSTGRES_HOST,
    database: "user_db",
    password: process.env.USER_DB_PASS || 'user_password',
    port: parseInt(process.env.POSTGRES_PORT||'5432' ,10),
});



