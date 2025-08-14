import {pool} from "../application/PostgresPool";
import minioClient from "../application/MinioPool";

const BUCKET = process.env.BUCKET || 'musics';

export type musicType ={
    id:number,
    name:string,
    author:string,
    album:string,
    genre:string,
    created_at:string,
}


export const MusicRepo = {
    async addMusicInPostgres(name:string, author:string, genre:string, album:string):Promise<string> {
        const result = await pool.query(
            `INSERT INTO musics (name, author, album, genre) 
            VALUES($1, $2, $3, $4)
            RETURNING id`,
            [name,author,album, genre]);

        return result.rows[0].id;
    },
    async addMusicInMinio(file:Buffer, name:string):Promise<boolean> {
        try {
            const res = await minioClient.putObject(BUCKET, name, file);
            return true
        }catch(err) {
            console.error(err);
            return false;
        }
    },

    async findMusicInPostgres(id:number):Promise<musicType> {
        const res = await pool.query(
            `SELECT * FROM musics
            WHERE id = $1`,
            [id]
        )
        return res.rows[0] as musicType;
    },

    async createUrl(name:string):Promise<string | null> {
        try {
            const res = await minioClient.presignedGetObject(BUCKET, name, 10 * 60);
            return res
        }catch(err) {
            console.error(err);
            return null;
        }
    },

    async deleteMusicPostgres(id:number):Promise<boolean> {
        const res = await pool.query(
            `DELETE FROM musics
            WHERE id = $1`,
            [id]
        )

        return res.rowCount === 1;
    },

    async deleteMusicMinio(name:string):Promise<void> {
        await minioClient.removeObject(BUCKET, name);
    },


    async updatePostgres(id:number, name?:string, author?:string, album?:string, genre?:string ):Promise<boolean> {
        const fields:string[] = [];
        const params: any[] = [];

        const musicName = (await this.findMusicInPostgres(id)).name;

        const a = musicName.substring(musicName.lastIndexOf('.'));

        const updates: Record<string, any> = { name, author, album, genre };

        Object.entries(updates).forEach(([key, value]) => {
            if (value !== undefined) {
                if (key == 'name') value += a;
                fields.push(`${key} = $${fields.length + 1}`);
                params.push(value);
            }
        });

        if (fields.length === 0) return false;
        params.push(id);
        const query = `UPDATE musics SET ${fields.join(", ")} WHERE id = $${fields.length + 1}`;

        const result = await pool.query(query, params);

        return !!result.rowCount;
    },

    async UpdateMinio(oldName:string, newName:string):Promise<void> {
        await minioClient.copyObject(BUCKET,newName, `${BUCKET}/${oldName}`);
        await minioClient.removeObject(BUCKET, oldName);
    }

}