import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login_component({ role }) {
  const [phoneOrMail, setPhoneOrMail] = useState("");
  const [password, setPassword] = useState("");
  const [showError, setShowError] = useState(false);
  const [mailError, setMailError] = useState(false);
  // const { role } = useParams();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    handleMail();

    if (!phoneOrMail || !password) {
      setShowError(true);
      return;
    }
    setShowError(false);

    try {
      if (role === "user") {
        // Create form data
        const formData = new URLSearchParams();
        formData.append("grant_type", "password");
        formData.append("username", phoneOrMail);
        formData.append("password", password);

        const res = await axios.post(
          "http://iam.localhost/api/v1/users/login",
          formData,
        );

        console.log("Server response:", res.data);
        localStorage.setItem("token", `"${res.data.access_token}"`);
        handleNavigate();
      }
    } catch (error) {
      console.error("Error during login:", error.response?.data);
      console.log("Error details:", error.response?.data?.detail);
      alert(error.response?.data?.message || "Login failed. Please try again.");
    }

    try {
      if (role === "coach") {
        // Create form data
        const formData = new URLSearchParams();
        formData.append("grant_type", "password");
        formData.append("username", phoneOrMail);
        formData.append("password", password);

        const res = await axios.post(
          "http://iam.localhost/api/v1/coach/login",
          formData,
        );

        console.log("Server response:", res.data);
        localStorage.setItem("token", `"${res.data.access_token}"`);
        handleNavigate();
      }
    } catch (error) {
      console.error("Error during login:", error.response?.data);
      console.log("Error details:", error.response?.data?.detail);
      alert(error.response?.data?.message || "Login failed. Please try again.");
    }
    try {
      if (role === "admin") {
        // Create form data
        const formData = new URLSearchParams();
        formData.append("grant_type", "password");
        formData.append("username", phoneOrMail);
        formData.append("password", password);

        const res = await axios.post(
          "http://iam.localhost/api/v1/admin/login",
          formData,
        );

        console.log("Server response:", res.data);
        localStorage.setItem("token", `"${res.data.access_token}"`);
        handleNavigate();
      }
    } catch (error) {
      console.error("Error during login:", error.response?.data);
      console.log("Error details:", error.response?.data?.detail);
      alert(error.response?.data?.message || "Login failed. Please try again.");
    }
  }

  const handleNavigate = (e) => {
    if (role == "user") {
      navigate("/user_panel");
    } else if (role == "coach") {
      navigate("/coach_panel");
    } else if (role == "admin") {
      navigate("/admin_panel");
    }
  };

  const handleMail = (e) => {
    if (!/^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com)$/.test(phoneOrMail)) {
      setMailError(true);
      console.log(setPhoneOrMail);
    } else {
      setMailError(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="top-0 max-sm:w-[75%] max-lg:w-[50%] w-[25%] h-[400px] md:h-[px] border border-white rounded-[10px] bg-coal flex flex-col justify-center align-items-center text-center text-[20px]"
    >
      <p
        className={`text-superRed text-[15px] ${
          showError ? "block" : "hidden"
        }`}
      >
        لطفا فیلدهای الزامی را پر کنید
      </p>
      <div className="my-3 w-[90%] mx-auto flex flex-col justify-start text-right">
        <label className="text-[15px] mb-2" htmlFor="email_input_box">
          شماره تماس یا آدرس ایمیل
        </label>
        <p
          className={`text-[12px] text-superRed ${
            mailError ? "block" : "hidden"
          }`}
        >
          لطفا آدرس ایمیل یاهو یا جیمیل وارد کند
        </p>
        <input
          type="text"
          value={phoneOrMail}
          name="email"
          id={`${role == "user"? "email_input_box" : "coach_email_input_box"}`}
          onChange={(e) => setPhoneOrMail(e.target.value)}
          className={`email text-center text-[15px] py-2 bg-coal border rounded-[10px] ${
            showError && !phoneOrMail ? "border-superRed" : "border-white"
          }`}
          // pattern="([a-z0-9._%+-]+@(gmail\.com|yahoo\.com))"
          placeholder="آدرس ایمیل یاهو یا جیمیل"
        />
      </div>

      <div className="my-3 w-[90%] mx-auto flex flex-col justify-start text-right">
        <label className="text-[15px] mb-2" htmlFor="password">
          گذرواژه
        </label>
        <input
          type="text"
          value={password}
          id={`${role == "user" ? "password_input_box" : "coach_password_input_box"}`}
          onChange={(e) => setPassword(e.target.value)}
          className={`text-center text-[15px] py-2 bg-coal border rounded-[10px] ${
            showError && !password ? "border-superRed" : "border-white"
          }`}
          placeholder="**********"
        />
      </div>

      <a
        href={`/forgot_password/${role}`}
        className="my-2 text-[15px] hover:text-superRed transition-all duration-300"
      >
        گذرواژه خود را فراموش کرده‌اید؟
      </a>

      <a
        href="/user_signup"
        className="my-2 mb-3 text-[15px] hover:text-superRed transition-all duration-300"
      >
        حساب کاربری ندارید؟
      </a>

      <button
        type="submit"
        id="submit_button"
        className="text-mintCream bg-superRed hover:bg-crimsonRed h-[40px] text-[20px] font-medium max-sm:w-[80%] w-[50%] rounded-[10px] mx-auto transition-all duration-300"
      >
        {/* <a href={`/otp_page/${role}`}>ورود</a> */}
        ورود
      </button>
    </form>
  );
}
