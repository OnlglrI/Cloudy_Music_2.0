import {pool} from '../application/PosgresConnect';
import {refreshType} from "../types";







export const AuthRepository = {
    async saveToken(userId:string, refreshToken:string, userAgent:string, ip:string, expiresAt:Date): Promise<Number> {
        const result = await pool.query(
            `INSERT INTO refresh_tokens (user_id, token, user_agent, ip_address, expires_at)
            VALUES ($1, $2, $3, $4, $5)`,
            [userId, refreshToken, userAgent, ip, expiresAt]);

        return result.rowCount || 0;

    },
    async findValidToken(token: string, userId: string) {
        const result = await pool.query(
            `SELECT * FROM refresh_tokens WHERE token = $1 AND user_id = $2 AND expires_at > now()`,
            [token, userId]
        );
        return result.rows[0] as refreshType;
    },
    async deleteToken(token: string) {
        const res = await pool.query(`DELETE FROM refresh_tokens WHERE token = $1`, [token]);

        return res.rowCount === 1;
    },
    async deleteExpiredTokens() {
        await pool.query(`DELETE FROM refresh_tokens WHERE expires_at < now()`);
    },

    async deleteTokenForUser(userId:number) {
        const res = await pool.query('DELETE FROM refresh_tokens WHERE user_id = $1', [userId]);
        if (!res.rowCount) {
            return false;
        }
        return res.rowCount >= 1;
    }


}
