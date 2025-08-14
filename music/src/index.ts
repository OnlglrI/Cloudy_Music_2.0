import 'dotenv/config';
import express, {Request, Response} from "express";
import GetMusicRouter from "./Routers/MusicRouter";



export const app = express();
app.use(express.json());

app.get("/", (req:Request, res:Response) => {
    res.send("Hello world!!!");
})

app.use('/api/music', GetMusicRouter());




const port = Number(process.env.MUSIC_PORT) || 8080;


app.listen(port,'0.0.0.0', () => {
    console.log(`Listening on port ${port}`)
});


// process.on('SIGINT', async () => {
//     console.log('Остановка сервера, закрытие соединения с БД...');
//     await pool.end();
//     process.exit(0);
// })