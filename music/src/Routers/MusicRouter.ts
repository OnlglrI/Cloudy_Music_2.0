import express, {Request, Response} from 'express';
import multer from "multer";
import {MusicService} from "../Services/MusicService";


const upload = multer({ storage: multer.memoryStorage() }); // хранение в памяти


const GetMusicRouter = () => {
    const router = express.Router();

    router.get('/', async (req: Request, res: Response) => {
        res.status(200).send('success');
    })

    router.post('/addMusic',upload.single("audio"), async (req: Request, res: Response) => {
        if (!req.file) {
            return res.status(400).json({error: "Файл не получен"});
        }
        const uploaded = await MusicService.addMusic(req.file.buffer,req.file.originalname, req.body.author, req.body.genre, req.body.album );

        if (!uploaded) {
            res.status(401).json({massage:'Cannot save this music.'});
        }else{
            res.status(201).json({massage:'Music Saved Successfully'})
        }
    })

    router.post('/streaming-link/:id([0-9]+)', async (req: Request, res: Response) => {
        const stream = await MusicService.stream(+req.params.id)

        if (!stream) {
            res.status(401).json({massage:'cant create a stream url'});
        }

        res.status(201).json({url:stream})

    })

    router.get('/metadata/:id([0-9]+)', async (req: Request, res: Response) => {
        const metadata = await MusicService.getMetadata(+req.params.id)

        if (!metadata) {
            res.status(404).json({massage:'Not found music'});
        }else {
            res.status(200).json({metadata})
        }
    })

    router.delete('/delete/:id([0-9]+)', async (req: Request, res: Response) => {
        const deleted = await MusicService.deleteMusic(+req.params.id)
        if (!deleted) {
            res.status(404).json({massage:'Not found music'});
        }else{
            res.status(200).json({massage:'Deleted music'})
        }
    })


    router.put('/update/:id([0-9]+)', async (req: Request, res: Response) => {
        const updated = await MusicService.updateMusic(+req.params.id, req.body.name, req.body.author, req.body.album, req.body.genre );
        if (!updated) {
            res.status(404).json({massage:'Not found music'});
        }else {
            res.status(200).json({massage:'Updated music'})
        }
    })

    return router;
}


export default GetMusicRouter;

