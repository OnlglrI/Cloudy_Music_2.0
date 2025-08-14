import { Client } from 'minio';

const minioClient = new Client({
    endPoint: 'localhost',      // или IP, где работает MinIO
    port: 9000,                  // порт по умолчанию
    useSSL: false,               // true, если используется https
    accessKey: process.env.MINIO_ROOT_USER || 'minio',     // замени на свой
    secretKey: process.env.MINIO_ROOT_PASSWORD || 'minio123',     // замени на свой
});

// const exists = await minioClient.bucketExists('musics').catch(() => false);
// if (!exists) {
//     await minioClient.makeBucket('musics');
// }


export default minioClient;