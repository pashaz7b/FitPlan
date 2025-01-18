import { useState } from "react";
import fit_logo from "/Images/Fit-Logo-Resized.png";
import { useNavigate } from "react-router-dom";

export default function Admin_panel() {
  const [adminInfo, setAdminInfo] = useState({
    nameSurname: "نیوشا قنبری",
    username: "im_new",
    password: "********",
    phoneNumber: "989123456789+",
    email: "new.mewj@gmail.com",
    birthDate: "1365/7/18",
    image: "/Images/michael-dam-mEZ3PoFGs_k-unsplash.jpg",
  });

  const [tempInfo, setTempInfo] = useState(adminInfo);
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const navigate = useNavigate();
  const handleNavigate = (e) => {
    navigate("./user_login");
  };

  return (
    <div className="max-lg:pr-0 max-lg:justify-center max-lg:text-center max-lg:mx-auto bg-black w-full h-full flex justify-start pr-[400px] gap-[35px] mx-auto font-iranyekan">
      <div className="max-lg:hidden fixed top-[48px] right-[51px] w-[320px] h-[700px] overflow-hidden bg-coal rounded-[15px] shadow-lg font-iranyekan">
        {/* Static Header Section */}
        <div className="flex flex-col items-center bg-coal">
          {adminInfo.image && adminInfo.image.trim() ? (
            <img
              src={adminInfo.image}
              alt={adminInfo.nameSurname}
              className="w-full max-h-[220px] object-cover object-top"
            />
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="220px"
              viewBox="0 -960 960 960"
              width="full"
              fill="#e8eaed"
            >
              <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
            </svg>
          )}
          <p className="mt-3 text-lg font-semibold text-superRed">
            {adminInfo.nameSurname}
          </p>
          <p className="mt-2 text-lg text-superRed font-light">
            {adminInfo.username}@
          </p>
        </div>

        {/* Scrollable List Section */}
        <div className="overflow-y-auto font-medium max-h-[330px] scrollbar-thin scrollbar-thumb-superRed scrollbar-track-coal">
          <div className="flex flex-col gap-1 p-2">
            <a
              href="/admin_panel"
              className="w-[90%] border-crimsonRed bg-crimsonRed text-black text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>اطلاعات کاربر</p>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="35px"
                viewBox="0 -960 960 960"
                width="35px"
                fill="#000000"
              >
                <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
              </svg>
            </a>
            <a
              href="/admin_panel/admin_trainees"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>شاگردان</p>
              <div className="h-[30px]">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="24px"
                  viewBox="0 -960 960 960"
                  width="24px"
                  fill="#e8eaed"
                >
                  <path d="m216-160-56-56 384-384H440v80h-80v-160h233q16 0 31 6t26 17l120 119q27 27 66 42t84 16v80q-62 0-112.5-19T718-476l-40-42-88 88 90 90-262 151-40-69 172-99-68-68-266 265Zm-96-280v-80h200v80H120ZM40-560v-80h200v80H40Zm739-80q-33 0-57-23.5T698-720q0-33 24-56.5t57-23.5q33 0 57 23.5t24 56.5q0 33-24 56.5T779-640Zm-659-40v-80h200v80H120Z" />
                </svg>
              </div>
            </a>
            <a
              href="/admin_panel/admin_coaches"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>مربی‌ها</p>
              <div className="h-[30px]">
                <img
                  src="/Images/bodybuilding-White.png"
                  alt="coaches_icon"
                  className="h-full"
                />
              </div>
            </a>

            <a
              href="/admin_panel/admin_transactions"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>تراکنش‌ها</p>
              <svg
                width="27"
                height="26"
                viewBox="0 0 27 26"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4.67647 26C3.64902 26 2.77941 25.6629 2.06765 24.9887C1.35588 24.3145 1 23.4908 1 22.5176V20.2944C1 19.9353 1.12684 19.6357 1.38051 19.3956C1.63395 19.1553 1.95025 19.0352 2.32941 19.0352H5.41177V0.489975C5.41177 0.345339 5.47353 0.248527 5.59706 0.199541C5.72059 0.150323 5.83885 0.170404 5.95184 0.259786L7.03235 1.1088C7.16054 1.21234 7.29914 1.26411 7.44816 1.26411C7.59694 1.26411 7.73542 1.21234 7.8636 1.1088L9.09669 0.155314C9.22488 0.0517704 9.36348 0 9.5125 0C9.66152 0 9.80012 0.0517704 9.92831 0.155314L11.1614 1.1088C11.2896 1.21234 11.4281 1.26411 11.5768 1.26411C11.7259 1.26411 11.8645 1.21234 11.9926 1.1088L13.2257 0.155314C13.3539 0.0517704 13.4925 0 13.6415 0C13.7903 0 13.9288 0.0517704 14.057 0.155314L15.2901 1.1088C15.4183 1.21234 15.5569 1.26411 15.7059 1.26411C15.8549 1.26411 15.9935 1.21234 16.1217 1.1088L17.3548 0.155314C17.483 0.0517704 17.6214 0 17.7702 0C17.9192 0 18.0578 0.0517704 18.186 0.155314L19.4191 1.1088C19.5473 1.21234 19.6859 1.26411 19.8349 1.26411C19.9837 1.26411 20.1222 1.21234 20.2504 1.1088L21.4835 0.155314C21.6116 0.0517704 21.7502 0 21.8993 0C22.0483 0 22.1869 0.0517704 22.3151 0.155314L23.5482 1.1088C23.6763 1.21234 23.8148 1.26411 23.9636 1.26411C24.1126 1.26411 24.2512 1.21234 24.3794 1.1088L25.4599 0.259786C25.5729 0.170404 25.6912 0.150323 25.8147 0.199541C25.9382 0.248527 26 0.345339 26 0.489975V22.5176C26 23.4908 25.6441 24.3145 24.9324 24.9887C24.2206 25.6629 23.351 26 22.3235 26H4.67647ZM22.3235 23.9106C22.7402 23.9106 23.0895 23.7771 23.3713 23.5101C23.6532 23.2431 23.7941 22.9123 23.7941 22.5176V3.01611H7.61765V19.0352H19.5239C19.9028 19.0352 20.219 19.1553 20.4724 19.3956C20.7261 19.6357 20.8529 19.9353 20.8529 20.2944V22.5176C20.8529 22.9123 20.9939 23.2431 21.2757 23.5101C21.5576 23.7771 21.9069 23.9106 22.3235 23.9106ZM10.4739 6.15028H16.611C16.9238 6.15028 17.1858 6.25034 17.3971 6.45046C17.6081 6.65035 17.7136 6.89853 17.7136 7.195C17.7136 7.49147 17.6081 7.73965 17.3971 7.93954C17.1858 8.13966 16.9238 8.23972 16.611 8.23972H10.4739C10.1609 8.23972 9.8989 8.13966 9.68787 7.93954C9.47659 7.73965 9.37096 7.49147 9.37096 7.195C9.37096 6.89853 9.47659 6.65035 9.68787 6.45046C9.8989 6.25034 10.1609 6.15028 10.4739 6.15028ZM10.4739 10.3292H16.611C16.9238 10.3292 17.1858 10.4292 17.3971 10.6294C17.6081 10.8292 17.7136 11.0774 17.7136 11.3739C17.7136 11.6704 17.6081 11.9185 17.3971 12.1184C17.1858 12.3186 16.9238 12.4186 16.611 12.4186H10.4739C10.1609 12.4186 9.8989 12.3186 9.68787 12.1184C9.47659 11.9185 9.37096 11.6704 9.37096 11.3739C9.37096 11.0774 9.47659 10.8292 9.68787 10.6294C9.8989 10.4292 10.1609 10.3292 10.4739 10.3292ZM20.768 8.42708C20.408 8.42708 20.1011 8.30705 19.8474 8.067C19.594 7.82671 19.4673 7.53605 19.4673 7.195C19.4673 6.85396 19.594 6.56329 19.8474 6.32301C20.1011 6.08295 20.408 5.96293 20.768 5.96293C21.1281 5.96293 21.4349 6.08295 21.6886 6.32301C21.9423 6.56329 22.0691 6.85396 22.0691 7.195C22.0691 7.53605 21.9423 7.82671 21.6886 8.067C21.4349 8.30705 21.1281 8.42708 20.768 8.42708ZM20.768 12.606C20.408 12.606 20.1011 12.4859 19.8474 12.2459C19.594 12.0056 19.4673 11.7149 19.4673 11.3739C19.4673 11.0328 19.594 10.7422 19.8474 10.5019C20.1011 10.2618 20.408 10.1418 20.768 10.1418C21.1281 10.1418 21.4349 10.2618 21.6886 10.5019C21.9423 10.7422 22.0691 11.0328 22.0691 11.3739C22.0691 11.7149 21.9423 12.0056 21.6886 12.2459C21.4349 12.4859 21.1281 12.606 20.768 12.606ZM4.67647 23.9106H18.6471V21.1246H3.20588V22.5176C3.20588 22.9123 3.34681 23.2431 3.62868 23.5101C3.91054 23.7771 4.2598 23.9106 4.67647 23.9106Z"
                  fill="#FFF7ED"
                />
              </svg>
            </a>
            <a
              href="/"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>خانه</p>
              <svg
                width="25"
                height="24"
                viewBox="0 0 25 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4.1 21.9017H8.78475V14.8537C8.78475 14.4956 8.90597 14.1953 9.1484 13.9529C9.39107 13.7106 9.6916 13.5895 10.05 13.5895H14.95C15.3084 13.5895 15.6089 13.7106 15.8516 13.9529C16.094 14.1953 16.2153 14.4956 16.2153 14.8537V21.9017H20.9V9.5273C20.9 9.45573 20.8843 9.3908 20.8528 9.33251C20.8215 9.27423 20.7789 9.22259 20.725 9.17759L12.7558 3.19232C12.684 3.12961 12.5987 3.09825 12.5 3.09825C12.4013 3.09825 12.316 3.12961 12.2442 3.19232L4.275 9.17759C4.2211 9.22259 4.17852 9.27423 4.14725 9.33251C4.11575 9.3908 4.1 9.45573 4.1 9.5273V21.9017ZM2 21.9017V9.5273C2 9.127 2.0896 8.7478 2.2688 8.3897C2.44823 8.03136 2.69603 7.73632 3.0122 7.50458L10.9817 1.50568C11.4239 1.16856 11.9293 1 12.4979 1C13.0665 1 13.5733 1.16856 14.0183 1.50568L21.9878 7.50458C22.304 7.73632 22.5518 8.03136 22.7312 8.3897C22.9104 8.7478 23 9.127 23 9.5273V21.9017C23 22.4739 22.7931 22.9666 22.3794 23.38C21.9658 23.7933 21.4726 24 20.9 24H15.3808C15.0222 24 14.7217 23.8788 14.4792 23.6363C14.2366 23.3941 14.1153 23.0938 14.1153 22.7355V15.6878H10.8848V22.7355C10.8848 23.0938 10.7634 23.3941 10.5208 23.6363C10.2783 23.8788 9.97778 24 9.61915 24H4.1C3.5274 24 3.03425 23.7933 2.62055 23.38C2.20685 22.9666 2 22.4739 2 21.9017Z"
                  fill="#E8EAED"
                />
              </svg>
            </a>
          </div>
        </div>
        <a
          href="/user_login"
          className="text-superRed font-medium text-[20px] flex justify-center mx-auto mt-5 hover:text-mintCream transition-all duration-300"
        >
          خروج
        </a>
      </div>

      <div className="flex flex-col gap-5 justify-start w-[95%] py-[40px]">
        <div className="flex justify-between">
          <h1 className="text-[45px] font-bold text-mintCream">
            اطلاعات کاربر
          </h1>
          {/* <a href="/user_panel/info_edit" className="text-superRed text-[25px] font-semibold border-[2px] border-superRed rounded-[15px] max-h-[59px] pt-2 px-8 hover:bg-superRed hover:text-black transition-all duration-300">ویرایش</a> */}
          <div className=" text-white font-iranyekan">
            {/* Navbar */}
            <nav className="flex lg:hidden items-center justify-between p-4 bg-black">
              {/* Hamburger Icon */}
              <div
                className="cursor-pointer text-2xl"
                onClick={() => setIsOpen(!isOpen)}
              >
                {isOpen ? "✖" : "☰"}
              </div>
            </nav>

            {/* Sidebar */}
            <div
              className={`fixed z-10 top-0 left-0 h-full w-[70%] bg-[#1c1c1c] transform ${
                isOpen ? "translate-x-0" : "-translate-x-full"
              } transition-transform duration-300`}
            >
              {/* Close Button */}
              <div className="flex justify-between p-4">
                <div className="h-[50px]">
                  <img src={fit_logo} alt="fit_logo" className="h-full" />
                </div>
                <button
                  className="text-white text-xl"
                  onClick={() => setIsOpen(false)}
                >
                  ✖
                </button>
              </div>

              <div className="flex flex-col items-center bg-coal">
                {adminInfo.image && adminInfo.image.trim() ? (
                  <img
                    src={adminInfo.image}
                    alt={adminInfo.nameSurname}
                    className="w-full max-h-[250px] object-cover"
                  />
                ) : (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="250px"
                    viewBox="0 -960 960 960"
                    width="full"
                    fill="#e8eaed"
                  >
                    <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
                  </svg>
                )}
                <p className="mt-3 text-lg font-semibold text-superRed">
                  {adminInfo.nameSurname}
                </p>
                <p className="mt-2 text-lg text-superRed font-light">
                  {adminInfo.username}@
                </p>
              </div>
              <div className="overflow-y-auto font-medium max-h-[330px] scrollbar-thin scrollbar-thumb-superRed scrollbar-track-coal">
                <div className="flex flex-col gap-1 p-2">
                  <a
                    href="/admin_panel"
                    className="w-[90%] border-crimsonRed bg-crimsonRed text-black text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>اطلاعات کاربر</p>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      height="35px"
                      viewBox="0 -960 960 960"
                      width="35px"
                      fill="#000000"
                    >
                      <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
                    </svg>
                  </a>
                  <a
                    href="/admin_panel/admin_trainees"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>شاگردان</p>
                    <div className="h-[30px]">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        height="24px"
                        viewBox="0 -960 960 960"
                        width="24px"
                        fill="#e8eaed"
                      >
                        <path d="m216-160-56-56 384-384H440v80h-80v-160h233q16 0 31 6t26 17l120 119q27 27 66 42t84 16v80q-62 0-112.5-19T718-476l-40-42-88 88 90 90-262 151-40-69 172-99-68-68-266 265Zm-96-280v-80h200v80H120ZM40-560v-80h200v80H40Zm739-80q-33 0-57-23.5T698-720q0-33 24-56.5t57-23.5q33 0 57 23.5t24 56.5q0 33-24 56.5T779-640Zm-659-40v-80h200v80H120Z" />
                      </svg>
                    </div>
                  </a>
                  <a
                    href="/admin_panel/admin_coaches"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>مربی‌ها</p>
                    <div className="h-[30px]">
                      <img
                        src="/Images/bodybuilding-White.png"
                        alt="coaches_icon"
                        className="h-full"
                      />
                    </div>
                  </a>

                  <a
                    href="/admin_panel/admin_transactions"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>تراکنش‌ها</p>
                    <svg
                      width="27"
                      height="26"
                      viewBox="0 0 27 26"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M4.67647 26C3.64902 26 2.77941 25.6629 2.06765 24.9887C1.35588 24.3145 1 23.4908 1 22.5176V20.2944C1 19.9353 1.12684 19.6357 1.38051 19.3956C1.63395 19.1553 1.95025 19.0352 2.32941 19.0352H5.41177V0.489975C5.41177 0.345339 5.47353 0.248527 5.59706 0.199541C5.72059 0.150323 5.83885 0.170404 5.95184 0.259786L7.03235 1.1088C7.16054 1.21234 7.29914 1.26411 7.44816 1.26411C7.59694 1.26411 7.73542 1.21234 7.8636 1.1088L9.09669 0.155314C9.22488 0.0517704 9.36348 0 9.5125 0C9.66152 0 9.80012 0.0517704 9.92831 0.155314L11.1614 1.1088C11.2896 1.21234 11.4281 1.26411 11.5768 1.26411C11.7259 1.26411 11.8645 1.21234 11.9926 1.1088L13.2257 0.155314C13.3539 0.0517704 13.4925 0 13.6415 0C13.7903 0 13.9288 0.0517704 14.057 0.155314L15.2901 1.1088C15.4183 1.21234 15.5569 1.26411 15.7059 1.26411C15.8549 1.26411 15.9935 1.21234 16.1217 1.1088L17.3548 0.155314C17.483 0.0517704 17.6214 0 17.7702 0C17.9192 0 18.0578 0.0517704 18.186 0.155314L19.4191 1.1088C19.5473 1.21234 19.6859 1.26411 19.8349 1.26411C19.9837 1.26411 20.1222 1.21234 20.2504 1.1088L21.4835 0.155314C21.6116 0.0517704 21.7502 0 21.8993 0C22.0483 0 22.1869 0.0517704 22.3151 0.155314L23.5482 1.1088C23.6763 1.21234 23.8148 1.26411 23.9636 1.26411C24.1126 1.26411 24.2512 1.21234 24.3794 1.1088L25.4599 0.259786C25.5729 0.170404 25.6912 0.150323 25.8147 0.199541C25.9382 0.248527 26 0.345339 26 0.489975V22.5176C26 23.4908 25.6441 24.3145 24.9324 24.9887C24.2206 25.6629 23.351 26 22.3235 26H4.67647ZM22.3235 23.9106C22.7402 23.9106 23.0895 23.7771 23.3713 23.5101C23.6532 23.2431 23.7941 22.9123 23.7941 22.5176V3.01611H7.61765V19.0352H19.5239C19.9028 19.0352 20.219 19.1553 20.4724 19.3956C20.7261 19.6357 20.8529 19.9353 20.8529 20.2944V22.5176C20.8529 22.9123 20.9939 23.2431 21.2757 23.5101C21.5576 23.7771 21.9069 23.9106 22.3235 23.9106ZM10.4739 6.15028H16.611C16.9238 6.15028 17.1858 6.25034 17.3971 6.45046C17.6081 6.65035 17.7136 6.89853 17.7136 7.195C17.7136 7.49147 17.6081 7.73965 17.3971 7.93954C17.1858 8.13966 16.9238 8.23972 16.611 8.23972H10.4739C10.1609 8.23972 9.8989 8.13966 9.68787 7.93954C9.47659 7.73965 9.37096 7.49147 9.37096 7.195C9.37096 6.89853 9.47659 6.65035 9.68787 6.45046C9.8989 6.25034 10.1609 6.15028 10.4739 6.15028ZM10.4739 10.3292H16.611C16.9238 10.3292 17.1858 10.4292 17.3971 10.6294C17.6081 10.8292 17.7136 11.0774 17.7136 11.3739C17.7136 11.6704 17.6081 11.9185 17.3971 12.1184C17.1858 12.3186 16.9238 12.4186 16.611 12.4186H10.4739C10.1609 12.4186 9.8989 12.3186 9.68787 12.1184C9.47659 11.9185 9.37096 11.6704 9.37096 11.3739C9.37096 11.0774 9.47659 10.8292 9.68787 10.6294C9.8989 10.4292 10.1609 10.3292 10.4739 10.3292ZM20.768 8.42708C20.408 8.42708 20.1011 8.30705 19.8474 8.067C19.594 7.82671 19.4673 7.53605 19.4673 7.195C19.4673 6.85396 19.594 6.56329 19.8474 6.32301C20.1011 6.08295 20.408 5.96293 20.768 5.96293C21.1281 5.96293 21.4349 6.08295 21.6886 6.32301C21.9423 6.56329 22.0691 6.85396 22.0691 7.195C22.0691 7.53605 21.9423 7.82671 21.6886 8.067C21.4349 8.30705 21.1281 8.42708 20.768 8.42708ZM20.768 12.606C20.408 12.606 20.1011 12.4859 19.8474 12.2459C19.594 12.0056 19.4673 11.7149 19.4673 11.3739C19.4673 11.0328 19.594 10.7422 19.8474 10.5019C20.1011 10.2618 20.408 10.1418 20.768 10.1418C21.1281 10.1418 21.4349 10.2618 21.6886 10.5019C21.9423 10.7422 22.0691 11.0328 22.0691 11.3739C22.0691 11.7149 21.9423 12.0056 21.6886 12.2459C21.4349 12.4859 21.1281 12.606 20.768 12.606ZM4.67647 23.9106H18.6471V21.1246H3.20588V22.5176C3.20588 22.9123 3.34681 23.2431 3.62868 23.5101C3.91054 23.7771 4.2598 23.9106 4.67647 23.9106Z"
                        fill="#FFF7ED"
                      />
                    </svg>
                  </a>
                  <a
                    href="/"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>خانه</p>
                    <svg
                      width="25"
                      height="24"
                      viewBox="0 0 25 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M4.1 21.9017H8.78475V14.8537C8.78475 14.4956 8.90597 14.1953 9.1484 13.9529C9.39107 13.7106 9.6916 13.5895 10.05 13.5895H14.95C15.3084 13.5895 15.6089 13.7106 15.8516 13.9529C16.094 14.1953 16.2153 14.4956 16.2153 14.8537V21.9017H20.9V9.5273C20.9 9.45573 20.8843 9.3908 20.8528 9.33251C20.8215 9.27423 20.7789 9.22259 20.725 9.17759L12.7558 3.19232C12.684 3.12961 12.5987 3.09825 12.5 3.09825C12.4013 3.09825 12.316 3.12961 12.2442 3.19232L4.275 9.17759C4.2211 9.22259 4.17852 9.27423 4.14725 9.33251C4.11575 9.3908 4.1 9.45573 4.1 9.5273V21.9017ZM2 21.9017V9.5273C2 9.127 2.0896 8.7478 2.2688 8.3897C2.44823 8.03136 2.69603 7.73632 3.0122 7.50458L10.9817 1.50568C11.4239 1.16856 11.9293 1 12.4979 1C13.0665 1 13.5733 1.16856 14.0183 1.50568L21.9878 7.50458C22.304 7.73632 22.5518 8.03136 22.7312 8.3897C22.9104 8.7478 23 9.127 23 9.5273V21.9017C23 22.4739 22.7931 22.9666 22.3794 23.38C21.9658 23.7933 21.4726 24 20.9 24H15.3808C15.0222 24 14.7217 23.8788 14.4792 23.6363C14.2366 23.3941 14.1153 23.0938 14.1153 22.7355V15.6878H10.8848V22.7355C10.8848 23.0938 10.7634 23.3941 10.5208 23.6363C10.2783 23.8788 9.97778 24 9.61915 24H4.1C3.5274 24 3.03425 23.7933 2.62055 23.38C2.20685 22.9666 2 22.4739 2 21.9017Z"
                        fill="#E8EAED"
                      />
                    </svg>
                  </a>
                </div>
              </div>
              <a
                href="/user_login"
                className="text-superRed font-medium text-[20px] flex justify-center mx-auto mt-5 hover:text-mintCream transition-all duration-300"
              >
                خروج
              </a>
            </div>
          </div>
        </div>
        <div className="max-md:flex-col max-md:justify-start max-md:gap-3 max-md:text-center max-md:overflow-y-auto border mb-[22px] rounded-[10px] h-[618px] overflow-hidden flex justify-start gap-5 text-mintCream">
          <div className="max-md:text-center max-md:justify-center max-md:h-full max-md:w-full max-md:mx-auto h-full w-[25%] overflow-hidden">
            <img
              src={adminInfo.image}
              alt="user_image"
              className="max-md:text-center max-md:justify-center max-md:w-full max-md:object-cover object-cover object-center h-full scale-[100%]"
            />
          </div>
          <div className="max-md:w-[95%] max-md:gap-4 overflow-y-auto scrollbar-none max-md:mx-auto w-[70%] py-5 px-2 flex flex-col gap-11">
            <h1 className="text-[45px] font-medium">{adminInfo.nameSurname}</h1>
            <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
              <div className="w-full flex justify-between">
                <p className="font-medium text-[20px]">نام کاربری:</p>
                <p className="text-[20px] font-light">{adminInfo.username}</p>
              </div>
              <div className="w-full flex justify-between">
                <p className="font-medium text-[20px]">گذرواژه:</p>
                <p className="text-[20px] font-light">********</p>
              </div>
            </div>
            <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
              <div className="w-full flex justify-between">
                <p className="font-medium text-[20px]">شماره تماس:</p>
                <p className="text-[20px] font-light">
                  {adminInfo.phoneNumber}
                </p>
              </div>
              <div className="w-full flex justify-between">
                <p className="font-medium text-[20px]">آدرس ایمیل:</p>
                <p className="text-[15px] font-light">{adminInfo.email}</p>
              </div>
            </div>
            <div className="max-md:flex-col max-md:gap-4 max-lg:w-[35%] w-[30%] flex mx-auto justify-between gap-11">
              <div className="w-full flex justify-between">
                <p className="font-medium text-[20px]">تاریخ تولد:</p>
                <p className="text-[20px] font-light">{adminInfo.birthDate}</p>
              </div>
            </div>
            <button className="text-center max-md:text-center max-md:flex max-md:justify-center max-md:mx-auto text-superRed text-[25px] font-semibold  max-h-[62px]">
              <a
                href="/admin_panel/info_edit"
                className="border-[2px] border-superRed rounded-[15px] py-2 px-8 hover:bg-superRed hover:text-black transition-all duration-300"
              >
                ویرایش
              </a>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
