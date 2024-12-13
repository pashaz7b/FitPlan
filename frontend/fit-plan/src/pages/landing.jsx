import { useNavigate } from "react-router-dom";
import fit_logo from "/Images/Fit-Logo-Resized.png";
import header_img from "/Images/header-athlete.png";
import where_we_began from "/Images/charles-gaudreault-xXofYCc3hqc-unsplash.jpg";

export default function Landing(){

    const navigate = useNavigate();
    const handleNavigate = (e) =>{
        navigate("./user_login");
    };

    return(
        <>
            <div className="h-full w-full bg-mintCream">
                <div className="absolute z-10 text-mintCream w-[75%] h-[100px] rounded-b-[30px] flex justify-center items-center text-[20px] py-[15px] px-[40px] mx-[15%] font-iranyekan">
                    <div className="flex justify-between items-center w-full">
                        <img src={fit_logo} alt="Logo" className="h-[70px]" />
                        <div className="flex justify-center gap-[26px] items-center h-[50px] pt-[15px] text-[20px] font-medium text-center">
                            <a href="" className="hover:text-superRed transition-all duration-300">فیت‌پلن</a>
                            <a href="" className="hover:text-superRed transition-all duration-300">مربی‌ها</a>
                            <a href="" className="hover:text-superRed transition-all duration-300">پادکست</a>
                            <a href="" className="hover:text-superRed transition-all duration-300">مقالات</a>
                            <a href="" className="bg-superRed rounded-[10px] px-5 pb-3 hover:bg-crimsonRed transition-all duration-300">ورود</a>
                        </div>
                    </div>
                </div>
                <div className="relative z-0 h-[550px] bg-mintCream font-iranyekan">
                    <div
                        className="absolute inset-0 bg-cover bg-center bg-black text-center"
                        style={{
                            clipPath: "polygon(0 0, 100% 0, 100% 10%, 100% 100%, 0 50%)",
                        }}
                    >
                        <div className="relative flex text-white">
                            <img src={header_img} alt="" className="absolute object-contain object-center h-[1200px] top-[20px] right-[200px]" />
                            <div className="absolute right-[710px] top-[110px] text-[70px] font-bold flex flex-col text-right text-mintCream">
                                <p>مثل یک</p>
                                <p><span className="text-superRed">قهرمان</span> بجنگ</p>
                            </div>
                        </div>
                    </div>
                    <div className="relative z-10 h-[152px] flex justify-evenly w-[32%] rounded-[15px] bg-mintCream shadow-[-20px_50px_70px_0px_rgba(197,18,11,0.3)] top-[320px] mx-auto">
                        <div className="group flex flex-col text-center justify-center hover:scale-[120%] transition-all duration-300">
                            <a href="">
                            <svg xmlns="http://www.w3.org/2000/svg" height="56px" viewBox="0 -960 960 960" width="55px" fill="#000000" className="group-hover:fill-superRed mx-auto transition-all duration-300"><path d="M290-595.38V-840q0-12.75 8.63-21.37 8.63-8.63 21.38-8.63 12.76 0 21.37 8.63Q350-852.75 350-840v244.62h55.39V-840q0-12.75 8.62-21.37 8.63-8.63 21.39-8.63 12.75 0 21.37 8.63 8.61 8.62 8.61 21.37v244.62q0 53.69-33.34 92.42-33.35 38.73-82.04 49.27V-120q0 12.75-8.63 21.37Q332.74-90 319.99-90q-12.76 0-21.37-8.63Q290-107.25 290-120v-333.69q-48.69-10.54-82.04-49.27-33.34-38.73-33.34-92.42V-840q0-12.75 8.63-21.37 8.62-8.63 21.38-8.63 12.75 0 21.37 8.63 8.61 8.62 8.61 21.37v244.62H290ZM674.61-410h-73.02q-15.51 0-25.86-10.39-10.34-10.4-10.34-25.76V-680q0-75.39 43.61-132.69Q652.61-870 697.61-870q16.85 0 26.93 12.08 10.07 12.07 10.07 30.31V-120q0 12.75-8.63 21.37Q717.36-90 704.6-90q-12.75 0-21.37-8.63-8.62-8.62-8.62-21.37v-290Z"/></svg>
                            <p className="font-medium group-hover:text-superRed transition-all duration-300">برنامه غذایی</p>
                            </a>
                        </div>
                        <div className="group flex flex-col text-center justify-center hover:scale-[120%] transition-all duration-300">
                            <svg xmlns="http://www.w3.org/2000/svg" height="56px" viewBox="0 -960 960 960" width="55px" fill="#000000" className="group-hover:fill-superRed mx-auto transition-all duration-300"><path d="m801-585-41.77-41.77 24.61-25.61q3.85-3.85 3.85-8.66 0-4.81-3.85-8.65L669.69-783.84q-3.84-3.85-8.65-3.85-4.81 0-8.66 3.85l-25.61 24.61L584-802l26.15-27.15q20.31-20.31 50.08-19.81t50.08 20.81l117.84 117.84q20.31 20.31 20.31 49.58t-20.31 49.58L801-585ZM349.85-132.85q-20.31 20.31-49.58 20.31t-49.58-20.31l-116.3-116.31q-20.7-20.69-20.7-51.11 0-30.42 20.7-51.12L159-376l42.77 42.77-25.23 24.61q-3.85 3.85-3.85 8.66 0 4.81 3.85 8.65l114.77 114.77q3.84 3.85 8.65 3.85 4.81 0 8.66-3.85l24.61-25.23L376-159l-26.15 26.15ZM743-436.92l51.23-51.23q3.85-3.85 3.85-8.85t-3.85-8.85L505.85-794.23q-3.85-3.85-8.85-3.85t-8.85 3.85L436.92-743q-3.84 3.85-3.84 8.65 0 4.81 3.84 8.66l288.77 288.77q3.85 3.84 8.66 3.84 4.8 0 8.65-3.84ZM471.85-165.77l51.23-51.85q3.84-3.84 3.84-8.65 0-4.81-3.84-8.65L234.92-523.08q-3.84-3.84-8.65-3.84-4.81 0-8.65 3.84l-51.85 51.23q-3.85 3.85-3.85 8.85t3.85 8.85l288.38 288.38q3.85 3.85 8.85 3.85t8.85-3.85Zm-17.16-222.46 117.7-117.08-67.08-67.08-117.08 117.7 66.46 66.46Zm59.54 264.61q-20.69 20.7-51.23 20.7-30.54 0-51.23-20.7L123.62-411.77q-20.7-20.69-20.7-51.23 0-30.54 20.7-51.23l51.23-51.62q20.69-20.69 51.11-20.69 30.43 0 51.12 20.69l68.38 68.39 117.7-117.69-68.39-67.77q-20.69-20.69-20.69-51.43 0-30.73 20.69-51.42l51.62-51.61q20.69-20.7 51.11-20.7 30.42 0 51.11 20.7l288.77 288.77q20.7 20.69 20.7 51.11 0 30.42-20.7 51.11l-51.61 51.62q-20.69 20.69-51.42 20.69-30.74 0-51.43-20.69l-67.77-68.39-117.69 117.7 68.39 68.38q20.69 20.69 20.69 51.12 0 30.42-20.69 51.11l-51.62 51.23Z"/></svg>
                            <p className="font-medium group-hover:text-superRed transition-all duration-300">برنامه تمرینی</p>
                        </div>
                        <div className="group flex flex-col text-center justify-center hover:scale-[120%] transition-all duration-300">
                            <svg xmlns="http://www.w3.org/2000/svg" height="56px" viewBox="0 -960 960 960" width="55px" fill="#000000" className="group-hover:fill-superRed mx-auto transition-all duration-300"><path d="M420.38-222.31q-90.38 0-154.03-63.65-63.66-63.66-63.66-154.04 0-12.41 1.58-24.82t3.96-22.26q-4.61 2-10.46 2.62-5.85.61-10.27.61-37.19 0-62.54-25.43-25.34-25.43-25.34-62.26t24.23-62.26q24.22-25.43 61.23-25.43 30.31 0 53.92 17.35 23.62 17.34 31.54 44.04 29.15-27.7 68.38-43.77 39.23-16.08 81.46-16.08h403.85q15.36 0 25.76 10.39 10.39 10.4 10.39 25.76v49.23q0 14.71-9.95 24.66-9.95 9.96-24.66 9.96h-187.7V-440q0 90.7-63.49 154.2-63.49 63.49-154.2 63.49ZM187.31-531.54q17 0 28.5-11.5t11.5-28.5q0-17-11.5-28.5t-28.5-11.5q-17 0-28.5 11.5t-11.5 28.5q0 17 11.5 28.5t28.5 11.5Zm233.13 236.93q60.25 0 102.79-42.6 42.54-42.59 42.54-102.84 0-60.26-42.59-102.8-42.6-42.54-102.85-42.54-60.25 0-102.79 42.6Q275-500.2 275-439.95q0 60.26 42.59 102.8t102.85 42.54Zm.01-73.08q29.86 0 51.05-21.26 21.19-21.26 21.19-51.12 0-29.85-21.26-51.04-21.26-21.2-51.11-21.2-29.86 0-51.05 21.26-21.19 21.26-21.19 51.12 0 29.85 21.26 51.04 21.26 21.2 51.11 21.2Zm-.07-72.31Z"/></svg>
                            <p className="font-medium group-hover:text-superRed transition-all duration-300">مربی‌ها</p>
                        </div>
                    </div>
                </div>
                
            </div>
            {/* sections below the header section */}
            <div className="bg-mintCream w-full h-full text-black font-iranyekan">
                {/* where we began section  */}
                <div className="w-[70%] mx-auto flex justify-center gap-5 pb-[100px] overflow-hidden ">
                    <div className="w-1/2 aspect-video overflow-hidden rounded-[20px] h-[450px]">
                        <img src={where_we_began} alt="A man with six packs" className="object-contain object-center w-full h-full scale-[190%]" />
                    </div>
                    <div className="flex flex-col gap-3 text-right w-1/2">
                        <div className="flex">
                            <div className="w-[5px] h-[60px] bg-superRed ml-4 rounded-[15px]"></div>
                            <p className="font-bold text-[50px]">از کجا شروع کردیم...</p>
                        </div>
                        <p className="leading-10 text-justify text-[22px]">شروع ما از یک علاقه ساده به سلامت و تناسب اندام بود. از جلسات کوچک با دوستان در باشگاه‌های محلی، تا مطالعه عمیق‌تر در مورد تکنیک‌های تمرین و تغذیه، ما قدم به قدم پیشرفت کردیم. هدف اصلی ما از همون اول، ایجاد بستری بود که بتونیم دانسته‌های خودمون رو با دیگران به اشتراک بذاریم و به علاقه‌مندان بدنسازی کمک کنیم تا به بهترین نسخه از خودشون تبدیل بشن. با تلاش‌های مستمر و با انگیزه قوی، این پلتفرم رو راه‌اندازی کردیم تا برای همه قابل دسترس باشه.</p>
                        <div className="text-left">
                            <a href="user_login" className="text-mintCream bg-superRed  py-[10px] px-[10px] rounded-[10px] hover:bg-crimsonRed transition-all duration-300">با ما همراه شوید</a>
                        </div>
                    </div>
                </div>

                {/* Coaches Introduction section */}
                <div className="flex flex-col"></div>

            </div>
        </>
    );
}