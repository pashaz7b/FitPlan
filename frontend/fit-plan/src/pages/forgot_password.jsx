import { useEffect, useState } from "react";
import Forgot_pass_comp from "../components/forgot_pass_comp";
import fit_logo from "/Images/Fit-Logo-Resized.png"
import { BrowserRouter as Router, Routes, Route, useParams, useNavigate } from "react-router-dom";

export default function Forgot_password() {
    const { role } = useParams();
    
    
    useEffect(() => {
        const roles = ["user", "coach", "admin"];
        const isRoleValid = roles.includes(role);
        if (isRoleValid){
            console.log(role);
        } else {
            console.log("Invalid Role");
        }


    }, [])

    return(
        <div className="bg-black h-screen flex flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan">
            <a href="/landing" className="sm:w-[40%] md:w-[25%] lg:w-[17%] sm:h-[150px] md:h-[100px] lg:h-[80px] mb-[30px]">
                <img 
                    src= {fit_logo} 
                    className="object-contain object-center"
                    alt="logo" 
                />
            </a>
            <Forgot_pass_comp role={role}/>
        </div>
    );
}