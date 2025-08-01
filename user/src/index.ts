import express, {Request, Response} from "express";
import {pool} from './application/PosgresConnect'
import {UsersRoute} from "./Routes/UsersRoute";
import {AuthRoute} from "./Routes/AuthRoute";
import {inputUserMiddleware} from "./middlewares/UserLoginInpustMiddleware";
import {inputValidationMiddleware} from "./middlewares/ErorrsMiddleware";



const app = express();
app.use(express.json());


app.get("/", (req:Request, res:Response) => {
    res.send("Hello!!!!sss!!!1");
})

app.use('/api/users', UsersRoute());

app.use('/api/auth', AuthRoute());

app.get('/api/login',inputUserMiddleware, inputValidationMiddleware, (req: Request, res:Response) => {
    res.status(200).send("verify");
} )


const PORT = Number(process.env.USER_PORT) || 8080;


app.listen(PORT,'0.0.0.0', () => {
    console.log(`Listening on port ${PORT}`)
});


process.on('SIGINT', async () => {
    console.log('Остановка сервера, закрытие соединения с БД...');
    await pool.end();
    process.exit(0);
})