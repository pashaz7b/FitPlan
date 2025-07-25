import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import Testing_header from "../components/testing_header";
import Footer_comp from "../components/footer_comp";
import fit_logo from "/Images/Fit-Logo-Resized.png";

export default function New_gym_init() {
  const [showError, setShowError] = useState(false);
  const [otp, setOtp] = useState("");
  const [gymName, setGymName] = useState("");
  const [bussinessLis, setBussinessLis] = useState("");
  const [sportFacility, setSportFacility] = useState("");
  const [facilities, setFacilities] = useState("");
  const [formNum, setFormNum] = useState(1);

  async function handleSubmit_1(e) {
    e.preventDefault();
    handleMail();

    if (!mail) {
      setShowError(true);
      console.log(showError);

      return;
    }
    setShowError(false);
    setFormNum(2);
  }

  async function handleSubmit_2(e) {
    e.preventDefault();

    if (!otp || !/^[0-9]{5}/.test(otp)) {
      setShowError(true);
      console.log(showError);
      return;
    }
    setShowError(false);
    setFormNum(3);
  }

  async function handleSubmit_3(e) {
    e.preventDefault();

    if (!coachingCardId || !nationalID) {
      setShowError(true);
      console.log(showError);
      return;
    }
    setShowError(false);
    setFormNum(4);
  }
  async function handleSubmit_4(e) {
    e.preventDefault();

    if (!userID || !password || !passwordConf) {
      setShowError(true);
      console.log(showError);
      return;
    }

    if (password != passwordConf) {
      setShowPassError(true);
      console.log(showPassError);
      return;
    }
    setShowError(false);
    setShowPassError(false);
    setFormNum(5);
  }
  async function handleSubmit_5(e) {
    e.preventDefault();

    if (!birthDate || !height || !weight) {
      setShowError(true);
      console.log(showError);
      return;
    }
    setShowError(false);
    setFormNum(6);
  }
  async function handleSubmit_6(e) {
    e.preventDefault();

    setFormNum(7);
  }

  async function backToLanding() {
    useNavigate("/");
  }

  const handleMail = (e) => {
    if (!/^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com)$/.test(mail)) {
      setShowError(true);
      console.log(mail);
    } else {
      setShowError(false);
    }
  };
  return (
    <div className="h-screen w-full bg-mintCream font-iranyekan text-coal">
      <Testing_header />
      <div className="pt-20 mx-auto text-center">
        {/* first form */}
        <form
          onSubmit={handleSubmit_1}
          className={`w-[25%] max-md:w-[75%] text-center pt-6 mb-[122px] mx-auto border border-coal rounded-[10px] ${
            formNum === 1 ? "flex" : "hidden"
          }`}
        >
          <div className="flex flex-col p-3 w-full text-center justify-center">
            <img src={fit_logo} alt="fit_plan_logo" className="w-1/3 mx-auto" />
            <p
              className={`pt-5 text-superRed text-[15px] ${
                showError ? "block" : "hidden"
              }`}
            >
              لطفا فیلدهای الزامی را پر کنید
            </p>

            <div className="my-6 w-[80%] max-sm:w-[90%] mx-auto flex flex-col justify-start text-right">
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2"
                htmlFor="email_input_box"
              >
                شماره تماس یا آدرس ایمیل
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
                لطفا آدرس ایمیل یاهو یا جیمیل وارد کند
              </p>
              <input
                type="text"
                value={mail}
                name="email"
                id={mail}
                onChange={(e) => setMail(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !mail ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="آدرس ایمیل یاهو یا جیمیل"
              />
            </div>
            <button
              type="submit"
              id="submit_button"
              className="text-mintCream bg-irishGreen hover:bg-green-800 h-[40px] text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300"
            >
              {/* <a href={`/otp_page/${role}`}>ورود</a> */}
              تائید
            </button>
          </div>
        </form>

        {/* second form */}
        <form
          onSubmit={handleSubmit_2}
          className={`w-[25%] max-md:w-[75%] text-center pt-6 mb-[122px] mx-auto border border-coal rounded-[10px] ${
            formNum === 2 ? "flex" : "hidden"
          }`}
        >
          <div className="flex flex-col p-3 w-full text-center justify-center">
            <img src={fit_logo} alt="fit_plan_logo" className="w-1/3 mx-auto" />
            <p
              className={`pt-5 text-superRed text-[15px] ${
                showError ? "block" : "hidden"
              }`}
            >
              لطفا فیلدهای الزامی را پر کنید
            </p>

            <div className="my-6 w-[80%] max-sm:w-[90%] mx-auto flex flex-col justify-start text-right">
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2"
                htmlFor="email_input_box"
              >
                تائید آدرس ایمیل
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
                لطفا کد 5 رقمی‌ای که پیامک شد را اینجا وارد کنید
              </p>
              <input
                type="text"
                value={otp}
                name="otp"
                id={otp}
                onChange={(e) => setOtp(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !otp ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="1 5 9 7 5"
              />
            </div>
            <button
              type="submit"
              id="submit_button"
              className="text-mintCream bg-irishGreen hover:bg-green-800 h-[40px] text-[15px] font-medium max-md:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300"
            >
              {/* <a href={`/otp_page/${role}`}>ورود</a> */}
              تائید آدرس ایمیل
            </button>
          </div>
        </form>

        {/* third form */}
        <form
          onSubmit={handleSubmit_3}
          className={`w-[25%] max-md:w-[75%] text-center pt-6 mb-[122px] mx-auto border border-coal rounded-[10px] ${
            formNum === 3 ? "flex" : "hidden"
          }`}
        >
          <div className="flex flex-col p-3 w-full text-center justify-center">
            <img src={fit_logo} alt="fit_plan_logo" className="w-1/3 mx-auto" />
            <p
              className={`pt-5 text-superRed text-[15px] ${
                showError ? "block" : "hidden"
              }`}
            >
              لطفا فیلدهای الزامی را پر کنید
            </p>

            <div className="my-6 w-[80%] max-sm:w-[90%] mx-auto flex flex-col justify-start text-right">
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2"
                htmlFor="email_input_box"
              >
                کد ملی
              </label>
              <p className="text-[15px] text-midtoneGray mb-2">
                لطفا کد ملی خود را وارد کنید
              </p>
              <input
                type="text"
                value={nationalID}
                name="nationalID"
                id={nationalID}
                onChange={(e) => setNationalID(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !nationalID ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="2051234567"
              />
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2 mt-6"
                htmlFor="email_input_box"
              >
                شناسه مربی‌گری
              </label>
              <p className="text-[15px] text-midtoneGray mb-2">
                لطفا شناسه‌ی کارت مربی‌گری خود را وارد کنید
              </p>
              <input
                type="text"
                value={coachingCardId}
                name="coachingCardId"
                id={coachingCardId}
                onChange={(e) => setCoachingCardId(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !coachingCardId
                    ? "border-superRed"
                    : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="110/12345"
              />
            </div>
            <button
              type="submit"
              id="submit_button"
              className="text-mintCream bg-irishGreen hover:bg-green-800 h-[40px] text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300"
            >
              {/* <a href={`/otp_page/${role}`}>ورود</a> */}
              تائید
            </button>
          </div>
        </form>

        {/* fourth form */}
        <form
          onSubmit={handleSubmit_4}
          className={`w-[25%] max-md:w-[75%] text-center pt-6 mb-[122px] mx-auto border border-coal rounded-[10px] ${
            formNum === 4 ? "flex" : "hidden"
          }`}
        >
          <div className="flex flex-col p-3 w-full text-center justify-center">
            <img src={fit_logo} alt="fit_plan_logo" className="w-1/3 mx-auto" />
            <p
              className={`pt-5 text-superRed text-[15px] ${
                showError ? "block" : "hidden"
              }`}
            >
              لطفا فیلدهای الزامی را پر کنید
            </p>
            <p
              className={`pt-5 text-superRed text-[15px] ${
                showPassError ? "block" : "hidden"
              }`}
            >
              گذرواژه تکرار شده صحیح نیست
            </p>

            <div className="my-6 w-[80%] max-sm:w-[90%] mx-auto flex flex-col justify-start text-right">
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2"
                htmlFor="username"
              >
                نام کاربری
              </label>
              <p className="text-[15px] text-midtoneGray mb-1">
                لطفا نام‌کاربری منحصر به فردی بسازید
              </p>
              <input
                type="text"
                value={userID}
                name="userID"
                id={userID}
                onChange={(e) => setUserID(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !userID ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="MyUserName"
              />
              <label
                className="text-[20px] max-md:text-[15px] font-bold mt-6  mb-1"
                htmlFor="email_input_box"
              >
                گذرواژه
              </label>
              <p className="text-[15px] text-midtoneGray mb-1">
                لطفا یک گذرواژه برای خود تعیین کنید
              </p>
              <input
                type="text"
                value={password}
                name="password"
                id={password}
                onChange={(e) => setPassword(e.target.value)}
                className={`email text-center text-[15px] my-1 py-2 bg-mintCream border rounded-[10px] ${
                  showError && !password ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="********"
              />
              <p className="text-[15px] text-midtoneGray mb-1">
                لطفا گذرواژه خود را تکرار کنید
              </p>
              <input
                type="text"
                value={passwordConf}
                name="passwordConf"
                id={passwordConf}
                onChange={(e) => setPasswordConf(e.target.value)}
                className={`email text-center text-[15px] my-1 py-2 bg-mintCream border rounded-[10px] ${
                  showError && !passwordConf ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="********"
              />
            </div>
            <button
              type="submit"
              id="submit_button"
              className="text-mintCream bg-irishGreen hover:bg-green-800 h-[40px] text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300"
            >
              {/* <a href={`/otp_page/${role}`}>ورود</a> */}
              تائید
            </button>
          </div>
        </form>

        {/* fifth form */}
        <form
          onSubmit={handleSubmit_5}
          className={`w-[25%] max-md:w-[75%] text-center pt-6 mb-[122px] mx-auto border border-coal rounded-[10px] ${
            formNum === 5 ? "flex" : "hidden"
          }`}
        >
          <div className="flex flex-col p-3 w-full text-center justify-center">
            <img src={fit_logo} alt="fit_plan_logo" className="w-1/3 mx-auto" />
            <p
              className={`pt-5 text-superRed text-[15px] ${
                showError ? "block" : "hidden"
              }`}
            >
              لطفا فیلدهای الزامی را پر کنید
            </p>

            <div className="my-6 w-[80%] max-sm:w-[90%] mx-auto flex flex-col justify-start text-right">
              <div className="max-sm:flex max-sm:flex-col max-sm:text-center max-sm:mx-auto flex flex-col text-right">
                <label
                  className="text-[20px] max-md:text-[15px] font-bold mb-2"
                  htmlFor="username"
                >
                  اطلاعات حرفه‌ای
                </label>
                <div className="flex gap-1 max-md:flex-col">
                  <div className="w-[60%] max-md:w-full">
                    <label htmlFor="birthDate" className="mb-3">
                      تاریخ تولد
                    </label>
                    <input
                      type="text"
                      value={birthDate}
                      onChange={(e) => setBirthDate(e.target.value)}
                      className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-mintCream border rounded-[10px] ${
                        showError && !birthDate
                          ? "border-superRed"
                          : "border-coal"
                      }`}
                      placeholder="1380/8/22"
                    />
                  </div>
                  <div className="w-[40%] max-md:w-full">
                    <label htmlFor="gender" className="mb-3">
                      جنسیت
                    </label>
                    <select
                      name="gender"
                      id="gender"
                      value={gender}
                      onChange={(e) => setGender(e.target.value)}
                      className={`text-right text-[15px] w-[100%] py-2 bg-mintCream border rounded-[10px] ${
                        showError ? "border-superRed" : "border-coal"
                      }`}
                    >
                      <option value="آقا">آقا</option>
                      <option value="خانم">خانم</option>
                    </select>
                  </div>
                </div>
                <div className="flex mt-3 gap-1  max-md:flex-col">
                  <div className="w-[50%] max-md:w-full">
                    <label htmlFor="height" className="mb-3">
                      قد(سانتی‌متر)
                    </label>
                    <input
                      type="number"
                      value={height}
                      step="0.01"
                      min="0.00"
                      onChange={(e) => setHeight(e.target.value)}
                      className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-mintCream border rounded-[10px] ${
                        showError && !height ? "border-superRed" : "border-coal"
                      }`}
                    />
                  </div>
                  <div className="w-[50%] max-md:w-full">
                    <label htmlFor="weight" className="mb-3">
                      وزن(کیلوگرم)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      min="30"
                      value={weight}
                      onChange={(e) => setWeight(e.target.value)}
                      className={`text-center text-[15px] px-[30px] w-[100%] py-2 bg-mintCream border rounded-[10px] ${
                        showError && !weight ? "border-superRed" : "border-coal"
                      }`}
                    />
                  </div>
                </div>
              </div>
            </div>
            <button
              type="submit"
              id="submit_button"
              className="text-mintCream bg-irishGreen hover:bg-green-800 h-[40px] text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300"
            >
              {/* <a href={`/otp_page/${role}`}>ورود</a> */}
              تائید
            </button>
          </div>
        </form>

        {/* sixth form */}
        <form
          onSubmit={handleSubmit_6}
          className={`w-[25%] max-md:w-[75%] text-center pt-6 mb-[122px] mx-auto border border-coal rounded-[10px] ${
            formNum === 6 ? "flex" : "hidden"
          }`}
        >
          <div className="flex flex-col p-3 w-full text-center justify-center">
            <img src={fit_logo} alt="fit_plan_logo" className="w-1/3 mx-auto" />
            <p
              className={`pt-5 text-superRed text-[15px] ${
                showError ? "block" : "hidden"
              }`}
            >
              لطفا فیلدهای الزامی را پر کنید
            </p>

            <div className="my-6 w-[80%] max-sm:w-[90%] mx-auto flex flex-col justify-start text-right">
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2"
                htmlFor="email_input_box"
              >
                افتخارات
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
                لطفا به عنوان یک مربی از افتخارات و قهرمانی‌ها در مسابقاتی که
                شرکت کرده‌اید بنویسید
              </p>
              <textarea
                id="breakfast"
                cols="30"
                rows="10"
                onChange={(e) => setAchievement(e.target.value)}
                className="border rounded-[15px] bg-gray-300 p-3 w-full resize-none"
                placeholder="قهرمانی در مسابقات..."
              ></textarea>
            </div>
            <button
              type="submit"
              id="submit_button"
              className="text-mintCream bg-irishGreen hover:bg-green-800 h-[40px] text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300"
            >
              {/* <a href={`/otp_page/${role}`}>ورود</a> */}
              تائید
            </button>
          </div>
        </form>

        <div
          className={`${formNum === 7 ? "flex" : "hidden"} text-center mx-auto`}
        >
          <div className="text-center mx-auto mb-[50px]">
            <img src={fit_logo} alt="" className="w-1/6 text-center mx-auto" />
            <h2 className="mt-10 font-bold text-[25px]">
              ممنون از وقتی که گذاشتین
            </h2>
            <p className="w-1/3 max-md:full text-center mx-auto mt-4">
              درخواست شما به دست ادمین بررسی و نتیجه از طریق{" "}
              <span className="font-bold">پیامک</span> به شما اعلام خواهد شد.
              سپاس از شکیبایی شما!
            </p>
            <div className="my-10">
              <a
                href="/"
                className=" bg-irishGreen text-mintCream border border-irishGreen px-5 py-2 rounded-[10px] hover:bg-mintCream hover:text-irishGreen transition-all duration-300"
              >
                بازگشت به صفحه اصلی
              </a>
            </div>
          </div>
        </div>

        <div
          className={`${
            formNum < 7 ? "block" : "hidden"
          } mb-3 text-midtoneGray`}
        >
          <p>{`مرحله ${formNum} از 5`}</p>
        </div>
      </div>
      <Footer_comp />
    </div>
  );
}
