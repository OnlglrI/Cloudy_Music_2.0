import express, {Request, Response} from 'express';
import {UsersService} from "../domain/UsersService";
import {validateForCodeInputMiddleware, validateUserRegInputMiddleware} from "../middlewares/UserRegInputMiddleware";
import {inputValidationMiddleware} from "../middlewares/ErorrsMiddleware";





export const UsersRoute = () => {
    const router = express.Router();

    router.post('/reg',validateUserRegInputMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const createdUser = await UsersService.createUser(req.body.username, req.body.password, req.body.email, req.body.code);

        if (!createdUser){
            res.status(400).send("User already exists");
        }

        res.status(201).send("User already exists");
    })
    router.post('/code', validateForCodeInputMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const createdCode = await UsersService.createCode(req.body.email);

        if (!createdCode) {
            res.status(400).send('Code not created');
            return;
        }

        res.status(201).send('Code created');
    });



    return router;
}







