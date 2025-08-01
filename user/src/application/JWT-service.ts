import jwt from 'jsonwebtoken';
import {UserType} from "../types";


const ACCESS_SECRET = process.env.ACCESS_SECRET || 'lox';
const REFRESH_SECRET = process.env.REFRESH_SECRET || '12345';



export const JwtService = {
    async generateToken(user:UserType) {
        const accessToken = jwt.sign({userId:user.id, userEmail:user.email}, ACCESS_SECRET, {expiresIn: '15m'});
        const refreshToken = jwt.sign({ userId: user.id, userEmail:user.email }, REFRESH_SECRET, { expiresIn: '30d' });
        return {accessToken, refreshToken};
    },

    async verifyAccessToken(accessToken:string) {
        try {
            const userId = jwt.verify(accessToken, ACCESS_SECRET) as {userId:string}; ;
            return userId;
        }catch (e) {
            return null;
        }
    },
    async verifyRefreshToken(refreshToken:string) {
        try {
            const user = jwt.verify(refreshToken, REFRESH_SECRET) as { userId: string };
            return {userId: user.userId, refreshToken: refreshToken};
        }catch (e) {
            return null;
        }

    }
}

