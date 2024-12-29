import React, { useEffect, useState } from "react";
import Login_component from "../components/login_component";
import fit_logo from "/Images/Fit-Logo-Resized.png";

export default function User_login() {
    const [role, setRole] = useState("user");
    const url = `/user_login?role=${role}`;

    const [activeMode, setActiveMode] = useState("user_submit");
    
    useEffect(()=>{
        setRole("user");

        console.log(role);
    }, [])

    const switchMode = (mode) => {
        setActiveMode(mode);
        onClickFunc(mode);
    };
    const onClickFunc = (pageID) => {
        const userSubmit = document.getElementById("user_submit");
        const coachSubmit = document.getElementById("coach_submit");

        if (userSubmit && coachSubmit) {
            if (pageID == "coach_submit") {
                userSubmit.className = "bg-black h-screen hidden flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan";
                coachSubmit.className = "bg-black h-screen flex flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan";
                setRole("coach");
            } else if (pageID == "user_submit") {
                userSubmit.className = "bg-black h-screen flex flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan";
                coachSubmit.className = "bg-black h-screen hidden flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan";
                setRole("user");
            }
        } else {
            console.error("Element not found");
        }
    };

    return(
        <>
        <div id="user_submit" className="bg-black h-screen flex flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan">
            <a href="/" className="max-sm:w-[70%] max-md:w-[35%] max-lg:w-[30%] max-sm:h-[150px] max-md:h-[100px] max-lg:h-[80px] w-[20%] h-[150px] mb-0">
                <img 
                    src={fit_logo} 
                    className="object-contain object-center"
                    alt="logo" 
                />
            </a>
            <a 
                href="/admin_login"
                className="mb-[28px] font-medium mt-4 hover:scale-110 hover:shadow-lg hover:text-superRed transition-all duration-300"
            >
                ادمین هستم
            </a>
        <div className="p-0 mb-0 max-sm:w-[60%] max-md:w-[40%] max-lg:w-[30%] w-[20%] sm:h-[50px] md:h-[48px] text-[15px] flex justify-around items-center text-center rounded-[15px] border-t border-l border-r border-white rounded-t-[15px] rounded-b-[0px] overflow-hidden">
            <div className="w-[70%] lg:w-[50%] h-[100%] p-[10px] text-ellipsis flex justify-center text-center align-items-center bg-superRed text-black">کاربر هستم</div>
            <button onClick={() => switchMode("coach_submit")} className="w-[70%] lg:w-[50%] h-[100%] p-[10px] text-ellipsis flex justify-center text-center align-items-center">مربی هستم</button>
        </div>
        <Login_component role={role}/>
    </div>
    <div id="coach_submit" className="bg-black h-screen hidden flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan">
        <a href="/" className="sm:w-[40%] md:w-[25%] lg:w-[17%] sm:h-[150px] md:h-[100px] lg:h-[80px] mb-0">
            <img 
                src={fit_logo} 
                className="object-contain object-center"
                alt="logo" 
            />
        </a>
        <a 
            href="/admin_login"
            className="mb-[28px] font-medium mt-4 hover:scale-110 hover:shadow-lg hover:text-superRed transition-all duration-300"
        >
            ادمین هستم
        </a>
        <div className="p-0 mb-0 w-[20%] md:w-[20%] sm:h-[50px] md:h-[48px] text-[15px] flex justify-around items-center text-center rounded-[15px] border-t border-l border-r border-white rounded-t-[15px] rounded-b-[0px] overflow-hidden">
            <button  onClick={() => switchMode("user_submit")} className="w-[70%] lg:w-[50%] h-[100%] p-[10px] text-ellipsis flex justify-center text-center align-items-center">کاربر هستم</button>
            <div className="w-[70%] lg:w-[50%] h-[100%] p-[10px] text-ellipsis flex justify-center text-center align-items-center bg-superRed text-black">مربی هستم</div>
        </div>
        <Login_component role={role} />
    </div>
    
    </>
    
        );
}