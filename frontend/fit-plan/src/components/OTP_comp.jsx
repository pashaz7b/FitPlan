import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

export default function OTP_comp({email}) {

    const [otp, setOTP] = useState("");
    const [showError,setShowError] = useState(false);
    const navigate = useNavigate();
    const { role } = useParams();

    async function resendOTP() {
        if(role === "user"){
            const res = await axios.post(
                "http://iam.localhost/api/v1/users/resendOTP",
                {
                    email: email,
                }
            );
        } else if(role === "coach"){
            const res = await axios.post(
                "http://iam.localhost/api/v1/coach/resendOTP",
                {
                    email: email,
                }
            );
        } else if(role === "admin"){
            const res = await axios.post(
                "http://iam.localhost/api/v1/admin/resendOTP",
                {
                    email: email,
                }
            );
        }
    };

    async function handleOTP(e) {
        e.preventDefault();

        if(!otp){
            setShowError(true);
        } else {
            setShowError(false);
            // console.log("submit sucessful");
            // console.log(role);
            // handleNavigate();
            if(role === "user"){
                const res = await axios.post(
                    "http://iam.localhost/api/v1/users/verifyOTP",
                    {
                        email: email,
                        OTP: otp,
                    }
                );

            } else if(role === "coach"){
                const res = await axios.post(
                    "http://iam.localhost/api/v1/coach/verifyOTP",
                    {
                        email: email,
                        OTP: otp,
                    }
                );

            } else if(role === "admin"){
                const res = await axios.post(
                    "http://iam.localhost/api/v1/admin/verifyOTP",
                    {
                        email: email,
                        OTP: otp,
                    }
                );

            }
            navigate("/");
        }
    };

    // const handleNavigate = (e) => {
    //     if(role == "user"){
    //         navigate("/user_panel");
    //     } else if(role == "coach"){
    //         navigate("/coach_panel");
    //     } else if(role == "admin"){
    //         navigate("/admin_panel");
    //     }
    // };

    return(
        <form onSubmit={handleOTP} className="top-0 mt-5 max-sm:w-[70%] max-md:w-[60%] w-[35%] md:w-[28%] h-[250px] md:h-[px] border border-white rounded-[10px] bg-coal flex flex-col justify-center align-items-center text-center text-[20px]">
            <p className={`text-superRed text-[15px] ${ showError ? "block" : "hidden"}`}>لطفا فیلدهای الزامی را پر کنید</p>
            <label htmlFor="otp_code" className=" justify-start text-right mx-5">کد پنج رقمی</label>
            <p className="text-midtoneGray text-[12px] justify-start text-right px-3 my-2">لطفا کدی که به ایمیلتان فرستادیم را وارد کنید</p>
            <input 
            type="text"
            value={otp}
            onChange={(e) => setOTP(e.target.value)}
            className={`text-center text-[15px] py-2 mx-5 mt-3 bg-coal border rounded-[10px] ${showError ? "border-superRed" : "border-white"}`} />
            <button onClick={resendOTP} className="text-[15px] mt-4">کدی دریافت نکردید؟ <span className="text-superRed">ارسال مجدد</span></button>
            <button type="submit" className="text-mintCream bg-superRed hover:bg-crimsonRed h-[40px] mt-5 text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300">ورود</button>
        </form>
    );
}