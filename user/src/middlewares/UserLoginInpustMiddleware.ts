import {Request, Response, NextFunction} from "express";
import {UsersService} from "../domain/UsersService";
import {AuthService} from "../domain/AuthService";






export const validateUserLoginInputMiddleware = (req:Request, res:Response, next:NextFunction) => {
    const {email, password} = req.body;
    if (!email || !password) {
        res.status(400).send('Email or password is required');
        return;
    }
    next();
}



export const inputUserMiddleware = async (req:Request, res:Response, next:NextFunction) => {
    if (!req.headers.authorization){
        res.status(401).send('Unauthorized');
        return
    }
    const token = req.headers.authorization.split(' ')[1];
    try {
        const userEmail = await AuthService.verifyAccessToken(token); // Верификация токена
        if (userEmail) {
            req.user = await UsersService.FindUserByEmail(userEmail); // Получаем пользователя по ID
            next();
            return // Переходим к следующему middleware или обработчику
        }
    } catch (error) {
        // Если ошибка при верификации токена
        res.status(401).send('Unauthorized');
        return
    }
    res.status(401).send('Unauthorized');
    // Если нет userId, отправляем ответ Unauthorized
    return
};