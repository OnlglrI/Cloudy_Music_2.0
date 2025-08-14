import express, {Request, Response} from 'express';
import {UsersService} from "../domain/UsersService";
import {
    validateEmailInputMiddleware,
    validateUserRegInputMiddleware,
} from "../middlewares/UserRegInputMiddleware";
import {inputValidationMiddleware} from "../middlewares/ErorrsMiddleware";
import {inputUserMiddleware} from "../middlewares/UserLoginInpustMiddleware";





export const UsersRoute = () => {
    const router = express.Router();

    router.post('/reg',validateUserRegInputMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const createdUser = await UsersService.createUser(req.body.username, req.body.password, req.body.email, req.body.code);

        if (!createdUser){
            res.status(400).send({message:"User already exists"});
        }

        res.status(201).send("User already exists");
    })
    router.post('/code', validateEmailInputMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const createdCode = await UsersService.createCode(req.body.email);

        if (!createdCode) {
            res.status(400).send('Code not created');
            return;
        }

        res.status(201).send('Code created');
    });

    router.delete('/delete',inputUserMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const deleted = await UsersService.DeleteUserByEmail(req.user!.id);


        if (deleted){
            res.status(200).send("User Deleted");
        }else {
            res.status(404).send({message:"User Not Found"});
        }

    });

    router.put('/update/password',inputUserMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const updated = await UsersService.updateUserPassword(req.user!.id, req.body.password);

        if (updated){
            res.status(200).send("Password Updated");
        }else {
            res.status(404).send({message:"User Not Found"});
        }

    });

    router.put('/update/username',inputUserMiddleware, inputValidationMiddleware, async (req:Request, res:Response) => {
        const updated = await UsersService.updateUserName(req.user!.id, req.body.username);

        if (updated){
            res.status(200).send("Username Updated");
        }else {
            res.status(404).send({message:"User Not Found"});
        }

    });



    return router;
}







