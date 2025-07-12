import React, { useState } from "react";
import fit_logo from "/Images/Fit-Logo-Resized.png";

const Testing_header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <div className="relative font-iranyekan">
      {/* Top Navbar */}
      <div className="flex items-center justify-between px-4 py-3 bg-black text-white md:hidden">
        <a href="/" className="h-[30px]">
          <img
            src={fit_logo}
            alt="fit_logo"
            className="h-full object-contain"
          />
        </a>
        <button onClick={toggleMenu} className="focus:outline-none text-white">
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
        </button>
      </div>

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 transform ${
          isMenuOpen ? "translate-x-0" : "-translate-x-full"
        } transition-transform duration-300 bg-coal text-white w-64 z-50`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between px-4 py-3 h-[60px] border-b border-superRed">
            <a href="/" className="h-[50px]">
              <img
                src={fit_logo}
                alt="fot_logo"
                className="object-contain object-center h-full"
              />
            </a>
            <button
              onClick={toggleMenu}
              className="focus:outline-none text-white"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <nav className="mt-4 space-y-2 px-4">
            <a
              href="./about_us"
              className="block py-2 px-3 rounded hover:bg-superRed transition-all duration-300"
              onClick={closeMenu}
            >
              فیت‌پلن
            </a>
            <a
              href="./about_us"
              className="block py-2 px-3 rounded hover:bg-superRed transition-all duration-300"
              onClick={closeMenu}
            >
              باشگاه‌ها
            </a>
            <a
              href="./coaches"
              className="block py-2 px-3 rounded hover:bg-superRed transition-all duration-300"
              onClick={closeMenu}
            >
              مربی‌ها
            </a>
            <a
              href="./podcasts"
              className="block py-2 px-3 rounded hover:bg-superRed transition-all duration-300"
              onClick={closeMenu}
            >
              پادکست
            </a>
            <a
              href="./articles"
              className="block py-2 px-3 rounded hover:bg-superRed transition-all duration-300"
              onClick={closeMenu}
            >
              مقالات
            </a>
            <a
              href="./user_login"
              className="block py-2 px-3 rounded hover:bg-superRed transition-all duration-300"
              onClick={closeMenu}
            >
              ورود
            </a>
          </nav>
        </div>
      </div>

      {/* Overlay */}
      {isMenuOpen && (
        <div
          className="fixed inset-0 bg-black opacity-50 z-40"
          onClick={closeMenu}
        ></div>
      )}

      {/* Desktop Navbar */}
      <div className="bg-mintCream">
        <div className="hidden md:flex items-center w-[80%] h-[80px] rounded-b-[30px] mx-auto justify-between px-8 py-3 bg-black text-white">
          <a href="/" className="h-[60px]">
            <img
              src={fit_logo}
              alt="fit_logo"
              className="h-full object-contain"
            />
          </a>
          <nav className="flex justify-start max-lg:gap-5 gap-10 font-medium">
            <a
              href="./about_us"
              className="hover:text-superRed transition-all duration-300"
            >
              فیت‌پلن
            </a>
            <a
              href="./gyms"
              className="hover:text-superRed transition-all duration-300"
            >
              باشگاه‌ها
            </a>
            <a
              href="./coaches"
              className="hover:text-superRed transition-all duration-300"
            >
              مربی‌ها
            </a>
            <a
              href="./podcasts"
              className="hover:text-superRed transition-all duration-300"
            >
              پادکست
            </a>
            <a
              href="./articles"
              className="hover:text-superRed transition-all duration-300"
            >
              مقالات
            </a>
            <a
              href="./user_login"
              className="bg-superRed px-4 py-1 rounded-[10px] hover:bg-crimsonRed transition-all duration-300"
            >
              ورود
            </a>
          </nav>
        </div>
      </div>
    </div>
  );
};

export default Testing_header;
