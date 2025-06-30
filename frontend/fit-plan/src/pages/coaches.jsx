import React, { useEffect, useState } from "react";
import Footer_comp from "../components/footer_comp";
import { useNavigate } from "react-router-dom";
import fit_logo from "/Images/Fit-Logo-Resized.png";
import Testing_header from "../components/testing_header";
import axios from "axios";

export default function Coaches() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [coaches, setCoaches] = useState([]);
  const [selectedCoach, setSelectedCoach] = useState(null); // For selected coach details

  let value = ""
  if(localStorage.getItem("token")){
    value = localStorage.getItem("token");
    
  }

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  // async function selectCoach(workoutPlanId) {
  //   const token = localStorage.getItem("token"); // Retrieve token from localStorage
  //   console.log(token);
    
  
  //   if (token) {
  //     try {
  //       const res = await axios.post(
  //         "http://fitplan.localhost/api/v1/user/set_user_workout_coach",
  //         {
  //           work_out_plan_id: workoutPlanId, // Payload for the API
  //         },
  //         {
  //           headers: {
  //             Authorization: `Bearer ${localStorage.getItem("token")}`, // Ensure token is parsed correctly
  //         },
  //         }
  //       );
  
  //       console.log("Coach selected successfully:", res.data);
  //     } catch (error) {
  //       console.error("Error selecting coach:", error);
  //     }
  //   } else {
  //     console.error("No token found. User might not be authenticated.");
  //     // Optionally redirect to login
  //     window.location.href = "/login";
  //   }
  // }

  async function selectCoach(selectedByUser) {
    const token = JSON.parse(localStorage.getItem("token")); // Retrieve token from localStorage
    console.log(selectedByUser.coach_name);
    console.log(selectedByUser.work_out_plan_id);

    
    if (token) {
      try {
        // Make the POST request to set the coach
        const res = await axios.post(
          "http://fitplan.localhost/api/v1/user/set_user_workout_coach",
          {
            work_out_plan_id: selectedByUser.work_out_plan_id, 
          },
          {
            headers: {
              Authorization: `Bearer ${token}`, 
            },
          }
        );
        
  
        console.log("Coach selected successfully:", res.data);
      } catch (error) {
        console.error("Error selecting coach:", error.response?.data);
      }
    } else {
      console.error("No token found. User might not be authenticated.");
      window.location.href = "/login"; // Redirect to login if token is missing
    }
  }
  

  async function loadCoaches() {
    try {
      const response = await axios.get(
        "http://fitplan.localhost/api/v1/user/get_user_all_coach_free"
      );
      const coachData = response.data;

      const updatedCoaches = await Promise.all(
        coachData.map(async (coach) => {
          try {
            const emailEncoded = encodeURIComponent(coach.coach_email);
            const imageResponse = await axios.get(
              `http://media.localhost/api/v1/users/media/get_all_coach_profile/${emailEncoded}`,
              { responseType: "blob" }
            );
            const imageURL = URL.createObjectURL(imageResponse.data);

            return {
              ...coach,
              image: imageURL,
            };
          } catch (imageError) {
            console.error(
              `Error fetching image for coach ${coach.coach_email}:`,
              imageError
            );
            return {
              ...coach,
              image: null,
            };
          }
        })
      );

      setCoaches(updatedCoaches);
    } catch (error) {
      console.error("Error loading coaches:", error);
    }
  }

  useEffect(() => {
    loadCoaches();
  }, []);

  return (
    <>
      <div className="relative font-iranyekan">
      <Testing_header />
        

        {/* All Coaches Section */}
        <div
          id="all_coaches"
          className={`z-20 ${
            selectedCoach ? "hidden" : "flex"
          } pt-[200px] bg-mintCream w-full h-full font-iranyekan`}
        >
          <div className="w-[80%] flex justify-start mx-auto">
            <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
              {coaches.map((coach, index) => (
                <div
                  key={index}
                  onClick={() => setSelectedCoach(coach)} // Set selected coach
                  className="rounded-lg p-4 group text-center mx-auto transition-all transform hover:scale-105 duration-300 cursor-pointer"
                >
                  {coach.image ? (
                    <img
                      src={coach.image}
                      alt={coach.coach_name}
                      className="w-60 h-60 mx-auto object-cover object-top rounded-full group-hover:shadow-2xl transition-all duration-300"
                    />
                  ) : (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      height="240"
                      viewBox="0 -960 960 960"
                      width="240"
                      fill="#000"
                      className="text-center mx-auto rounded-full border-coal border-[2px]"
                    >
                      <path d="M480-492.31q-57.75 0-98.87-41.12Q340-574.56 340-632.31q0-57.75 41.13-98.87 41.12-41.13 98.87-41.13 57.75 0 98.87 41.13Q620-690.06 620-632.31q0 57.75-41.13 98.88-41.12 41.12-98.87 41.12ZM180-248.46v-28.16q0-29.38 15.96-54.42 15.96-25.04 42.66-38.5 59.3-29.07 119.65-43.61 60.35-14.54 121.73-14.54t121.73 14.54q60.35 14.54 119.65 43.61 26.7 13.46 42.66 38.5Q780-306 780-276.62v28.16q0 25.3-17.73 43.04-17.73 17.73-43.04 17.73H240.77q-25.31 0-43.04-17.73Q180-223.16 180-248.46Zm60 .77h480v-28.93q0-12.15-7.04-22.5-7.04-10.34-19.11-16.88-51.7-25.46-105.42-38.58Q534.7-367.69 480-367.69q-54.7 0-108.43 13.11-53.72 13.12-105.42 38.58-12.07 6.54-19.11 16.88-7.04 10.35-7.04 22.5v28.93Zm240-304.62q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 384.62Z" />
                    </svg>
                  )}
                  <div className="mt-4">
                    <h3 className="text-[40px] font-semibold text-black">
                      {coach.coach_name}
                    </h3>
                    <p className="text-coal mt-2">{coach.coach_biography}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Coach Detail Section */}
        <div
          id="coach_detail"
          className={`z-20 ${
            selectedCoach ? "flex" : "hidden"
          } flex-col pt-[200px] bg-mintCream w-full h-full font-iranyekan`}
        >
          {selectedCoach && (
            <div className="mx-auto text-center mb-[110px]">
              <div className="max-md:flex-col max-md:justify-start max-md:gap-3 max-md:text-center max-md:overflow-y-auto border-coal border-[2px] mb-[22px] rounded-[10px] h-[618px] w-[70%] mx-auto overflow-hidden flex justify-start gap-5 text-coal">
                <div className="max-md:text-center max-md:justify-center max-md:h-full max-md:w-full max-md:mx-auto h-full w-[25%] overflow-hidden">
                  <img
                    src={selectedCoach.image}
                    alt="user_image"
                    className="max-md:text-center max-md:justify-center max-md:w-full max-md:object-cover object-cover object-center h-full scale-[100%]"
                  />
                </div>
                <div className="max-md:w-[95%] max-md:gap-4 overflow-y-auto scrollbar-none max-md:mx-auto w-[70%] py-5 px-2 flex flex-col gap-11">
                  <h1 className="text-[45px] font-medium text-coal">
                    {selectedCoach.coach_name}
                  </h1>
                  <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">نام کاربری:</p>
                      <p className="text-[20px] font-light text-coal">
                        {selectedCoach.coach_user_name}
                      </p>
                    </div>
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">گذرواژه:</p>
                      <p className="text-[20px] font-light text-coal">
                        ********
                      </p>
                    </div>
                  </div>
                  <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">شماره تماس:</p>
                      <p className="text-[20px] font-light text-coal">
                        {selectedCoach.coach_phone_number}
                      </p>
                    </div>
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">آدرس ایمیل:</p>
                      <p className="text-[15px] font-light text-coal">
                        {selectedCoach.coach_email}
                      </p>
                    </div>
                  </div>
                  <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">تاریخ تولد:</p>
                      <p className="text-[20px] font-light text-coal">
                        {selectedCoach.coach_date_of_birth}
                      </p>
                    </div>
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">جنسیت:</p>
                      <p className="text-[20px] font-light text-coal">
                        {selectedCoach.coach_gender}
                      </p>
                    </div>
                  </div>
                  <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">قد(سانتی متر):</p>
                      <p className="text-[20px] font-light text-coal">
                        {selectedCoach.coach_height}
                      </p>
                    </div>
                    <div className="w-full flex justify-between">
                      <p className="font-medium text-[20px]">وزن(کیلوگرم):</p>
                      <p className="text-[20px] font-light text-coal">
                        {selectedCoach.coach_weight}
                      </p>
                    </div>
                  </div>
                  <div className="max-md:flex-col max-md:gap-4 w-full flex justify-between gap-11">
                    <div className="w-full flex justify-center gap-11">
                      <p className="font-medium text-[20px]">وضعیت:</p>
                      <p className="text-[20px] font-light text-coal">
                        {selectedCoach.status ? "غیر فعال" : "فعال"}
                      </p>
                    </div>
                  </div>
                  <div className="w-full flex max-md:flex-col max-md:justify-center max-md:text-center max-md:mx-auto justify-between gap-2">
                    <p className="font-medium text-[20px] w-[40%] max-md:w-full">
                      درباره مربی:
                    </p>
                    <p className="text-[20px] font-light text-coal">
                      {selectedCoach.coach_biography}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
          <button
            onClick={() => selectCoach(selectedCoach)}
            className="text-superRed font-medium border-superRed border-[2px] w-[350px] mx-auto rounded-[10px] py-2 text-[20px] mb-[100px]"
          >
            انتخاب این مربی به عنوان مربی من
          </button>
        </div>
      </div>
    </>
  );
}
