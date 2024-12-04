import OTP_comp from "../components/OTP_comp";
import fit_logo from "/Images/Fit-Logo-Resized.png";

export default function Otp_page() {
    return(
        <div className="bg-black h-screen flex flex-col justify-center items-center sm:text-[13px] lg:text-[25px] text-mintCream font-iranyekan">
            <a href="/landing" className="sm:w-[40%] md:w-[25%] lg:w-[17%] sm:h-[150px] md:h-[100px] lg:h-[80px] mb-5">
                <img 
                    src={fit_logo} 
                    className="object-contain object-center"
                    alt="logo" 
                />
            </a>
            <OTP_comp />
        </div>
    );
}