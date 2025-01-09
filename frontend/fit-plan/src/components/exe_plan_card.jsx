import React, { useState } from "react";

export default function Exe_plan_card({ plan }) {
  const [completed, setCompleted] = useState(
    plan.days.map((day) => day.movements.map(() => false))
  );

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
    // <div className="collapse ">
    //   <input type="radio" name="my-accordion-1" />
    //   <div className="collapse-title disabled:hover w-full max-h-[139px] p-0 rounded-[15px] border border-mintCream overflow-hidden flex cursor-pointer transition-all duration-300 hover:bg-superRed">
    //     <img
    //       src={image}
    //       alt={name}
    //       className="w-[25%] h-full object-cover object-top"
    //     />
    //     <div className="w-[75%] h-full flex flex-col gap-2 text-right p-4 transition-all duration-300">
    //       <p className="text-mintCream text-[35px] font-semibold">{name}</p>
    //       <p className="text-mintCream text-[20px]">{description}</p>
    //     </div>
    //   </div>
    //   <div className="collapse-content bg-coal rounded-[10px] flex flex-col gap-10 text-mintCream text-center px-4 py-5">

    //   </div>
    // </div>
    <div className="collapse max-h-[500px] overflow-y-auto scrollbar-thin scrollbar-thumb-superRed scrollbar-track-coal">
      <input type="radio" name="my-accordion-1" />
      <div className="collapse-title disabled:hover w-full max-h-[139px] p-0 rounded-[15px] border border-mintCream overflow-hidden flex cursor-pointer transition-all duration-300 hover:bg-superRed">
        <img
          src={plan.image}
          alt={plan.title}
          className="w-[25%] h-full object-cover object-top"
        />
        <div className="w-[75%] h-full flex flex-col gap-2 text-right p-4 transition-all duration-300">
          <p className="text-mintCream text-[35px] font-semibold">{plan.title}</p>
          <p className="text-mintCream text-[20px]">{plan.description}</p>
        </div>
      </div>
      <div className="collapse-content bg-coal rounded-[10px] flex flex-col gap-10 text-mintCream text-center px-4">
        <div className="rounded-lg shadow-md p-4 mb-4">
          {/* <h2 className="text-xl font-bold mb-4">{plan.title}</h2> */}
          <div className="space-y-4 bg-black">
            {plan.days.map((day, dayIndex) => (
              <div
                key={dayIndex}
                className="collapse collapse-arrow border border-gray-300 rounded-lg"
              >
                <input type="checkbox" />
                <div className="collapse-title text-[20px] font-semibold">
                  {day.name}
                </div>
                <div className="collapse-content">
                  <div className="grid max-md:grid-cols-1 grid-cols-2  gap-4 mt-4">
                    {day.movements.map((movement, movementIndex) => (
                      <div
                        key={movementIndex}
                        className="flex gap-2 items-center bg-coal p-4 rounded-[15px] shadow"
                      >
                        <input
                          type="checkbox"
                          className="checkbox checkbox-primary mr-3"
                          checked={completed[dayIndex][movementIndex]}
                          onChange={() => handleToggle(dayIndex, movementIndex)}
                        />
                        <div className="flex justify-between w-full">
                          <p className="text-lg">{movement.name}</p>
                          <p className="text-sm text-mintCream">
                            {movement.repeats}
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
