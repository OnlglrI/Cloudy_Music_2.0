import type { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

// Аутентификация в стиле user-сервиса:
// - Проверяем наличие Authorization: Bearer <token>
// - Верифицируем токен тем же секретом JWT_SECRET (или AUTH_JWT_SECRET)
// - Кладём информацию о пользователе в req.user (email и/или id из payload)

const JWT_SECRET = process.env.JWT_SECRET || process.env.AUTH_JWT_SECRET || '';

export function requireAuth() {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      const auth = req.headers.authorization;
      if (!auth || !auth.startsWith('Bearer ')) {
        return res.status(401).send('Unauthorized');
      }

      if (!JWT_SECRET) {
        // Лучше явно упасть 500, чтобы не вводить в заблуждение
        return res.status(500).send('JWT secret is not configured on server');
      }

      const token = auth.split(' ')[1];
      const payload = jwt.verify(token, JWT_SECRET) as { email?: string; userId?: number | string; id?: number | string };

      const userEmail = payload.email;
      const userId = payload.userId ?? payload.id;

      if (!userEmail && !userId) {
        return res.status(401).send('Unauthorized');
      }

      (req as any).user = { email: userEmail, id: userId };
      return next();
    } catch (error) {
      return res.status(401).send('Unauthorized');
    }
  };
}

export type AuthenticatedRequest = Request & { user?: { email?: string; id?: number | string } };
