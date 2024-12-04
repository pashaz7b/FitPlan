import React, {useState} from "react";
import { useNavigate } from "react-router-dom";

export default function Login_component({role}) {
    
    const [phoneOrMail, setPhoneOrMail] = useState("");
    const [password, setPassword] = useState("");
    const [showError, setShowError] = useState(false);
    const [mailError, setMailError] = useState(false);
    const navigate = useNavigate();
    
    const handleSubmit = (e) =>{
        e.preventDefault();
        handleMail();
    
        if (!phoneOrMail || !password){
            setShowError(true);
        } else {
            setShowError(false);
    
            console.log("Submit successful!");
            navigate(`/otp_page/${role}`);
        }
    };

    const handleMail = (e) => {
        if (!/^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com)$/.test(phoneOrMail)) {
          setMailError(true);
          console.log(setPhoneOrMail);
        } else {
          setMailError(false);
        }
      };

    return(
        <form onSubmit={handleSubmit} className="top-0 w-[35%] md:w-[28%] h-[400px] md:h-[px] border border-white rounded-[10px] bg-coal flex flex-col justify-center align-items-center text-center text-[20px]">
            <p className={`text-superRed text-[15px] ${ showError ? "block" : "hidden"}`}>لطفا فیلدهای الزامی را پر کنید</p>
            <div className="my-3 w-[90%] mx-auto flex flex-col justify-start text-right">
                <label className="text-[15px] mb-2" htmlFor="phoneOrMail">
                    شماره تماس یا آدرس ایمیل
                </label>
                <p className={`text-[12px] text-superRed ${mailError ? "block" : "hidden"}`}>لطفا آدرس ایمیل یاهو یا جیمیل وارد کند</p>
                <input 
                type="text" 
                value={phoneOrMail} 
                onChange={(e) => setPhoneOrMail(e.target.value)}
                className={`text-center text-[15px] py-2 bg-coal border rounded-[10px] ${showError && !phoneOrMail ? "border-superRed" : "border-white"}`} 
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))" 
                placeholder="آدرس ایمیل یاهو یا جیمیل" />
            </div>

            <div className="my-3 w-[90%] mx-auto flex flex-col justify-start text-right">
                <label className="text-[15px] mb-2" htmlFor="password">
                    گذرواژه
                </label>
                <input 
                type="text" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                className={`text-center text-[15px] py-2 bg-coal border rounded-[10px] ${showError && !password ? "border-superRed" : "border-white"}`} 
                placeholder="**********" />
            </div>

            <a href={`/forgot_password/${role}`} className="my-2 text-[15px] hover:text-superRed transition-all duration-300">
                گذرواژه خود را فراموش کرده‌اید؟
            </a>

            <a href="/user_signup" className="my-2 mb-3 text-[15px] hover:text-superRed transition-all duration-300">
                حساب کاربری ندارید؟
            </a>

            <button type="submit" className="text-mintCream bg-superRed hover:bg-crimsonRed h-[40px] text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300">
                <a href={`/otp_page/${role}`}>ورود</a>
            </button>

        </form>
    );
}