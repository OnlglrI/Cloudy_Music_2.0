import bcrypt from 'bcrypt';
import {UsersRepository} from "../repositories/UsersRepository";
import {AuthRepository} from "../repositories/AuthRepository";
import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
    service: "Gmail",
    auth: {
        user:"clt.development.studio@gmail.com",
        pass:"aphn jczi xyiw lwvp",
    },
});




export const UsersService = {
    async createUser(username:string, password:string, email:string, code:string):Promise<boolean> {

        const verifyCode = await UsersRepository.VerifyCode(code);

        if (!verifyCode) {
            return false;
        }
        if(email != verifyCode){
            return false;
        }

        const salt = await bcrypt.genSalt(10);
        const passhash = await this.generateHash(password, salt);

        const createdUser = await UsersRepository.CreateUser(username, email, passhash, salt);

        if (createdUser === 1) {
            return true;
        }else {
            return false;
        }

    },
    async generateHash(password:string, salt:string) {
        const hash = await bcrypt.hash(password, salt);
        return hash;
    },


    async createCode(email: string): Promise<boolean> {
        const code = Math.floor(100000 + Math.random() * 900000).toString(); // 6-значный код
        const CreatedCode = await UsersRepository.CreateCode(email, code);

        if (CreatedCode == "OK") {
            const mail = await transporter.sendMail({
                to: email,
                subject: "Verification",
                text: `Your code has been created: ${code}`,
            })

            return true;
        }
        return false;
    },
}