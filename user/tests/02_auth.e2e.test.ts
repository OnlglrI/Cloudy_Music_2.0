import { request } from './setup';

describe('Auth Endpoints', () => {
    const testUser = {
        email: 'test@example.com',
        password: 'StrongPassword123',
    };

    let refreshToken: string;

    beforeAll(async () => {
        await request
            .post('/api/users/code')
            .send({ email: testUser.email });

        await request
            .post('/api/users/reg')
            .send({
                email: testUser.email,
                username: 'TestUser',
                password: testUser.password,
                code: '123456',
            });
    });

    it('should login and return tokens', async () => {
        const res = await request
            .post('/api/auth/login')
            .send({
                email: testUser.email,
                password: testUser.password,
            });

        expect(res.status).toBe(201);
        expect(res.body).toHaveProperty('accessToken');
        expect(res.body).toHaveProperty('refreshToken');
        refreshToken = res.body.refreshToken;
    });

    it('should refresh tokens', async () => {
        const res = await request
            .post('/api/auth/refresh-token')
            .send({ refreshToken });

        expect(res.status).toBe(200);
        expect(res.body).toHaveProperty('accessToken');
        expect(res.body).toHaveProperty('refreshToken');
        refreshToken = res.body.refreshToken;
    });

    it('should logout user', async () => {
        const acctoken = await request
            .post('/api/auth/refresh-token')
            .send({ refreshToken });
        const accessToken = acctoken.body.accessToken;

        const res = await request
            .delete('/api/auth/logout')
            .set('Authorization', `Bearer ${accessToken}`)
            .send({ refreshToken });

        expect(res.status).toBe(200);
    });

    it('should logout from all sessions', async () => {
        const loginRes = await request
            .post('/api/auth/login')
            .send({
                email: testUser.email,
                password: testUser.password,
            });

        const accessToken = loginRes.body.accessToken;

        const res = await request
            .delete('/api/auth/logout-all')
            .set('Authorization', `Bearer ${accessToken}`);

        expect(res.status).toBe(200);
    });

    // ======= Негативные кейсы =======

    it('should reject login with wrong password', async () => {
        const res = await request.post('/api/auth/login').send({
            email: testUser.email,
            password: 'WrongPassword',
        });

        expect(res.status).toBe(401);
        expect(res.body).toHaveProperty('error');
    });

    it('should reject login with non-existent email', async () => {
        const res = await request.post('/api/auth/login').send({
            email: 'notfound@example.com',
            password: testUser.password,
        });

        expect(res.status).toBe(401);
        expect(res.body).toHaveProperty('error');
    });

    it('should reject refresh with invalid token', async () => {
        const res = await request.post('/api/auth/refresh-token').send({
            refreshToken: 'invalidtoken123',
        });

        expect(res.status).toBe(400);
        expect(res.body).toHaveProperty('message');
    });

    it('should reject logout without access token', async () => {
        const res = await request.delete('/api/auth/logout').send();

        expect(res.status).toBe(401);
    });

    it('should reject logout with invalid access token', async () => {
        const res = await request
            .delete('/api/auth/logout')
            .set('Authorization', 'Bearer fake.jwt.token');

        expect(res.status).toBe(401);
    });
});
