import { request } from './setup';

describe('User Endpoints', () => {
    const email = 'newuser@example.com';
    const username = 'NewUser';
    const password = 'TestPassword1';

    it('should request verification code', async () => {
        const res = await request
            .post('/api/users/code')
            .send({ email });

        expect(res.status).toBe(201);
    });

    it('should register user', async () => {
        const res = await request
            .post('/api/users/reg')
            .send({
                email: email,
                username: username,
                password: password,
                code: '123456',
            });

        expect(res.status).toBe(201);
    });

    it('should not register with wrong code', async () => {
        const res = await request
            .post('/api/users/reg')
            .send({
                email: 'wrongcode@example.com',
                username: 'FailUser',
                password: 'AnotherPass1',
                code: '000000',
            });

        expect(res.status).toBe(400);
        expect(res.body).toHaveProperty('message');
    });

    it('should delete user', async () => {
        const loginRes = await request
            .post('/api/auth/login')
            .send({ email: email, password: password });

        const accessToken = loginRes.body.accessToken;

        const res = await request
            .delete('/api/users/delete')
            .set('Authorization', `Bearer ${accessToken}`);

        expect(res.status).toBe(200);
    });

    it('should not delete user without token', async () => {
        const res = await request.delete('/api/users/delete');

        expect(res.status).toBe(401);
    });



});


// describe('Negative Cases', () => {
//
//
//     it('should not register with weak password', async () => {
//         await request
//             .post('/api/users/code')
//             .send({ email: 'weakpass@example.com' });
//
//         const res = await request
//             .post('/api/users/reg')
//             .send({
//                 email: 'weakpass@example.com',
//                 username: 'WeakUser',
//                 password: '123',
//                 code: '123456',
//             });
//
//         expect(res.status).toBe(400);
//         expect(res.body).toHaveProperty('message');
//     });
//
// });



