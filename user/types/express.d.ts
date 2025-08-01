import {UserType} from "../src/types";


declare global {
    declare namespace Express {
        interface Request {
            user?:UserType;
        }
    }
}