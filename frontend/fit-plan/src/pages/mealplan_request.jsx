import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import fit_logo from "/Images/Fit-Logo-Resized.png";

export default function Mealplan_req() {
  const [userInfo, setUserInfo] = useState({
    nameSurname: "آونگ روزبه",
    username: "AAAvng",
    password: "********",
    phoneNumber: "989123456789+",
    email: "avng.rzbh@gmail.com",
    birthDate: "1365/7/18",
    gender: "آقا",
    height: "175",
    weight: "65",
    image: "/Images/payton-tuttle-RFFR1JjkJx8-unsplash.jpg",
  });

  const [weight, setWeight] = useState("");
  const [weightError, setWeightError] = useState(false);
  const [waistSize, setWaistSize] = useState("");
  const [waistSizeError, setWaistSizeError] = useState(false);
  const [showError, setShowError] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState("");
  const [images, setImages] = useState([]);
  const [preview, setPreview] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    handleWeight(e);
    handleWaistSize(e);

    if (!waistSize || !weight) {
      setShowError(true);
    } else {
      setShowError(false);
      console.log("Submit Successful!");
      console.log(waistSize);
      console.log(weight);
      navigate("/user_panel/user_mealPlan");
    }
  };

  const handleWeight = (e) => {
    const value = e.target.value || "";
    const sanitizedValue = value
      .replace(/[^\d.]/g, "")
      .replace(/(\..*?)\..*/g, "$1");

    if (value == "") {
      setWeightError(true);
    } else {
      setWeightError(false);
      setWeight(sanitizedValue);
      console.log(e.value.target);
    }
  };

  const handleWaistSize = (e) => {
    const value = e.target.value || "";
    const sanitizedValue = value
      .replace(/[^\d.]/g, "")
      .replace(/(\..*?)\..*/g, "$1");

    if (sanitizedValue == "") {
      console.log("No Size");
      setWaistSizeError(true);
    } else {
      setWaistSizeError(false);
      setWaistSize(sanitizedValue);
      console.log(e.value.target);
    }
  };

  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const handlePlanType = (event) => {
    setSelectedPlan(event.target.value);
  };

  const handleFileChange = (event) => {
    setPreview(true);

    const selectedFiles = Array.from(event.target.files);
    setImages((prevImages) => [...prevImages, ...selectedFiles]);
  };

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = "/Files/Measuring.pdf";
    link.download = "Measuring.pdf";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };
  return (
    <div className="max-lg:pr-0 max-lg:justify-center max-lg:text-center max-lg:mx-auto bg-black w-full h-full flex justify-start pr-[400px] gap-[35px] mx-auto font-iranyekan">
      <div className="max-lg:hidden fixed top-[48px] right-[51px] w-[320px] h-[700px] overflow-hidden bg-coal rounded-[15px] shadow-lg font-iranyekan">
        {/* Static Header Section */}
        <div className="flex flex-col items-center bg-coal">
          <img
            src="/Images/payton-tuttle-RFFR1JjkJx8-unsplash.jpg"
            alt="User Avatar"
            className="w-full max-h-[250px] object-contain"
          />
          <p className="mt-3 text-lg font-semibold text-superRed">
            {userInfo.nameSurname}
          </p>
          <p className="mt-2 text-lg text-superRed font-light">
            {userInfo.username}@
          </p>
        </div>

        {/* Scrollable List Section */}
        <div className="overflow-y-auto font-medium max-h-[330px] scrollbar-thin scrollbar-thumb-superRed scrollbar-track-coal">
          <div className="flex flex-col gap-1 p-2">
            <a
              href="/user_panel"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>اطلاعات کاربر</p>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="35px"
                viewBox="0 -960 960 960"
                width="35px"
                fill="#e8eaed"
              >
                <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
              </svg>
            </a>
            <a
              href="/user_panel/user_coach"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>مربی</p>
              <div className="h-[30px]">
                <img
                  src="/Images/bodybuilding-White.png"
                  alt="coaches_icon"
                  className="h-full"
                />
              </div>
            </a>
            <a
              href="/user_panel/user_tutorial"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>آموزش حرکات</p>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 -960 960 960"
                width="24px"
                fill="#e8eaed"
              >
                <path d="M160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h480q33 0 56.5 23.5T720-720v180l126-126q10-10 22-5t12 19v344q0 14-12 19t-22-5L720-420v180q0 33-23.5 56.5T640-160H160Zm0-80h480v-480H160v480Zm0 0v-480 480Z" />
              </svg>
            </a>
            <a
              href="/user_panel/user_mealPlan"
              className="w-[90%] border-[2px] border-crimsonRed bg-crimsonRed text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>برنامه غذایی</p>
              <svg
                width="28"
                height="28"
                viewBox="0 0 28 28"
                fill="#e8eaed"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M7.41475 10.154V2C7.41475 1.71667 7.51235 1.47922 7.70756 1.28767C7.90276 1.09589 8.14457 1 8.43296 1C8.72159 1 8.96328 1.09589 9.15803 1.28767C9.35301 1.47922 9.4505 1.71667 9.4505 2V10.154H11.3298V2C11.3298 1.71667 11.4273 1.47922 11.6223 1.28767C11.8175 1.09589 12.0594 1 12.3481 1C12.6364 1 12.8781 1.09589 13.0731 1.28767C13.2679 1.47922 13.3652 1.71667 13.3652 2V10.154C13.3652 11.3471 12.9882 12.374 12.234 13.2347C11.4797 14.0953 10.5518 14.6428 9.4505 14.877V26C9.4505 26.2833 9.3529 26.5208 9.15769 26.7123C8.96248 26.9041 8.72068 27 8.43228 27C8.14366 27 7.90197 26.9041 7.70722 26.7123C7.51224 26.5208 7.41475 26.2833 7.41475 26V14.877C6.31341 14.6428 5.38556 14.0953 4.6312 13.2347C3.87707 12.374 3.5 11.3471 3.5 10.154V2C3.5 1.71667 3.5976 1.47922 3.79281 1.28767C3.98779 1.09589 4.22959 1 4.51821 1C4.80661 1 5.0483 1.09589 5.24328 1.28767C5.43803 1.47922 5.53541 1.71667 5.53541 2V10.154H7.41475ZM20.4642 16.3333H17.9867C17.6359 16.3333 17.3434 16.2179 17.1093 15.987C16.8754 15.7559 16.7585 15.4697 16.7585 15.1283V7.33333C16.7585 5.658 17.2517 4.18367 18.2382 2.91033C19.2246 1.63678 20.2267 1 21.2446 1C21.6258 1 21.9303 1.13422 22.1583 1.40267C22.3861 1.67089 22.5 2.00767 22.5 2.413V26C22.5 26.2833 22.4024 26.5208 22.2072 26.7123C22.0122 26.9041 21.7704 27 21.4818 27C21.1934 27 20.9517 26.9041 20.7567 26.7123C20.5617 26.5208 20.4642 26.2833 20.4642 26V16.3333Z"
                  fill="#FFF7ED"
                />
              </svg>
            </a>
            <a
              href="/user_panel/user_exercisePlan"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>برنامه تمرینی</p>
              <svg
                width="27"
                height="26"
                viewBox="0 0 27 26"
                fill="#e8eaed"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g clip-path="url(#clip0_156_1578)">
                  <path
                    d="M24.5347 9.40209L23.0966 7.96395L23.9439 7.08221C24.0323 6.99384 24.0765 6.89445 24.0765 6.78405C24.0765 6.67364 24.0323 6.57437 23.9439 6.48623L20.0138 2.55607C19.9256 2.4677 19.8264 2.42351 19.716 2.42351C19.6055 2.42351 19.5062 2.4677 19.4178 2.55607L18.536 3.40339L17.0635 1.93082L17.9638 0.996054C18.43 0.529874 19.0047 0.302523 19.6881 0.314C20.3714 0.325476 20.9461 0.564304 21.4123 1.03048L25.4695 5.08769C25.9357 5.55387 26.1688 6.12288 26.1688 6.79472C26.1688 7.46656 25.9357 8.03557 25.4695 8.50175L24.5347 9.40209ZM9.00175 24.9695C8.53557 25.4357 7.96656 25.6688 7.29472 25.6688C6.62288 25.6688 6.05387 25.4357 5.58769 24.9695L1.58351 20.965C1.10837 20.4901 0.870809 19.9035 0.870809 19.2053C0.870809 18.507 1.10837 17.9204 1.58351 17.4452L2.43082 16.5979L3.90338 18.0705L3.03472 18.9178C2.94635 19.0062 2.90217 19.1055 2.90217 19.216C2.90217 19.3264 2.94635 19.4256 3.03472 19.5138L6.98623 23.4653C7.07437 23.5536 7.17364 23.5978 7.28405 23.5978C7.39445 23.5978 7.49384 23.5536 7.58221 23.4653L8.42952 22.5966L9.90209 24.0692L9.00175 24.9695ZM22.5378 14.5005L24.3017 12.7366C24.39 12.6482 24.4342 12.5467 24.4342 12.4319C24.4342 12.3171 24.39 12.2156 24.3017 12.1272L14.3728 2.19834C14.2844 2.10997 14.1829 2.06579 14.0681 2.06579C13.9533 2.06579 13.8518 2.10997 13.7634 2.19834L11.9995 3.96218C11.9114 4.05055 11.8673 4.14982 11.8673 4.26C11.8673 4.3704 11.9114 4.46979 11.9995 4.55816L21.9418 14.5005C22.0302 14.5886 22.1296 14.6327 22.24 14.6327C22.3502 14.6327 22.4494 14.5886 22.5378 14.5005ZM13.2022 23.8361L14.966 22.0509C15.0542 21.9628 15.0982 21.8635 15.0982 21.7531C15.0982 21.6427 15.0542 21.5434 14.966 21.4553L5.04473 11.534C4.95659 11.4458 4.85732 11.4018 4.74691 11.4018C4.63651 11.4018 4.53724 11.4458 4.4491 11.534L2.66391 13.2978C2.57554 13.3862 2.53136 13.4878 2.53136 13.6025C2.53136 13.7173 2.57554 13.8189 2.66391 13.9072L12.5928 23.8361C12.6811 23.9245 12.7827 23.9686 12.8975 23.9686C13.0122 23.9686 13.1138 23.9245 13.2022 23.8361ZM12.6114 16.1768L16.6638 12.1458L14.3542 9.83625L10.3232 13.8886L12.6114 16.1768ZM14.6613 25.2873C14.1864 25.7624 13.5985 26 12.8975 26C12.1965 26 11.6085 25.7624 11.1336 25.2873L1.2127 15.3664C0.737566 14.8915 0.5 14.3035 0.5 13.6025C0.5 12.9015 0.737566 12.3136 1.2127 11.8387L2.97654 10.0614C3.45144 9.58652 4.03801 9.34907 4.73624 9.34907C5.43471 9.34907 6.02139 9.58652 6.49629 10.0614L8.8506 12.4161L12.903 8.36403L10.5483 6.03072C10.0734 5.55582 9.83598 4.96558 9.83598 4.26C9.83598 3.55465 10.0734 2.96452 10.5483 2.48962L12.3256 0.712697C12.8005 0.237566 13.3871 0 14.0853 0C14.7835 0 15.3701 0.237566 15.845 0.712697L25.7873 10.655C26.2624 11.1299 26.5 11.7165 26.5 12.4147C26.5 13.1129 26.2624 13.6995 25.7873 14.1744L24.0104 15.9517C23.5355 16.4266 22.9454 16.664 22.24 16.664C21.5344 16.664 20.9442 16.4266 20.4693 15.9517L18.136 13.597L14.0839 17.6494L16.4386 20.0037C16.9135 20.4786 17.1509 21.0653 17.1509 21.7638C17.1509 22.462 16.9135 23.0486 16.4386 23.5235L14.6613 25.2873Z"
                    fill="#FFF7ED"
                  />
                </g>
                <defs>
                  <clipPath id="clip0_156_1578">
                    <rect
                      width="26"
                      height="26"
                      fill="white"
                      transform="translate(0.5)"
                    />
                  </clipPath>
                </defs>
              </svg>
            </a>
            <a
              href="/user_panel/user_transactions"
              className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
            >
              <p>تراکنش‌ها</p>
              <svg
                width="27"
                height="26"
                viewBox="0 0 27 26"
                fill="#e8eaed"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4.67647 26C3.64902 26 2.77941 25.6629 2.06765 24.9887C1.35588 24.3145 1 23.4908 1 22.5176V20.2944C1 19.9353 1.12684 19.6357 1.38051 19.3956C1.63395 19.1553 1.95025 19.0352 2.32941 19.0352H5.41177V0.489975C5.41177 0.345339 5.47353 0.248527 5.59706 0.199541C5.72059 0.150323 5.83885 0.170404 5.95184 0.259786L7.03235 1.1088C7.16054 1.21234 7.29914 1.26411 7.44816 1.26411C7.59694 1.26411 7.73542 1.21234 7.8636 1.1088L9.09669 0.155314C9.22488 0.0517704 9.36348 0 9.5125 0C9.66152 0 9.80012 0.0517704 9.92831 0.155314L11.1614 1.1088C11.2896 1.21234 11.4281 1.26411 11.5768 1.26411C11.7259 1.26411 11.8645 1.21234 11.9926 1.1088L13.2257 0.155314C13.3539 0.0517704 13.4925 0 13.6415 0C13.7903 0 13.9288 0.0517704 14.057 0.155314L15.2901 1.1088C15.4183 1.21234 15.5569 1.26411 15.7059 1.26411C15.8549 1.26411 15.9935 1.21234 16.1217 1.1088L17.3548 0.155314C17.483 0.0517704 17.6214 0 17.7702 0C17.9192 0 18.0578 0.0517704 18.186 0.155314L19.4191 1.1088C19.5473 1.21234 19.6859 1.26411 19.8349 1.26411C19.9837 1.26411 20.1222 1.21234 20.2504 1.1088L21.4835 0.155314C21.6116 0.0517704 21.7502 0 21.8993 0C22.0483 0 22.1869 0.0517704 22.3151 0.155314L23.5482 1.1088C23.6763 1.21234 23.8148 1.26411 23.9636 1.26411C24.1126 1.26411 24.2512 1.21234 24.3794 1.1088L25.4599 0.259786C25.5729 0.170404 25.6912 0.150323 25.8147 0.199541C25.9382 0.248527 26 0.345339 26 0.489975V22.5176C26 23.4908 25.6441 24.3145 24.9324 24.9887C24.2206 25.6629 23.351 26 22.3235 26H4.67647ZM22.3235 23.9106C22.7402 23.9106 23.0895 23.7771 23.3713 23.5101C23.6532 23.2431 23.7941 22.9123 23.7941 22.5176V3.01611H7.61765V19.0352H19.5239C19.9028 19.0352 20.219 19.1553 20.4724 19.3956C20.7261 19.6357 20.8529 19.9353 20.8529 20.2944V22.5176C20.8529 22.9123 20.9939 23.2431 21.2757 23.5101C21.5576 23.7771 21.9069 23.9106 22.3235 23.9106ZM10.4739 6.15028H16.611C16.9238 6.15028 17.1858 6.25034 17.3971 6.45046C17.6081 6.65035 17.7136 6.89853 17.7136 7.195C17.7136 7.49147 17.6081 7.73965 17.3971 7.93954C17.1858 8.13966 16.9238 8.23972 16.611 8.23972H10.4739C10.1609 8.23972 9.8989 8.13966 9.68787 7.93954C9.47659 7.73965 9.37096 7.49147 9.37096 7.195C9.37096 6.89853 9.47659 6.65035 9.68787 6.45046C9.8989 6.25034 10.1609 6.15028 10.4739 6.15028ZM10.4739 10.3292H16.611C16.9238 10.3292 17.1858 10.4292 17.3971 10.6294C17.6081 10.8292 17.7136 11.0774 17.7136 11.3739C17.7136 11.6704 17.6081 11.9185 17.3971 12.1184C17.1858 12.3186 16.9238 12.4186 16.611 12.4186H10.4739C10.1609 12.4186 9.8989 12.3186 9.68787 12.1184C9.47659 11.9185 9.37096 11.6704 9.37096 11.3739C9.37096 11.0774 9.47659 10.8292 9.68787 10.6294C9.8989 10.4292 10.1609 10.3292 10.4739 10.3292ZM20.768 8.42708C20.408 8.42708 20.1011 8.30705 19.8474 8.067C19.594 7.82671 19.4673 7.53605 19.4673 7.195C19.4673 6.85396 19.594 6.56329 19.8474 6.32301C20.1011 6.08295 20.408 5.96293 20.768 5.96293C21.1281 5.96293 21.4349 6.08295 21.6886 6.32301C21.9423 6.56329 22.0691 6.85396 22.0691 7.195C22.0691 7.53605 21.9423 7.82671 21.6886 8.067C21.4349 8.30705 21.1281 8.42708 20.768 8.42708ZM20.768 12.606C20.408 12.606 20.1011 12.4859 19.8474 12.2459C19.594 12.0056 19.4673 11.7149 19.4673 11.3739C19.4673 11.0328 19.594 10.7422 19.8474 10.5019C20.1011 10.2618 20.408 10.1418 20.768 10.1418C21.1281 10.1418 21.4349 10.2618 21.6886 10.5019C21.9423 10.7422 22.0691 11.0328 22.0691 11.3739C22.0691 11.7149 21.9423 12.0056 21.6886 12.2459C21.4349 12.4859 21.1281 12.606 20.768 12.606ZM4.67647 23.9106H18.6471V21.1246H3.20588V22.5176C3.20588 22.9123 3.34681 23.2431 3.62868 23.5101C3.91054 23.7771 4.2598 23.9106 4.67647 23.9106Z"
                  fill="#FFF7ED"
                />
              </svg>
            </a>
          </div>
        </div>
        <a
          href="/"
          className="text-superRed font-medium text-[20px] flex justify-center mx-auto mt-5 hover:text-mintCream transition-all duration-300"
        >
          خروج
        </a>
      </div>
      <div className="flex flex-col gap-5 justify-start w-[95%] py-[40px]">
        <div className="flex justify-between">
          <h1 className="text-[45px] font-bold text-mintCream">
            درخواست برنامه غذایی
          </h1>
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
                <img
                  src="/Images/payton-tuttle-RFFR1JjkJx8-unsplash.jpg"
                  alt="User Avatar"
                  className="w-full max-h-[250px] object-cover"
                />
                <p className="mt-3 text-lg font-semibold text-superRed">
                  {userInfo.nameSurname}
                </p>
                <p className="mt-2 text-lg text-superRed font-light">
                  {userInfo.username}@
                </p>
              </div>
              <div className="overflow-y-auto font-medium max-h-[330px] scrollbar-thin scrollbar-thumb-superRed scrollbar-track-coal">
                <div className="flex flex-col gap-1 p-2">
                  <a
                    href="/user_panel"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>اطلاعات کاربر</p>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      height="35px"
                      viewBox="0 -960 960 960"
                      width="35px"
                      fill="#e8eaed"
                    >
                      <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
                    </svg>
                  </a>
                  <a
                    href="/user_panel/user_coach"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>مربی</p>
                    <div className="h-[30px]">
                      <img
                        src="/Images/bodybuilding-White.png"
                        alt="coaches_icon"
                        className="h-full"
                      />
                    </div>
                  </a>
                  <a
                    href="/user_panel/user_tutorial"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>آموزش حرکات</p>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      height="24px"
                      viewBox="0 -960 960 960"
                      width="24px"
                      fill="#e8eaed"
                    >
                      <path d="M160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h480q33 0 56.5 23.5T720-720v180l126-126q10-10 22-5t12 19v344q0 14-12 19t-22-5L720-420v180q0 33-23.5 56.5T640-160H160Zm0-80h480v-480H160v480Zm0 0v-480 480Z" />
                    </svg>
                  </a>
                  <a
                    href="/user_panel/user_mealPlan"
                    className="w-[90%] border-[2px] border-crimsonRed bg-crimsonRed text-black text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>برنامه غذایی</p>
                    <svg
                      width="28"
                      height="28"
                      viewBox="0 0 28 28"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M7.41475 10.154V2C7.41475 1.71667 7.51235 1.47922 7.70756 1.28767C7.90276 1.09589 8.14457 1 8.43296 1C8.72159 1 8.96328 1.09589 9.15803 1.28767C9.35301 1.47922 9.4505 1.71667 9.4505 2V10.154H11.3298V2C11.3298 1.71667 11.4273 1.47922 11.6223 1.28767C11.8175 1.09589 12.0594 1 12.3481 1C12.6364 1 12.8781 1.09589 13.0731 1.28767C13.2679 1.47922 13.3652 1.71667 13.3652 2V10.154C13.3652 11.3471 12.9882 12.374 12.234 13.2347C11.4797 14.0953 10.5518 14.6428 9.4505 14.877V26C9.4505 26.2833 9.3529 26.5208 9.15769 26.7123C8.96248 26.9041 8.72068 27 8.43228 27C8.14366 27 7.90197 26.9041 7.70722 26.7123C7.51224 26.5208 7.41475 26.2833 7.41475 26V14.877C6.31341 14.6428 5.38556 14.0953 4.6312 13.2347C3.87707 12.374 3.5 11.3471 3.5 10.154V2C3.5 1.71667 3.5976 1.47922 3.79281 1.28767C3.98779 1.09589 4.22959 1 4.51821 1C4.80661 1 5.0483 1.09589 5.24328 1.28767C5.43803 1.47922 5.53541 1.71667 5.53541 2V10.154H7.41475ZM20.4642 16.3333H17.9867C17.6359 16.3333 17.3434 16.2179 17.1093 15.987C16.8754 15.7559 16.7585 15.4697 16.7585 15.1283V7.33333C16.7585 5.658 17.2517 4.18367 18.2382 2.91033C19.2246 1.63678 20.2267 1 21.2446 1C21.6258 1 21.9303 1.13422 22.1583 1.40267C22.3861 1.67089 22.5 2.00767 22.5 2.413V26C22.5 26.2833 22.4024 26.5208 22.2072 26.7123C22.0122 26.9041 21.7704 27 21.4818 27C21.1934 27 20.9517 26.9041 20.7567 26.7123C20.5617 26.5208 20.4642 26.2833 20.4642 26V16.3333Z"
                        fill="black"
                      />
                    </svg>
                  </a>
                  <a
                    href="/user_panel/user_exercisePlan"
                    className="w-[90%] border-[2px] border-crimsonRed bg-coal text-mintCream text-[20px] flex justify-between rounded-[10px] max-h-[58px] mx-auto mt-3 py-3 px-3 hover:bg-superRed hover:border-superRed transition-all duration-300"
                  >
                    <p>برنامه تمرینی</p>
                    <svg
                      width="27"
                      height="26"
                      viewBox="0 0 27 26"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g clip-path="url(#clip0_156_1578)">
                        <path
                          d="M24.5347 9.40209L23.0966 7.96395L23.9439 7.08221C24.0323 6.99384 24.0765 6.89445 24.0765 6.78405C24.0765 6.67364 24.0323 6.57437 23.9439 6.48623L20.0138 2.55607C19.9256 2.4677 19.8264 2.42351 19.716 2.42351C19.6055 2.42351 19.5062 2.4677 19.4178 2.55607L18.536 3.40339L17.0635 1.93082L17.9638 0.996054C18.43 0.529874 19.0047 0.302523 19.6881 0.314C20.3714 0.325476 20.9461 0.564304 21.4123 1.03048L25.4695 5.08769C25.9357 5.55387 26.1688 6.12288 26.1688 6.79472C26.1688 7.46656 25.9357 8.03557 25.4695 8.50175L24.5347 9.40209ZM9.00175 24.9695C8.53557 25.4357 7.96656 25.6688 7.29472 25.6688C6.62288 25.6688 6.05387 25.4357 5.58769 24.9695L1.58351 20.965C1.10837 20.4901 0.870809 19.9035 0.870809 19.2053C0.870809 18.507 1.10837 17.9204 1.58351 17.4452L2.43082 16.5979L3.90338 18.0705L3.03472 18.9178C2.94635 19.0062 2.90217 19.1055 2.90217 19.216C2.90217 19.3264 2.94635 19.4256 3.03472 19.5138L6.98623 23.4653C7.07437 23.5536 7.17364 23.5978 7.28405 23.5978C7.39445 23.5978 7.49384 23.5536 7.58221 23.4653L8.42952 22.5966L9.90209 24.0692L9.00175 24.9695ZM22.5378 14.5005L24.3017 12.7366C24.39 12.6482 24.4342 12.5467 24.4342 12.4319C24.4342 12.3171 24.39 12.2156 24.3017 12.1272L14.3728 2.19834C14.2844 2.10997 14.1829 2.06579 14.0681 2.06579C13.9533 2.06579 13.8518 2.10997 13.7634 2.19834L11.9995 3.96218C11.9114 4.05055 11.8673 4.14982 11.8673 4.26C11.8673 4.3704 11.9114 4.46979 11.9995 4.55816L21.9418 14.5005C22.0302 14.5886 22.1296 14.6327 22.24 14.6327C22.3502 14.6327 22.4494 14.5886 22.5378 14.5005ZM13.2022 23.8361L14.966 22.0509C15.0542 21.9628 15.0982 21.8635 15.0982 21.7531C15.0982 21.6427 15.0542 21.5434 14.966 21.4553L5.04473 11.534C4.95659 11.4458 4.85732 11.4018 4.74691 11.4018C4.63651 11.4018 4.53724 11.4458 4.4491 11.534L2.66391 13.2978C2.57554 13.3862 2.53136 13.4878 2.53136 13.6025C2.53136 13.7173 2.57554 13.8189 2.66391 13.9072L12.5928 23.8361C12.6811 23.9245 12.7827 23.9686 12.8975 23.9686C13.0122 23.9686 13.1138 23.9245 13.2022 23.8361ZM12.6114 16.1768L16.6638 12.1458L14.3542 9.83625L10.3232 13.8886L12.6114 16.1768ZM14.6613 25.2873C14.1864 25.7624 13.5985 26 12.8975 26C12.1965 26 11.6085 25.7624 11.1336 25.2873L1.2127 15.3664C0.737566 14.8915 0.5 14.3035 0.5 13.6025C0.5 12.9015 0.737566 12.3136 1.2127 11.8387L2.97654 10.0614C3.45144 9.58652 4.03801 9.34907 4.73624 9.34907C5.43471 9.34907 6.02139 9.58652 6.49629 10.0614L8.8506 12.4161L12.903 8.36403L10.5483 6.03072C10.0734 5.55582 9.83598 4.96558 9.83598 4.26C9.83598 3.55465 10.0734 2.96452 10.5483 2.48962L12.3256 0.712697C12.8005 0.237566 13.3871 0 14.0853 0C14.7835 0 15.3701 0.237566 15.845 0.712697L25.7873 10.655C26.2624 11.1299 26.5 11.7165 26.5 12.4147C26.5 13.1129 26.2624 13.6995 25.7873 14.1744L24.0104 15.9517C23.5355 16.4266 22.9454 16.664 22.24 16.664C21.5344 16.664 20.9442 16.4266 20.4693 15.9517L18.136 13.597L14.0839 17.6494L16.4386 20.0037C16.9135 20.4786 17.1509 21.0653 17.1509 21.7638C17.1509 22.462 16.9135 23.0486 16.4386 23.5235L14.6613 25.2873Z"
                          fill="#FFF7ED"
                        />
                      </g>
                      <defs>
                        <clipPath id="clip0_156_1578">
                          <rect
                            width="26"
                            height="26"
                            fill="white"
                            transform="translate(0.5)"
                          />
                        </clipPath>
                      </defs>
                    </svg>
                  </a>
                  <a
                    href="/user_panel/user_transactions"
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
                </div>
              </div>
              <a
                href="/"
                className="text-superRed font-medium text-[20px] flex justify-center mx-auto mt-5 hover:text-mintCream transition-all duration-300"
              >
                خروج
              </a>
            </div>
          </div>
        </div>
        <div className="my-[50px] rounded-[10px] h-full overflow-hidden flex justify-centert text-mintCream">
          <form className="flex flex-col gap-[20px] justify-center text-center text-mintCream w-full">
            <h1 className="text-[35px] font-medium">
              لطفا اطلاعات خواسته شده را وارد کنید
            </h1>
            <div className="flex justify-between max-lg:justify-center max-lg:flex-col max-lg:mx-auto max-lg:gap-6 w-full">
              <div className="flex flex-col gap-2 justify-center text-center">
                <label htmlFor="weight" className="font-medium">
                  وزن(کیلوگرم):
                </label>
                <input
                  type="number"
                  name="weight"
                  id="weight"
                  step="0.01"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  placeholder="80.00"
                  className={`text-center text-[15px] w-[100%] py-2 bg-coal border-[2px] rounded-[10px] ${
                    showError && !weight ? "border-superRed" : "border-white"
                  }`}
                />
              </div>
              <div className="flex flex-col gap-2 justify-center text-center">
                <label htmlFor="weight" className="font-medium">
                  دور کمر(سانتی‌متر):
                </label>
                <input
                  type="number"
                  name="weight"
                  id="weight"
                  step="0.01"
                  value={waistSize}
                  onChange={(e) => setWaistSize(e.target.value)}
                  placeholder="50.00"
                  className={`text-center text-[15px] w-[100%] py-2 bg-coal border-[2px] rounded-[10px] ${
                    showError && !weight ? "border-superRed" : "border-white"
                  }`}
                />
              </div>
              <div className="flex gap-2 justify-center text-center">
                <label className="flex items-center gap-2 border-[2px] text-[20px] font-medium rounded-[15px] px-[10px]">
                  <input
                    type="radio"
                    name="exercisePlan"
                    value="کات"
                    checked={selectedPlan === "کات"}
                    onChange={handlePlanType}
                    className="appearance-none w-5 h-5 rounded-full border border-gray-300 checked:bg-irishGreen checked:border-irishGreen focus:outline-none focus:ring-2 focus:ring-irishGreen"
                  />
                  <span className="ml-2 text-mintCream">کات</span>
                </label>
                <label className="flex items-center gap-2 border-[2px] text-[20px] font-medium rounded-[15px] px-[10px]">
                  <input
                    type="radio"
                    name="exercisePlan"
                    value="حجم"
                    checked={selectedPlan === "حجم"}
                    onChange={handlePlanType}
                    className="appearance-none w-5 h-5 rounded-full border border-gray-300 checked:bg-irishGreen checked:border-irishGreen focus:outline-none focus:ring-2 focus:ring-irishGreen"
                  />
                  <span className="ml-2 text-mintCream">حجم</span>
                </label>
              </div>
              <div className="flex flex-col gap-2 justify-center mx-auto text-center">
                <h1 className="font-medium">تصاویر شما</h1>
                <label
                  htmlFor="file-input"
                  className="flex items-center justify-center w-48 h-[40px] bg-mintCream text-black font-medium rounded-lg cursor-pointer hover:bg-irishGreen transition-all duration-300"
                >
                  افزودن تصویر
                </label>
                <input
                  id="file-input"
                  type="file"
                  accept="image/*"
                  multiple
                  className="hidden"
                  onChange={handleFileChange}
                />
              </div>
            </div>
            <p className={`text-superRed ${showError ? "block" : "hidden"}`}>
              لطفا فیلدهای الزامی را پر کنید.
            </p>
            <div className="flex justify-normal">
              <p
                className={`text-[25px] font-medium pt-[55px] ${
                  preview ? "block" : "hidden"
                }`}
              >
                تصاویر شما:
              </p>
              <div className="flex justify-center mx-auto gap-4 mt-6 ">
                {images.map((image, index) => (
                  <div key={index} className="relative w-32 h-32">
                    <img
                      src={URL.createObjectURL(image)}
                      alt={`preview ${index}`}
                      className="w-full h-full object-cover rounded-lg"
                    />
                  </div>
                ))}
              </div>
            </div>
            <div className="flex flex-col gap-6 text-right max-lg:text-center text-midtoneGray text-[18px] mt-[20px]">
              <p>
                برای دریافت راهنمای اندازه‌گیری دور کمر
                <span className="text-superRed hover:text-crimsonRed transition-all duration-300">
                  <button onClick={handleDownload}>اینجا</button>
                </span>{" "}
                کلیک کنید.
              </p>
              <p>
                <span className="text-superRed">برنامه حجم </span>برنامه‌ای است
                برای افزایش توده عضلانی و قدرت
              </p>
              <p>
                <span className="text-superRed">برنامه کات </span>برنامه‌ای است
                برای کاهش درصد چربی بدن و حفظ توده عضلانی
              </p>
              <p className="w-[517px]">
                <span className="text-superRed">تصویر ارسالی </span>باید از روبه
                رو و پشت (با فیگور جلو بازو) و از نیم‌رخ (با بازوانی که اندکی به
                سمت عقب نگاه داشته شده‌اند) باشد.
              </p>
            </div>

            <p className="mt-[60px] text-[25px] font-medium">
              مبلغ قابل پرداخت: 1,000,000 تومان
            </p>
            <button
              type="submit"
              onClick={handleSubmit}
              className="text-irishGreen text-[20px] font-medium mt-[50px] border-[2px] border-irishGreen max-w-[282px] mx-auto py-1 px-5 rounded-[10px] hover:bg-irishGreen hover:text-black transition-all duration-300"
            >
              درخواست برنامه غذایی
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
