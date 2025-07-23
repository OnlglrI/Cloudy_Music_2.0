import {Request} from 'express';


export type RequestWithBody<T> = Request<{},{},T>
export type RequestWithQuery<T> = Request<{},{},{},T>;
export type RequestWithParams<T> = Request<T>;
export type RequestWithParamsAndBody<T, B> = Request<T,{},B>;



export type UserType = {
        id: number;
        username: string;
        email: string;
        password: string;
        salt: string;
        created_at: string;
}






