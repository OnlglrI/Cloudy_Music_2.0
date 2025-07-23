import express from "express";
import {pool} from './application/PosgresConnect'
import {UsersRoute} from "./Routes/UsersRoute";



const app = express();
app.use(express.json());


app.get("/", (req: express.Request, res: express.Response) => {
    res.send("Hello!!!!sss!!!1");
})

app.use('/api/users', UsersRoute());


const PORT = Number(process.env.PORT) || 8080;


app.listen(PORT,'0.0.0.0', () => {
    console.log(`Listening on port ${PORT}`)
});


process.on('SIGINT', async () => {
    console.log('Остановка сервера, закрытие соединения с БД...');
    await pool.end();
    process.exit(0);
})