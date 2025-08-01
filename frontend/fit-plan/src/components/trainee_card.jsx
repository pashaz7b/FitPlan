import React from "react";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Trainee_card({
  nameSurname,
  username,
  phoneNumber,
  email,
  birthDate,
  gender,
  height,
  weight,
  image,
  onClick,
  userId, // Added a new prop to hold the trainee's ID
}) {
  const navigate = useNavigate();

  // Updated function to use the userId for navigation
  const navToChat = () => {
    navigate(`chat/${userId}`);
  };

  return (
    <div className="collapse max-h-[500px] overflow-y-auto scrollbar-thin scrollbar-thumb-superRed scrollbar-track-coal">
      <input type="radio" name="my-accordion-1" />
      <div className="collapse-title disabled:hover w-full max-h-[139px] p-0 rounded-[15px] border border-mintCream overflow-hidden flex cursor-pointer transition-all duration-300 hover:bg-superRed">
        {image && image.trim() ? (
          <img
            src={image}
            alt={nameSurname}
            className="w-[25%] h-full object-cover object-top"
          />
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="full"
            viewBox="0 -960 960 960"
            width="25%"
            fill="#e8eaed"
          >
            <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
          </svg>
        )}
        <div className="flex w-full">
          <div className="w-[75%] h-full flex flex-col gap-2 text-right p-4 transition-all duration-300">
            <p className="text-mintCream text-[35px] font-semibold">
              {nameSurname}
            </p>
            <p className="text-mintCream font-light text-[20px]">
              نام کاربری: {username}
            </p>
          </div>
        </div>
      </div>
      <div className="collapse-content max-h-[1200px] bg-coal rounded-[10px] flex flex-col gap-10 text-mintCream text-center px-4 pt-6">
        <button
          onClick={navToChat} // Updated to call the new function
          className="max-md:py-3 max-md:my-3 text-superRed border border-superRed rounded-[15px] px-5 py-0 max-h-[40%] font-medium text-[20px] hover:bg-superRed hover:text-black translate-all duration-300"
        >
          شروع گفتگو
        </button>
        <div className="max-md:w-[95%] max-md:gap-4 max-md:text-center max-md:overflow-y-auto max-md:scrollbar-thin max-md:scrollbar-thumb-superRed max-md:scrollbar-track-coal max-md:mx-auto w-[70%] py-5 px-2 flex flex-col text-center mx-auto gap-11">
          <h1 className="text-[45px] font-medium">{nameSurname}</h1>
          <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">نام کاربری:</p>
              <p className="text-[20px] font-light">{username}</p>
            </div>
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">گذرواژه:</p>
              <p className="text-[20px] font-light">********</p>
            </div>
          </div>
          <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">شماره تماس:</p>
              <p className="text-[20px] font-light">{phoneNumber}</p>
            </div>
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">آدرس ایمیل:</p>
              <p className="text-[15px] font-light">{email}</p>
            </div>
          </div>
          <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">تاریخ تولد:</p>
              <p className="text-[20px] font-light">{birthDate}</p>
            </div>
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">جنسیت:</p>
              <p className="text-[20px] font-light">{gender}</p>
            </div>
          </div>
          <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">قد(سانتی متر):</p>
              <p className="text-[20px] font-light">{height}</p>
            </div>
            <div className="w-full flex justify-between">
              <p className="font-medium text-[20px]">وزن(کیلوگرم):</p>
              <p className="text-[20px] font-light">{weight}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
