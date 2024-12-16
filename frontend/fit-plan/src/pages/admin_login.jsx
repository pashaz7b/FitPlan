import React, { useEffect, useState } from "react";
import Login_component from "../components/login_component";

export default function Admin_login() {
    const [role, setRole] = useState("admin");
    const url = `/admin_login?role=${role}`;

    useEffect(()=>{
        setRole("admin");

        console.log(role);
    }, [])


    return(
        <div className="bg-black h-screen flex flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan">
        <a href="/" className="sm:w-[40%] md:w-[25%] lg:w-[17%] sm:h-[150px] md:h-[100px] lg:h-[80px] mb-11">
            <img 
                src="Images/Fit-Logo-Resized.png" 
                className="object-contain object-center"
                alt="logo" 
            />
        </a>
        {/* <a 
            href="/admin_login"
            className="mb-[28px] font-medium mt-4 hover:scale-110 hover:shadow-lg hover:text-superRed transition-all duration-300"
        >
            ادمین هستم
        </a>
        <div className="p-0 mb-0 w-[20%] md:w-[20%] sm:h-[50px] md:h-[48px] text-[15px] flex justify-around items-center text-center rounded-[15px] border-t border-l border-r border-white rounded-t-[15px] rounded-b-[0px] overflow-hidden">
            <div className="w-[70%] lg:w-[50%] h-[100%] p-[10px] text-ellipsis flex justify-center text-center align-items-center bg-superRed text-black">کاربر هستم</div>
            <a href="/coach_login" className="w-[70%] lg:w-[50%] h-[100%] p-[10px] text-ellipsis flex justify-center text-center align-items-center">مربی هستم</a>
        </div> */}
        <Login_component role={role}/>
    </div>
        
        
    );
}