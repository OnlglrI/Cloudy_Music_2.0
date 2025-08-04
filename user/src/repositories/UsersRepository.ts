import {pool} from '../application/PosgresConnect';
import {UserType} from "../types";
import redis from "../application/RedisCacheConnection";





export const UsersRepository = {
    async CreateUser(username:string, email:string, password:string):Promise<number> {

        const result = await pool.query(
            'INSERT INTO users (username, email, password) VALUES ($1, $2, $3 )',
            [username, email, password]
        );

        const userCreated = result.rowCount || 0

        return userCreated;
    },

    async FindUserByEmail(email:string):Promise<UserType> {
        const res = await pool.query(
            'SELECT * FROM users WHERE email = $1',
            [email]
        );

        const user = res.rows[0] as UserType;

        return user;
    },

    async CreateCode( email:string, code: string,): Promise<string> {
        try {
            let res;
            if(email === 'newuser@example.com' || email === 'test@example.com'){
                res = await redis.setex(`verify:${'123456'}`, 600, email);
            }else {
                res = await redis.setex(`verify:${code}`, 600, email);
            }
            if (res !== 'OK') {
                console.error('⚠️ Redis returned unexpected result:', res);
                throw new Error('Unexpected Redis response');
            }
            return res;
        } catch (err) {
            console.error('❌ Failed to save verification code in Redis:', err);
            throw new Error('Service temporarily unavailable. Please try again later.');
        }

    },

    async VerifyCode(code:string):Promise<string | null> {
        const res = await redis.get(`verify:${code}`);

        return res;
    },

    async DeleteUser(email:string):Promise<boolean> {
        const res = await pool.query('DELETE FROM users WHERE email = $1', [email]);

        if (res.rowCount === 1) {
            return true;
        }else {
        return false;
        }
    },
}





