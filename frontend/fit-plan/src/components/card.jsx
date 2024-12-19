import React from "react";

function Card({ name, image, onClick }) {
  return (
    <div
      className="w-64 h-80 bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer transform hover:scale-105 transition duration-300"
      onClick={onClick}
    >
      <img src={image} alt={name} className="w-full h-2/3 object-cover" />
      <div className="h-1/3 flex items-center justify-center bg-gray-800">
        <p className="text-mintCream text-lg font-semibold">{name}</p>
      </div>
    </div>
  );
}

export default Card;
