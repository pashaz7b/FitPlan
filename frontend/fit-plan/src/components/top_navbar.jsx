import fit_logo from "/Images/Fit-Logo-Resized.png";

export default function Top_navbar(){
    return(
        <div className="bg-black absolute z-10 text-mintCream w-[75%] h-[100px] rounded-b-[30px] flex justify-center items-center text-[20px] py-[15px] px-[40px] mx-[15%] font-iranyekan">
                    <div className="flex justify-between items-center w-full">
                        <img src={fit_logo} alt="Logo" className="h-[70px]" />
                        <div className="flex justify-center gap-[26px] items-center h-[50px] pt-[15px] text-[20px] font-medium text-center">
                            <a href="./about_us" className="hover:text-superRed transition-all duration-300">فیت‌پلن</a>
                            <a href="./coaches" className="hover:text-superRed transition-all duration-300">مربی‌ها</a>
                            <a href="./podcasts" className="hover:text-superRed transition-all duration-300">پادکست</a>
                            <a href="./articles" className="hover:text-superRed transition-all duration-300">مقالات</a>
                            <a href="./user_login" className="bg-superRed rounded-[10px] px-5 pb-3 hover:bg-crimsonRed transition-all duration-300">ورود</a>
                        </div>
                    </div>
                </div>
    );
}