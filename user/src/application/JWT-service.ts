import jwt from 'jsonwebtoken';
import {UserType} from "../types";


const JWT_SECRET = process.env.JWT_SECRET || 'lox';



export const JwtService = {
    async generateToken(user:UserType) {
        return await jwt.sign({userId:user.id}, JWT_SECRET, {expiresIn: '1h'});
    },

    async verifyToken(token:string) {
        try {
            const userId = jwt.verify(token, JWT_SECRET) as {userId:number}; ;
            return userId;
        }catch (e) {
            return null;
        }
    },
}

