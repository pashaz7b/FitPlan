import React, { useEffect, useState } from "react";

export default function Exe_plan_card({ plan }) {
  const [groupedDays, setGroupedDays] = useState({});
  const [completed, setCompleted] = useState([]);

  // Group exercises by day
  useEffect(() => {
    if (plan?.exercises) {
      const grouped = plan.exercises.reduce((acc, exercise) => {
        if (!acc[exercise.day]) {
          acc[exercise.day] = [];
        }
        acc[exercise.day].push(exercise);
        return acc;
      }, {});
      setGroupedDays(grouped);
    }
  }, [plan]);

  // Initialize the completed state dynamically
  useEffect(() => {
    if (Object.keys(groupedDays).length > 0) {
      const initialCompleted = Object.keys(groupedDays).map((day) =>
        groupedDays[day].map(() => false)
      );
      setCompleted(initialCompleted);
    }
  }, [groupedDays]);

  // Handle checkbox toggle
  const handleToggle = (dayIndex, movementIndex) => {
    const updatedCompleted = completed.map((day, dIndex) =>
      dIndex === dayIndex
        ? day.map((checked, mIndex) =>
            mIndex === movementIndex ? !checked : checked
          )
        : day
    );
    setCompleted(updatedCompleted);
  };

  return (
    <div className="collapse max-h-[500px] overflow-y-auto scrollbar-thin scrollbar-thumb-superRed scrollbar-track-coal">
      <input type="radio" name="my-accordion-1" />
      <div className="collapse-title disabled:hover w-full max-h-[139px] p-0 rounded-[15px] border border-mintCream overflow-hidden flex cursor-pointer transition-all duration-300 hover:bg-superRed">
        {plan.image && plan.image.trim() ? (
          <img
            src={plan.image}
            alt={plan.coach_name}
            className="w-full max-h-[220px] object-cover object-top"
          />
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="150px"
            viewBox="0 -960 960 960"
            width="150px"
            fill="#e8eaed"
          >
            <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
          </svg>
        )}
        <div className="w-[75%] h-full flex flex-col gap-2 text-right p-4 transition-all duration-300">
          <p className="text-mintCream text-[35px] font-semibold">{plan?.coach_name}</p>
          <p className="text-mintCream text-[20px]">شما یک برنامه تمرینی از "{plan.coach_name}" دارید</p>
        </div>
      </div>
      <div className="collapse-content bg-coal rounded-[10px] flex flex-col gap-10 text-mintCream text-center px-4">
        <div className="rounded-lg shadow-md p-4 mb-4">
          <div className="space-y-4 bg-black">
            {Object.keys(groupedDays).map((day, dayIndex) => (
              <div
                key={dayIndex}
                className="collapse collapse-arrow border border-gray-300 rounded-lg"
              >
                <input type="checkbox" />
                <div className="collapse-title text-[20px] font-semibold">
                  {day}
                </div>
                <div className="collapse-content">
                  <div className="grid max-md:grid-cols-1 grid-cols-2 gap-4 mt-4">
                    {groupedDays[day].map((movement, movementIndex) => (
                      <div
                        key={movement.id}
                        className="flex gap-2 items-center bg-coal p-4 rounded-[15px] shadow"
                      >
                        <input
                          type="checkbox"
                          className="checkbox checkbox-primary mr-3"
                          checked={completed[dayIndex]?.[movementIndex] || false}
                          onChange={() => handleToggle(dayIndex, movementIndex)}
                        />
                        <div className="flex justify-between w-full">
                          <p className="text-lg">{movement.name}</p>
                          <p className="text-sm text-mintCream">
                            {movement.set}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
