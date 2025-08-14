// Глобальное дополнение типов Express. Подхватывается благодаря tsconfig.typeRoots: ["./types", "./node_modules/@types"]
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
