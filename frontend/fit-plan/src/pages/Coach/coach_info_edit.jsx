import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Coach_info_edit() {
  const navigate = useNavigate();

  const [userInfo, setUserInfo] = useState({
    nameSurname: "دانا لاجوردی",
    username: "Dana_Laj",
    password: "********",
    phoneNumber: "989123456789+",
    email: "Dana.Laj@gmail.com",
    birthDate: "1365/7/18",
    gender: "آقا",
    height: "175",
    weight: "65",
    status: "در دسترس",
    about:
      "دانا با بیش از ۱۵ سال تجربه در زمینه بدنسازی و تمرینات قدرتی، یکی از مربیان پیشرو در این حوزه به شمار می‌رود. او کار خود را به عنوان مربی شخصی در باشگاه‌های کوچک شروع کرد و به تدریج توانست با تدوین برنامه‌های تمرینی تخصصی برای ورزشکاران حرفه‌ای، شهرت زیادی کسب کند. دانا به بهینه‌سازی قدرت بدنی علاقه ویژه‌ای دارد و موفق شده چندین قهرمان مسابقات بدنسازی را آماده کند.",
    image: "/Images/Coach-Dana-Lajevardi.png",
  });

  const [showStatus, setShowStatus] = useState(true);

  useEffect(() => {
    if (userInfo.status === "در دسترس") {
      setShowStatus(true);
      console.log(tempInfo.status);
    } else {
      setShowStatus(false);
    }
  }, []);

  const [tempInfo, setTempInfo] = useState({
    nameSurname: userInfo.nameSurname,
    username: userInfo.username,
    password: userInfo.password,
    phoneNumber: userInfo.phoneNumber,
    email: userInfo.email,
    birthDate: userInfo.birthDate,
    gender: userInfo.gender,
    height: userInfo.height,
    weight: userInfo.weight,
    status: userInfo.status,
    about: userInfo.about,
    image: userInfo.image,
  });
  const [profilePhoto, setProfilePhoto] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setTempInfo((tempInfo) => ({ ...tempInfo, [name]: value }));
  };

  const handleSave = () => {
    setUserInfo(tempInfo);
    alert("Changes saved!");
    navigate("/coach_panel");
  };

  const handleCancel = () => {
    setTempInfo(userInfo);
    navigate("/coach_panel");
  };

  // Handling status and toggling between available and unavailable
  const handleStatus = () => {
    if (tempInfo.status === "در دسترس") {
      setTempInfo((tempInfo) => ({ ...tempInfo, status: "خارج از دسترس" }));
      console.log(tempInfo.status); //Ensuring about the satatus
    } else {
      setTempInfo((tempInfo) => ({ ...tempInfo, status: "در دسترس" }));
      console.log(tempInfo.status);
    }
  };

  const handleProfilePhotoChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const imageUrl = URL.createObjectURL(file);
      console.log("Generated URL:", imageUrl); // Ensure URL is generated
      setTempInfo((tempInfo) => {
        const updatedInfo = { ...tempInfo, image: imageUrl };
        console.log("Updated tempInfo:", updatedInfo); // Verify state update
        return updatedInfo;
      });
    }
  };

  return (
    <div className="bg-black w-full h-full flex justify-start gap-[35px] mx-auto font-iranyekan">
      <div className="flex flex-col gap-5 justify-start mx-auto w-[80%] py-[40px]">
        <div className="flex justify-between">
          <h1 className="text-[45px] font-bold text-mintCream">
            ویرایش اطلاعات کاربر
          </h1>
        </div>
        <form className="border mb-[22px] rounded-[10px] h-[618px] overflow-hidden flex max-md:flex-col max-md:justify-center justify-start gap-5 text-mintCream">
          <div className="h-full w-[25%] overflow-hidden max-md:w-full max-md:justify-center max-md:text-center max-md:mx-auto">
            <img
              src={tempInfo.image}
              alt="user_image"
              className="object-cover object-center h-full max-md:h-auto"
            />
          </div>
          <div className="w-[70%] overflow-y-auto scrollbar-none py-5 px-2 flex flex-col max-md:text-center max-md:mx-auto max-md:w-[90%] gap-11">
            <input
              type="text"
              id="nameSurname"
              name="nameSurname"
              value={tempInfo.nameSurname}
              onChange={handleInputChange}
              className="text-[45px] font-medium max-w-[600px] bg-coal border rounded-[8px] px-2"
            />
            <div className="w-full flex max-lg:flex-col justify-between gap-11">
              <div className="w-full flex justify-between max-sm:flex-col max-sm:w-auto max-sm:text-center max-sm:mx-auto">
                <p className="font-medium text-[20px]">نام کاربری:</p>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={tempInfo.username}
                  onChange={handleInputChange}
                  className="text-[20px] text-left font-light max-w-[180px] bg-coal border rounded-[8px] px-2"
                />
              </div>
              <div className="w-full flex justify-between max-sm:flex-col max-sm:w-auto max-sm:text-center max-sm:mx-auto">
                <p className="font-medium text-[20px]">گذرواژه:</p>
                <input
                  type="text"
                  id="password"
                  name="password"
                  value={tempInfo.password}
                  onChange={handleInputChange}
                  className="text-[20px] text-left font-light max-w-[180px] bg-coal border rounded-[8px] px-2"
                />
              </div>
            </div>
            <div className="w-full flex max-lg:flex-col justify-between gap-11">
              <div className="w-full flex justify-between max-sm:flex-col max-sm:w-auto max-sm:text-center max-sm:mx-auto">
                <p className="font-medium text-[20px]">شماره تماس:</p>
                <input
                  type="text"
                  id="phoneNumber"
                  name="phoneNumber"
                  value={tempInfo.phoneNumber}
                  onChange={handleInputChange}
                  className="text-[20px] text-left font-light max-w-[180px] bg-coal border rounded-[8px] px-2"
                />
              </div>
              <div className="w-full flex justify-between max-sm:flex-col max-sm:w-auto max-sm:text-center max-sm:mx-auto">
                <p className="font-medium text-[20px]">آدرس ایمیل:</p>
                <input
                  type="text"
                  id="email"
                  name="email"
                  value={tempInfo.email}
                  onChange={handleInputChange}
                  className="text-[15px] text-left font-light max-w-[180px] bg-coal border rounded-[8px] px-2"
                />
              </div>
            </div>
            <div className="w-full flex max-lg:flex-col justify-between gap-11">
              <div className="w-full flex justify-between max-sm:flex-col max-sm:w-auto max-sm:text-center max-sm:mx-auto">
                <p className="font-medium text-[20px]">تاریخ تولد:</p>
                <input
                  type="text"
                  id="birthDate"
                  name="birthDate"
                  value={tempInfo.birthDate}
                  onChange={handleInputChange}
                  className="text-[20px] text-left font-light max-w-[180px] bg-coal border rounded-[8px] px-2"
                />
              </div>
              <div className="w-full flex justify-between">
                <p className="font-medium text-[20px]">جنسیت:</p>
                <select
                  name="gender"
                  id="gender"
                  value={tempInfo.gender}
                  onChange={handleInputChange}
                  className="text-[18px] font-light max-w-[180px] bg-coal border rounded-[8px] px-3"
                >
                  <option value="آقا">آقا</option>
                  <option value="خانم">خانم</option>
                </select>
              </div>
            </div>
            <div className="w-full flex max-lg:flex-col justify-between gap-11">
              <div className="w-full flex justify-between max-sm:flex-col max-sm:w-auto max-sm:text-center max-sm:mx-auto">
                <p className="font-medium text-[20px]">قد(سانتی متر):</p>
                <input
                  type="number"
                  id="height"
                  name="height"
                  step="0.01"
                  value={tempInfo.height}
                  onChange={handleInputChange}
                  className="text-[20px] text-left font-light max-w-[180px] bg-coal border rounded-[8px] px-2"
                />
              </div>
              <div className="w-full flex justify-between max-sm:flex-col max-sm:w-auto max-sm:text-center max-sm:mx-auto">
                <p className="font-medium text-[20px]">وزن(کیلوگرم):</p>
                <input
                  type="number"
                  id="weight"
                  name="weight"
                  step="0.01"
                  value={tempInfo.weight}
                  onChange={handleInputChange}
                  className="text-[20px] text-left font-light max-w-[180px] bg-coal border rounded-[8px] px-2"
                />
              </div>
            </div>
            <div className="w-full flex max-lg:flex-col justify-between gap-11">
              
              <div className="w-full flex justify-end max-lg:justify-center max-lg:mx-auto">
                <button
                  type="button"
                  onClick={handleStatus}
                  style={{
                    backgroundColor:
                      tempInfo.status === "در دسترس" ? "#018625" : "#C5120B",
                    color: "white",
                    padding: "10px 20px",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                    transition: "background-color 0.3s",
                  }}
                  onMouseEnter={(e) =>
                    (e.target.style.backgroundColor =
                      tempInfo.status === "در دسترس" ? "#006400" : "#8B0000")
                  }
                  onMouseLeave={(e) =>
                    (e.target.style.backgroundColor =
                      tempInfo.status === "در دسترس" ? "#018625" : "#C5120B")
                  }
                >
                  {tempInfo.status === "در دسترس"
                    ? "آماده فعالیت هستم"
                    : "فعلا آماده فعالیت نیستم"}
                </button>
              </div>
            </div>
            <div className="w-full flex max-lg:flex-col justify-between gap-11">
              <div className="w-full flex justify-start gap-5">
                <p className="font-medium text-[20px]">درباره مربی</p>
                <textarea
                  type="text"
                  id="about"
                  name="about"
                  value={tempInfo.about}
                  onChange={handleInputChange}
                  className="text-[20px] leading-9 font-light w-full h-[400px] bg-coal border rounded-[8px] px-2"
                />
              </div>
            </div>
            <div className="flex max-lg:flex-col max-lg:gap-8 justify-between">
              <input
                type="file"
                id="profile-photo"
                accept="image/*"
                onChange={handleProfilePhotoChange}
                className="hidden text-[20px] font-light bg-coal border rounded-[8px]"
              />
              <label
                htmlFor="profile-photo"
                className="text-[20px] max-lg:text-center font-medium bg-coal border rounded-[8px] py-1 px-3 cursor-pointer hover:bg-mintCream hover:text-black transition-all duration-300"
              >
                ویرایش تصویر نمایه
              </label>
              <div className="flex justify-end max-lg:justify-center gap-3">
                <button
                  type="button"
                  onClick={handleSave}
                  className="bg-black text-irishGreen font-medium text-[17px] border-[2px] border-irishGreen rounded-[10px] py-2 px-5 hover:bg-irishGreen hover:text-black transition-all duration-300"
                >
                  ثبت تغییرات
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="bg-black text-superRed font-medium text-[17px] border-[2px] border-superRed rounded-[10px] py-2 px-5 hover:bg-superRed hover:text-black transition-all duration-300"
                >
                  لغو تغییرات
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
