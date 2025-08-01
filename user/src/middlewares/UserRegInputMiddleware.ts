import { Request, Response, NextFunction } from 'express';

export const validateUserRegInputMiddleware = (
    req: Request,
    res: Response,
    next: NextFunction
) => {
    const { username, password, email, code } = req.body;

    if (!username) {
        res.status(400).json({ error: 'Missing username' });
        return;
    }
    if (!password) {
        res.status(400).json({ error: 'Missing password' });
        return;
    }
    if (!email) {
        res.status(400).json({ error: 'Missing email' });
        return;
    }
    if (!code) {
        res.status(400).json({ error: 'Missing code' });
        return;
    }
    if (typeof username !== 'string' || typeof password !== 'string' || typeof email !== 'string' || typeof code !== 'string') {
        res.status(400).json({ error: 'invalid type' });
        return;
    }

    next();
};



export const validateForCodeInputMiddleware = (
    req: Request,
    res: Response,
    next: NextFunction
) =>{
    const { email } = req.body;
    if (!email) {
        res.status(400).json({ error: 'Missing email' });
    }
    next();
}