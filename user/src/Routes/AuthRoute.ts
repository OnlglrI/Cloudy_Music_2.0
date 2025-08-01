import express, { Request, Response } from 'express';
import {AuthService} from "../domain/AuthService";
import {validateUserLoginInputMiddleware} from "../middlewares/UserLoginInpustMiddleware";
import {inputValidationMiddleware} from "../middlewares/ErorrsMiddleware";
import {body} from "express-validator";





export const AuthRoute = () =>{
    const router = express.Router();


    router.post('/login',validateUserLoginInputMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {

        const verify = await AuthService.login(req.body.email, req.body.password, req);

        if (!verify) res.status(401).send('Wrong login or password');
        else{
            res.status(201).send(verify);
        }
    })


    router.post('/refresh-token', body('refreshToken').notEmpty().withMessage('refreshToken is required'), inputValidationMiddleware, async (req:Request, res:Response) => {
        const { refreshToken } = req.body;
        const tokens = await AuthService.refreshToken(refreshToken, req);
        if (!tokens) res.status(401).json({ message: 'Invalid refresh token' });
        res.status(200).json(tokens);
    })



    return router
}






