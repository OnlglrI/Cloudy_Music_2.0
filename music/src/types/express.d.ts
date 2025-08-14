// Дополняем типы Express, чтобы Request имел поле user
import 'express-serve-static-core';

declare global {
  namespace Express {
    interface UserPayload {
      email?: string;
      id?: number | string;
    }
    interface Request {
      user?: UserPayload;
    }
  }
}

export {};
