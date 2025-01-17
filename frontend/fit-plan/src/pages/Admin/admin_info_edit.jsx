import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Admin_info_edit() {
  const navigate = useNavigate();

  const [adminInfo, setAdminInfo] = useState({
    nameSurname: "نیوشا قنبری",
    username: "im_new",
    password: "new1365sha",
    phoneNumber: "989123456789+",
    email: "new.mewj@gmail.com",
    birthDate: "1365/7/18",
    image: "/Images/michael-dam-mEZ3PoFGs_k-unsplash.jpg",
  });


  const [tempInfo, setTempInfo] = useState({
    nameSurname: adminInfo.nameSurname,
    username: adminInfo.username,
    password: adminInfo.password,
    phoneNumber: adminInfo.phoneNumber,
    email: adminInfo.email,
    birthDate: adminInfo.birthDate,
    image: adminInfo.image,
  });
  const [profilePhoto, setProfilePhoto] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setTempInfo((tempInfo) => ({ ...tempInfo, [name]: value }));
  };

  const handleSave = () => {
    setAdminInfo(tempInfo);
    alert("Changes saved!");
    navigate("/admin_panel");
  };

  const handleCancel = () => {
    setTempInfo(adminInfo);
    navigate("/admin_panel");
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
