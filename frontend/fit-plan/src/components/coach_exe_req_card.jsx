import React, { useState } from "react";
import movements from "./movements"; // Import the movements list

export default function CoachExeReqCard({ requestList, onClick }) {
  const [planMovements, setPlanMovements] = useState([]);
  const days = ["روز اول", "روز دوم", "روز سوم", "روز چهارم"];

  const handleCheckboxChange = (movementName) => {
    setPlanMovements((prev) => {
      if (prev.includes(movementName)) {
        // Remove if already selected
        return prev.filter((name) => name !== movementName);
      } else {
        // Add if not selected
        return [...prev, movementName];
      }
    });
  };

  return (
    <div className="collapse max-h-[500px] overflow-y-auto scrollbar-none">
      <input type="radio" name="my-accordion-1" />
      <div className="collapse-title disabled:hover w-full max-h-[139px] p-0 rounded-[15px] border border-mintCream overflow-hidden flex cursor-pointer transition-all duration-300 hover:bg-superRed">
        {requestList.image && requestList.image.trim() ? (
          <img
            src={requestList.image}
            alt={requestList.nameSurname}
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
        <div className="w-[75%] h-full flex flex-col gap-2 text-right p-4 transition-all duration-300">
          <p className="text-mintCream text-[23px] font-normal text-center flex flex-col justify-center md:pt-8">
            شما یک درخواست برنامه تمرینی از "{requestList.nameSurname}" دارید
          </p>
        </div>
      </div>
      <div className="collapse-content max-h-[1200px] bg-coal rounded-[10px] flex flex-col gap-10 text-mintCream text-center px-4 pt-6">
        {days.map((day, index) => (
          <div
            key={index}
            tabIndex={0}
            className="collapse collapse-plus border border-superRed rounded-box mb-4"
          >
            <input type="checkbox" />
            <div className="collapse-title text-[25px] font-medium">{day}</div>
            <div className="collapse-content">
              <div className="grid max-sm:grid-cols-1 grid-cols-2 w-[80%] text-center mx-auto gap-10 mt-5">
                {movements.map((movement) => (
                  <label
                    key={`${day}-${movement.name}`}
                    className="flex items-center gap-2 border rounded-[15px] px-4 py-2 bg-coal"
                  >
                    <input
                      type="checkbox"
                      value={movement.name}
                      checked={planMovements.includes(movement.name)}
                      onChange={() => handleCheckboxChange(movement.name)}
                      className="form-checkbox"
                    />
                    <div className="flex justify-between w-full">
                      <p className="text-lg">{movement.name}</p>
                      <p className="text-sm text-mintCream">{movement.set}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>
          </div>
        ))}
        <button className="bg-irishGreen w-[20%] max-sm:w-[80%] text-center text-[20px] font-medium py-1 rounded-[10px] mx-auto hover:bg-[#01651b] transition-all duration-200">
          ارسال برنامه
        </button>
      </div>
    </div>
  );
}
