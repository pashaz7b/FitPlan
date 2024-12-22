import React from "react";

export default function Plan_card({ name, image, description, onClick }) {
  return (
    <div
      className="group w-full max-h-[139px] bg-black rounded-[15px] border border-mintCream overflow-hidden flex cursor-pointer transform hover:bg-coal transition-all duration-300"
      onClick={onClick}
    >
      <img src={image} alt={name} className="w-[10%] h-full object-cover" />
      <div className="w-[90%] h-full flex flex-col gap-2 text-right p-4 bg-black group-hover:bg-coal transition-all duration-300">
        <p className="text-mintCream text-[35px] font-semibold">{name}</p>
        <p className="text-mintCream text-[20px] ">{description}</p>
      </div>
    </div>
  );
}
