import { pool } from '../src/application/PosgresConnect'; // путь подгони под себя
import redis from '../src/application/RedisCacheConnection'; // если ты экспортируешь redis клиент
import {app} from '../src/index';
const supertest = require('supertest');

export const request = supertest(app);

beforeAll(async () => {
    // если нужно очистить базу перед тестами
    await pool.query(`DELETE FROM refresh_tokens`);
    await pool.query(`DELETE FROM users`);
    // очистка Redis (осторожно в реальной среде!)
    //await redis.flushall();
});

afterAll(async () => {
    await pool.end();
    await redis.quit();
});