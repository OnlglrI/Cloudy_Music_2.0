import nodemailer from "nodemailer";
import {AuthRepository} from "../repositories/AuthRepository";

const transporter = nodemailer.createTransport({
    service: "Gmail",
    auth: {
        user:"clt.development.studio@gmail.com",
        pass:"t22t12t05",
    }
});




export const AuthService = {


}
