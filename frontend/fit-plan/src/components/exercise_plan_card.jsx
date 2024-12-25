import React from "react";

export default function Plan_card({ name, image, description, onClick, breakfast, lunch, dinner }) {
  return (
    <div className="collapse ">
      <input type="radio" name="my-accordion-1" />
      <div 
        className="collapse-title disabled:hover w-full max-h-[139px] p-0 rounded-[15px] border border-mintCream overflow-hidden flex cursor-pointer transition-all duration-300 hover:bg-superRed"
      >
        <img 
          src={image} 
          alt={name} 
          className="w-[25%] h-full object-cover object-top" 
        />
        <div 
          className="w-[75%] h-full flex flex-col gap-2 text-right p-4 transition-all duration-300"
        >
          <p className="text-mintCream text-[35px] font-semibold">{name}</p>
          <p className="text-mintCream text-[20px]">{description}</p>
        </div>
      </div>
      <div className="collapse-content bg-coal rounded-[10px] flex flex-col gap-10 text-mintCream text-center px-4 py-5">
        <div id="breakfast" className="flex flex-col gap-2 text-right">
          <h1 className="font-bold text-[30px]">صبحانه</h1>
          <p className="text-[17px]">{breakfast}</p>
        </div>
        <div id="lunch" className="flex flex-col gap-2 text-right">
          <h1 className="font-bold text-[30px]">ناهار</h1>
          <p className="text-[17px]">{lunch}</p>
        </div>
        <div id="dinner" className="flex flex-col gap-2 text-right">
          <h1 className="font-bold text-[30px]">شام</h1>
          <p className="text-[17px]">{dinner}</p>
        </div>
        <p className="text-[18px] mt-8">این برنامه تا <span className="text-superRed"> 2ماه دیگر </span>اعتبار دارد</p>
      </div>
    </div>
  );
}
