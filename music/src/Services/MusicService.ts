import {MusicRepo, musicType} from "../Repositories/MusicRepo";


export const MusicService = {
    async addMusic (file:Buffer, fileName:string, author:string, genre:string, album?:string):Promise<boolean> {
        if (!album){
            album = '';
        }

        //const musicName = fileName.substring(0,fileName.lastIndexOf('.'));

        const post = await MusicRepo.addMusicInPostgres(fileName, author, genre, album);

        const domainName = post + '-' + fileName;

        const minio = await MusicRepo.addMusicInMinio(file, domainName);

        return minio;
    },

    async stream(id: number): Promise<string | null> {
        const music = await MusicRepo.findMusicInPostgres(id);

        const domainName = id + '-' + music.name;

        const url = await MusicRepo.createUrl(domainName);

        return url
    },

    async deleteMusic (id: number): Promise<boolean> {
        const music = await MusicRepo.findMusicInPostgres(id);

        const deleteInPost = await MusicRepo.deleteMusicPostgres(id);

        if (deleteInPost) {
            const domainName = id + '-' + music.name;
            await MusicRepo.deleteMusicMinio(domainName)
            return true;
        }else{
            return false;
        }
    },

    async getMetadata (id: number): Promise<musicType | null> {
        const music = await MusicRepo.findMusicInPostgres(id);
        if (!music){
            return null;
        }
        return{
            id: music.id,
            name: music.name.substring(0,music.name.lastIndexOf('.')),
            author: music.author,
            album: music.album,
            genre: music.genre,
            created_at: music.created_at,
        };
    },

    async updateMusic (id: number, name?:string, author?:string, album?:string, genre?:string ): Promise<boolean> {
        const music = await MusicRepo.findMusicInPostgres(id);

        const updated = await MusicRepo.updatePostgres(id, name, author, album, genre);

        if (!!name) {
            const newName = id + '-' + name + music.name.substring(music.name.lastIndexOf('.'))
            await MusicRepo.UpdateMinio(id + '-' + music.name, newName)
        }
        return updated;
    }


}











