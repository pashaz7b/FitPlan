import fit_logo from "/Images/Fit-Logo-Resized.png";
import peoson_svg from "/SVGs/person_24dp_E8EAED_FILL0_wght300_GRAD0_opsz24.svg";
import React, {useState} from "react";

export default function User_signup() {

    const [nameSurname, setNameSurname] = useState("");
    const [birthDate, setBirthDate] = useState("");
    const [imagePreview, setImagePreview] = useState(null);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [gender, setGender ] = useState("آقا");
    const [height, setHeight ] = useState("");
    const [weight, setWeight ] = useState("");
    const [showError, setShowError] = useState(false);
    const [phoneError, setPhoneError] = useState(false);
    const [weightError, setWeightError] = useState(false);
    const [heightError, setHeightError] = useState(false);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if(file){
            const reader = new FileReader();
            reader.onload = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handlePhone = (e) => {
    if (!/^9\d{9}$/.test(phone)) {
      setPhoneError(true);
      console.log();
    } else {
      setPhoneError(false);
    }
  };

    const handleSubmit = (e) => {
        e.preventDefault();
        handlePhone();
        handleHeight(e);
        handleWeight(e);

        if (!nameSurname || !birthDate || !username || !password || !email || !phone || !gender || !height || !weight){
            setShowError(true);
        } else {
            setShowError(false);
            console.log("Submit Successful!")
        }
    };

    const handleWeight = (e) => {
        const value = e.target.value || ""; // Fallback to an empty string if undefined
        const sanitizedValue = value
          .replace(/[^\d.]/g, "") // Allow only numbers and dots
          .replace(/(\..*?)\..*/g, "$1"); // Prevent multiple dots

        if(value == ""){
            setWeightError(true);
        }
        else {
            setWeightError(false);
            setWeight(sanitizedValue);
        }
    };

    const handleHeight = (e) => {
        const value = e.target.value || ""; // Fallback to an empty string if undefined
        const sanitizedValue = value
          .replace(/[^\d.]/g, "") // Allow only numbers and dots
          .replace(/(\..*?)\..*/g, "$1"); // Prevent multiple dots

        if(sanitizedValue == ""){

            setHeightError(true);
        }
        else {
            setHeightError(false);
            setHeight(sanitizedValue);
        }
    };



    return(
        <div className="bg-black h-full pb-[100px] flex flex-col justify-center items-center max-sm:text-[13px] text-[25px] text-mintCream font-iranyekan">
            <a href="/landing" className="sm:w-[40%] md:w-[25%] lg:w-[17%] sm:h-[150px] md:h-[100px] lg:h-[80px] mb-0 mt-[50px]">
                <img 
                    src={fit_logo} 
                    className="object-contain object-center"
                    alt="logo" 
                />
            </a>
        <form onSubmit={handleSubmit} className="sm:w-[95%] w-[90%] flex flex-col gap-[50px] items-center justify-center text-mintCream text-[20px]">
            <p className={`text-superRed text-[20px] mt-11 ${ showError ? "block" : "hidden"}`}>لطفا فیلدهای الزامی را پر کنید</p>
            <div id="identity_info" className="w-[70%] flex flex-col justify-between text-right">
                <p className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto text-superRed text-[30px] font-medium mt-10">اطلاعات هویتی</p>
                <div className="max-sm:flex max-sm:flex-col max-sm:gap-5 max-sm:text-center max-sm:mx-auto flex justify-between align-bottom items-end mt-auto">
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="first_surname" className="mb-3">نام و نام‌خانوادگی</label>
                        <input 
                        type="text"
                        value={nameSurname}
                        onChange={(e) => setNameSurname(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !nameSurname ? "border-superRed" : "border-white"}`} 
                        placeholder="فرداد فریدون"
                        />
                    </div>
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="birthDate" className="mb-3">تاریخ تولد</label>
                        <input 
                        type="text"
                        value={birthDate}
                        onChange={(e) => setBirthDate(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !birthDate ? "border-superRed" : "border-white"}`} 
                        placeholder="1380/8/22"
                        />
                    </div>
                    <div className="max-sm:flex max-sm:flex-col-reverse max-sm:text-center max-sm:mx-auto max-sm:items-center flex justify-between gap-5 align-bottom items-end mt-auto">
                        <label 
                        htmlFor="upload"
                        className="h-[35px] w-auto px-5 text-black bg-mintCream rounded-lg cursor-pointer hover:bg-irishGreen hover:text-mintCream transition">
                        افزودن تصویر
                        </label>
                        <input 
                        type="file"
                        id="upload"
                        accept="image/*"
                        onChange={handleFileChange}
                        className="hidden"
                         />
                         <div className="w-32 h-32 border-[2px] border-white rounded-[15px] flex items-center justify-center"
                         >
                            {imagePreview ? (
                                <img
                                    src={imagePreview}
                                    alt="Preview"
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <img
                                    src={peoson_svg}
                                    alt="Person Icon"
                                    className="w-28 h-28 text-gray-400"
                                />
                            )}
                         </div>
                    </div>
                </div>
            </div>
            <div id="user_info" className="w-[70%] flex flex-col justify-between text-right">
                <p className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto text-superRed text-[30px] font-medium mt-10">اطلاعات کاربری</p>
                <div className="max-sm:flex max-sm:flex-col max-sm:gap-5 max-sm:text-center max-sm:mx-auto flex justify-between align-bottom items-end mt-auto">
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="username" className="mb-3">نام کاربری</label>
                        <input 
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !username ? "border-superRed" : "border-white"}`} 
                        placeholder="FardadFer"
                        />
                    </div>
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="password" className="mb-3">گذرواژه</label>
                        <input 
                        type="text"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !password ? "border-superRed" : "border-white"}`} 
                        placeholder="**********"
                        />
                    </div>
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="mailAddress" className="mb-3">آدرس ایمیل</label>
                        <input 
                        type="text"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !email ? "border-superRed" : "border-white"}`} 
                        placeholder="fardad.frydn@gmail.com"
                        />
                    </div>
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="phoneNumber" className="mb-3">شماره تماس</label>
                        <p className={`text-superRed text-[15px] ${phoneError ? "block" : "hidden"}`}>لطفا شماره تماس را بدون صفر وارد کنید</p>
                        <input 
                        type="text"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !phone ? "border-superRed" : "border-white"}`} 
                        placeholder="9123456789"
                        // pattern="^9\d{9}$"
                        />
                    </div>
                </div>
            </div>
            <div id="bio_info" className="w-[70%] flex flex-col justify-between text-right">
                <p className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto text-superRed text-[30px] font-medium mt-10">اطلاعات بیولوژیکی</p>
                <div className="max-sm:flex max-sm:flex-col max-sm:gap-5 max-sm:text-center max-sm:mx-auto flex justify-evenly align-bottom gap-2 items-end">
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="gender" className="mb-3">جنسیت</label>
                        <select 
                        name="gender" 
                        id="gender" 
                        value={gender}
                        onChange={(e) => setGender(e.target.value)}
                        className={`text-right text-[15px] w-auto py-2 bg-coal border rounded-[10px] ${showError ? "border-superRed" : "border-white"}`}>
                            <option value="آقا">آقا</option>
                            <option value="خانم">خانم</option>
                        </select>
                    </div>
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="height" className="mb-3">قد(سانتی‌متر)</label>
                        <input 
                        type="number"
                        value={height}
                        step="0.01"
                        min="0.00"
                        onChange={(e) => setHeight(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !height ? "border-superRed" : "border-white"}`} 
                        />
                    </div>
                    <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                        <label htmlFor="weight" className="mb-3">وزن(کیلوگرم)</label>
                        <input 
                        type="number"
                        step="0.01"
                        min="30"
                        value={weight}
                        onChange={(e) => setWeight(e.target.value)}
                        className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-coal border rounded-[10px] ${showError && !weight ? "border-superRed" : "border-white"}`} 
                        />
                    </div>
                </div>
            </div>
            <button type="submit" className="mt-[50px] text-irishGreen bg-mintCream hover:text-mintCream hover:bg-irishGreen font-medium px-[70px] py-[5px] rounded-[10px] transition-all duration-300">ثبت نام</button>
        </form>
        </div>
        
    );
}