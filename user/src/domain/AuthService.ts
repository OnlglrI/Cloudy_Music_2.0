import {UsersRepository} from "../repositories/UsersRepository";
import {UserType} from "../types";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import {Request, Response} from "express";
import {AuthRepository} from "../repositories/AuthRepository";

const ACCESS_SECRET = process.env.ACCESS_SECRET || 'lox';
const REFRESH_SECRET = process.env.REFRESH_SECRET || '12345';

export const AuthService = {
    async login(email: string, password: string, req:Request): Promise<false | {accessToken:string, refreshToken:string}> {
        const user = await UsersRepository.FindUserByEmail(email);
        if (!user) return false;

        const verify = await bcrypt.compare(password, user.password)
        if (!verify) return false;

        const tokens = await this.generateToken(user, req);

        return tokens;

    },
    async generateToken(user:UserType, req:Request){
        const accessToken = jwt.sign({userId:user.id, userEmail:user.email}, ACCESS_SECRET, {expiresIn: '15m'});
        const refreshToken = jwt.sign({ userId: user.id, userEmail:user.email }, REFRESH_SECRET, { expiresIn: '30d' });

        const ip = req.ip || "Unknown";
        const userAgent = req.headers['user-agent'] || 'Unknown';
        const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);

        const saved =  await AuthRepository.saveToken(String(user.id), refreshToken, userAgent, ip, expiresAt);

        if (!saved) return false;

        return {accessToken, refreshToken};
    },

    async refreshToken(refreshToken:string, req:Request){
        try{
            const payload = jwt.verify(refreshToken, REFRESH_SECRET) as { userId: string, userEmail: string };
            const existingToken = await AuthRepository.findValidToken(refreshToken, payload.userId);
            if (!existingToken) return null;

            // Удалим старый и создадим новый
            await AuthRepository.deleteToken(refreshToken);
            const user = await UsersRepository.FindUserByEmail(payload.userEmail);
            const tokens = await this.generateToken(user, req);
            return tokens;
        }catch(err){
            console.error('❌ Refresh token verification failed:', err);
            return false;
        }

    },

    async verifyAccessToken(accessToken:string) {
        try {
            const userInfo = jwt.verify(accessToken, ACCESS_SECRET) as {userId:string, userEmail:string}; ;
            return userInfo.userEmail;
        }catch (e) {
            return null;
        }
    },

    async deleteToken(refreshToken:string) {
        const deleted = await AuthRepository.deleteToken(refreshToken);

        return deleted;
    },

    async deleteUserTokens(userId:number) {
      const deleted = await AuthRepository.deleteTokenForUser(userId);
      return deleted;
    },

}
