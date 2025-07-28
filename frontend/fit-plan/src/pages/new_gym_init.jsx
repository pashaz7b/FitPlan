import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import Testing_header from "../components/testing_header";
import Footer_comp from "../components/footer_comp";
import peoson_svg from "/SVGs/person_24dp_E8EAED_FILL0_wght300_GRAD0_opsz24.svg";
import fit_logo from "/Images/Fit-Logo-Resized.png";

export default function New_gym_init() {
  const [showError, setShowError] = useState(false);
  const [otp, setOtp] = useState("");
  const [gymName, setGymName] = useState("");
  const [bussinessLis, setBussinessLis] = useState("");
  const [imagePreview, setImagePreview] = useState(null);
  const [location, setLocation] = useState("");
  const [sportFacility, setSportFacility] = useState("");
  const [facilities, setFacilities] = useState("");
  const [formNum, setFormNum] = useState(1);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  async function handleSubmit_1(e) {
    e.preventDefault();

    if (!gymName) {
      setShowError(true);
      console.log(showError);

      return;
    }
    setShowError(false);
    setFormNum(2);
  }

  async function handleSubmit_2(e) {
    e.preventDefault();

    if (!bussinessLis) {
      setShowError(true);
      console.log(showError);

      return;
    }
    setShowError(false);
    setFormNum(3);
  }

  async function handleSubmit_3(e) {
    e.preventDefault();

    if (!bussinessLis) {
      setShowError(true);
      console.log(showError);

      return;
    }
    setShowError(false);
    setFormNum(4);
  }

  async function handleSubmit_4(e) {
    e.preventDefault();

    if (!location) {
      setShowError(true);
      console.log(showError);

      return;
    }
    setShowError(false);
    setFormNum(5);
  }

  async function handleSubmit_5(e) {
    e.preventDefault();
    setFormNum(6);
  }

  async function handleSubmit_6(e) {
    e.preventDefault();
    setFormNum(7);
  }

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
                نام باشگاه
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
                اول از همه اسم باشگاه شما چیه؟
              </p>
              <input
                type="text"
                value={gymName}
                name="gym_name"
                id={gymName}
                onChange={(e) => setGymName(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !gymName ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="باشگاه اندام‌پروران"
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
                پروانه کسب
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
                لطفا شماره پروانه کسب خود را وارد کنید
              </p>
              <input
                type="text"
                value={bussinessLis}
                name="bussinessLis"
                id={bussinessLis}
                onChange={(e) => setBussinessLis(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !bussinessLis ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="شماره پروانه کسب"
              />
              <p className="text-[15px] text-midtoneGray mt-5">
                لطفا تصویر پروانه کسب خود را آپلود کنید
              </p>
              <div className="max-sm:flex max-sm:flex-col-reverse max-sm:text-center max-sm:mx-auto max-sm:items-center flex justify-between gap-5 align-bottom items-end mt-auto">
                <label
                  htmlFor="upload"
                  className="h-[35px] w-auto px-5 text-black bg-mintCream rounded-lg cursor-pointer hover:bg-irishGreen hover:text-mintCream transition"
                >
                  افزودن تصویر
                </label>
                <input
                  type="file"
                  id="upload"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="hidden"
                />
                <div className="w-32 h-32 border-[2px] border-white rounded-[15px] flex items-center justify-center">
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

        {/* Third form */}
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
                تصاویر باشگاه
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
                با گذاشتن عکس از باشگاهتون ورزشکارای بیشتری رو به باشگاهتون جذب
                کنین
              </p>
              {/* <input
                type="number"
                value={bussinessLis}
                name="bussinessLis"
                id={bussinessLis}
                onChange={(e) => setBussinessLis(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !bussinessLis ? "border-superRed" : "border-coal"
                }`}
                // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
                placeholder="َشماره پروانه کسب"
              /> */}
              <div className="max-sm:flex max-sm:flex-col-reverse max-sm:text-center max-sm:mx-auto max-sm:items-center flex justify-between gap-5 align-bottom items-end mt-auto">
                <label
                  htmlFor="upload"
                  className="h-[35px] w-auto text-center mx-auto px-5 text-black bg-mintCream border border-irishGreen rounded-lg cursor-pointer hover:bg-irishGreen hover:text-mintCream transition"
                >
                  افزودن تصویر
                </label>
                <input
                  type="file"
                  id="upload"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="hidden"
                />
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

        {/* Fourth form */}
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

            <div className="my-6 w-[80%] max-sm:w-[90%] mx-auto flex flex-col justify-start text-right">
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2"
                htmlFor="email_input_box"
              >
                مکان باشگاه
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
                باشگاه شما رو کجا میشه پیدا کرد؟
              </p>
              <input
                type="text"
                value={location}
                name="location"
                id={location}
                onChange={(e) => setLocation(e.target.value)}
                className={`email text-center text-[15px] py-2 bg-mintCream border rounded-[10px] ${
                  showError && !location ? "border-superRed" : "border-coal"
                }`}
                placeholder="تهران، میدان تجریش..."
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
              <label
                className="text-[20px] max-md:text-[15px] font-bold mb-2"
                htmlFor="email_input_box"
              >
                امکانات ورزشی
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
              از امکانات ورزشی باشگاهتون بگین
              تا معلوم بشه چقدر از رقباتون جلوتر هستین!
              </p>
              <textarea
                id="sport_fclt"
                cols="30"
                rows="5"
                onChange={(e) => setSportFacility(e.target.value)}
                className="border rounded-[15px] bg-gray-300 p-3 w-full resize-none"
                placeholder="دستگاه پرواز - پرس تخت دستگاه -  دستگاه پشت پا ایستاده - دستگاه ساق پا نشسته - دستگاه لت بالا - ..."
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
                امکانات رفاهی
              </label>
              <p className="text-[15px] text-midtoneGray mb-5">
              اینجا بنویسین که با چه امکانات رفاهی‌ای‌
              میتونین تجربه‌ی بهتری به ورزشکارا ارائه کنین
              </p>
              <textarea
                id="breakfast"
                cols="30"
                rows="5"
                onChange={(e) => setAchievement(e.target.value)}
                className="border rounded-[15px] bg-gray-300 p-3 w-full resize-none"
                placeholder="بوفه - حمام - سرویس بهداشتی - سیستم خنک کننده سراسری - سیستم تهویه مطبوع قوی - ..."
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
          <p>{`مرحله ${formNum} از 6`}</p>
        </div>
      </div>
      <Footer_comp />
    </div>
  );
}
