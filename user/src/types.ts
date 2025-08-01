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
        created_at: string;
}



export type refreshType = {
        id: number;
        user_id: number;
        token: string;
        user_agent: string;
        ip_address: string;
        expires_at: string;
        created_at: string;
}






