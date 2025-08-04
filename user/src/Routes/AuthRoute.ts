import express, { Request, Response } from 'express';
import {AuthService} from "../domain/AuthService";
import {inputUserMiddleware, validateUserLoginInputMiddleware} from "../middlewares/UserLoginInpustMiddleware";
import {inputValidationMiddleware} from "../middlewares/ErorrsMiddleware";
import {body} from "express-validator";





export const AuthRoute = () =>{
    const router = express.Router();


    router.post('/login',validateUserLoginInputMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {

        const verify = await AuthService.login(req.body.email, req.body.password, req);

        if (!verify) res.status(401).send({error:'Wrong login or password'});
        else{
            res.status(201).send(verify);
        }
    })


    router.post('/refresh-token', body('refreshToken').notEmpty().withMessage('refreshToken is required'), inputValidationMiddleware, async (req:Request, res:Response) => {
        const { refreshToken } = req.body;
        const tokens = await AuthService.refreshToken(refreshToken, req);
        if (!tokens) res.status(400).json({ message: 'Invalid refresh token' });
        res.status(200).json(tokens);
    })


    router.delete('/logout',body('refreshToken').notEmpty().withMessage('refreshToken is required'),inputUserMiddleware,  inputValidationMiddleware, async (req:Request, res:Response) => {
        const deleted = await AuthService.deleteToken(req.body.refreshToken)

        if (!deleted) res.status(401).json({ message: 'Invalid refresh token' });
        res.status(200).json("You have logged out of your account");
    })


    router.delete('/logout-all',inputUserMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const deleted = await AuthService.deleteUserTokens(req.user!.id)

        if (!deleted) res.status(401).json({ message: 'No sessions available' });
        res.status(200).json("You have logged out of all your sessions");
    })



    return router
}






