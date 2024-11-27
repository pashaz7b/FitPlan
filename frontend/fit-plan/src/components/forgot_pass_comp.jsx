import React, {useState} from "react";

export default function Forgot_pass_comp({role}) {
    
    const [password, setPassword] = useState("");
    const [showError, setShowError] = useState(false);
    
    const handleRefresh = () =>{
        window.location.reload();
    }
    
    const handleSubmit = (e) =>{
        e.preventDefault();
    
        if (!password){
            setShowError(true);
        } else {
            setShowError(false);
    
            console.log("Submit successful!");
        }
    };

    return(
        <form onSubmit={handleSubmit} className="top-0 w-[35%] md:w-[28%] h-[400px] md:h-[px] border border-white rounded-[10px] bg-coal flex flex-col justify-around align-items-center text-center text-[20px]">
            <p className="text-superRed text-[15px] top-10">گذرواژه موقتی که به ایمیلتان فرستادیم را وارد کنید</p>
            <div className="flex flex-col justify-center gap-[30px] mb-[30px]">
                <p className={`text-superRed text-[15px] ${ showError ? "block" : "hidden"}`}>لطفا فیلدهای الزامی را پر کنید</p>
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

                <a href="/forgot_password" className="my-2 text-[15px]">
                     ایمیلی دریافت نکردید؟  <span><button onClick={handleRefresh} className="text-superRed">ارسال مجدد</button></span>
                </a>

                <button type="submit" className="text-mintCream bg-superRed hover:bg-crimsonRed h-[40px] text-[20px] font-medium sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300">
                    ورود
                </button>
            </div>

        </form>
    );
}