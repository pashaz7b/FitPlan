import { useNavigate } from "react-router-dom";
import Testing_header from "../components/testing_header";
import { useEffect, useState } from "react";
import Footer_comp from "../components/footer_comp";

export default function Gyms() {
  const [selectedGym, setSelectedGym] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    const handlePopState = () => {
      setSelectedGym(""); // Reset selectedGym when back button is pressed
    };

    // Listen for the popstate event
    window.addEventListener("popstate", handlePopState);

    return () => {
      window.removeEventListener("popstate", handlePopState);
      navigate("./");
    };
  }, []);

  const gyms = [
    {
      id: 1,
      gymName: "باشگاه نقش رستم",
      gymImage: ["/Images/gym1.jpg", "/Images/gym2.jpg", "/Images/gym3.jpg", "/Images/gym4.jpg"],
      gymAddress: "کمربندی امیرکلا، نیما 2",
    },
    {
      id: 2,
      gymName: "باشگاه طهماسبی",
      gymImage: ["/Images/gym2.jpg", "/Images/gym3.jpg", "/Images/gym1.jpg", "/Images/gym4.jpg"],
      gymAddress: "خیابان شریعتی، معلم 28",
    },
    {
      id: 3,
      gymName: "باشگاه مربی من",
      gymImage: ["/Images/gym3.jpg", "/Images/gym1.jpg", "/Images/gym2.jpg", "/Images/gym4.jpg"],
      gymAddress: "کمربندی غربی، توحید 46",
    },
    {
      id: 4,
      gymName: "باشگاه نقش رستم",
      gymImage: ["/Images/gym1.jpg", "/Images/gym2.jpg", "/Images/gym3.jpg", "/Images/gym4.jpg"],
      gymAddress: "کمربندی امیرکلا، نیما 2",
    },
    {
      id: 5,
      gymName: "باشگاه طهماسبی",
      gymImage: ["/Images/gym2.jpg", "/Images/gym3.jpg", "/Images/gym1.jpg", "/Images/gym4.jpg"],
      gymAddress: "خیابان شریعتی، معلم 28",
    },
    {
      id: 6,
      gymName: "باشگاه مربی من",
      gymImage: ["/Images/gym3.jpg", "/Images/gym1.jpg", "/Images/gym2.jpg", "/Images/gym4.jpg"],
      gymAddress: "کمربندی غربی، توحید 46",
    },
  ];


  const open_gym_detail = (gymId) => {
    navigate(`/gym_details/${gymId}`);
  };
  

  return (
    <>
      <Testing_header />
      <div className="py-10 bg-mintCream w-full h-full">
        <div id="all_gyms" className={`${selectedGym ? "hidden" : "flex"}`}>
          <div className="w-[80%] flex-col justify-start mx-auto font-iranyekan">
            <p className="font-bold text-[40px] text-coal mb-5">باشگاه‌ها</p>
            <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 mb-10">
              {gyms.map((gym, index) => (
                <div key={index} onClick={() => open_gym_detail(gym.id)}>
                  <div class="max-w-sm rounded-[20px] overflow-hidden shadow-lg hover:scale-105 hover:shadow-2xl transition-all transform duration-300 cursor-pointer">
                    {gym.gymImage ? (
                      <img
                        src={gym.gymImage[0]}
                        alt={gym.gymName}
                        className="w-full h-60 mx-auto object-cover object-top group-hover:shadow-2xl transition-all duration-300"
                      />
                    ) : (
                      <svg
                        width="100"
                        height="100"
                        viewBox="0 0 27 26"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="text-center mx-auto"
                      >
                        <g clip-path="url(#clip0_223_1020)">
                          <path
                            d="M24.5347 9.40209L23.0966 7.96395L23.9439 7.08221C24.0323 6.99384 24.0765 6.89445 24.0765 6.78405C24.0765 6.67364 24.0323 6.57437 23.9439 6.48623L20.0138 2.55607C19.9256 2.4677 19.8264 2.42351 19.716 2.42351C19.6055 2.42351 19.5062 2.4677 19.4178 2.55607L18.536 3.40339L17.0635 1.93082L17.9638 0.996054C18.43 0.529874 19.0047 0.302523 19.6881 0.314C20.3714 0.325476 20.9461 0.564304 21.4123 1.03048L25.4695 5.08769C25.9357 5.55387 26.1688 6.12288 26.1688 6.79472C26.1688 7.46656 25.9357 8.03557 25.4695 8.50175L24.5347 9.40209ZM9.00175 24.9695C8.53557 25.4357 7.96656 25.6688 7.29472 25.6688C6.62288 25.6688 6.05387 25.4357 5.58769 24.9695L1.58351 20.965C1.10837 20.4901 0.870809 19.9035 0.870809 19.2053C0.870809 18.507 1.10837 17.9204 1.58351 17.4452L2.43082 16.5979L3.90338 18.0705L3.03472 18.9178C2.94635 19.0062 2.90217 19.1055 2.90217 19.216C2.90217 19.3264 2.94635 19.4256 3.03472 19.5138L6.98623 23.4653C7.07437 23.5536 7.17364 23.5978 7.28405 23.5978C7.39445 23.5978 7.49384 23.5536 7.58221 23.4653L8.42952 22.5966L9.90209 24.0692L9.00175 24.9695ZM22.5378 14.5005L24.3017 12.7366C24.39 12.6482 24.4342 12.5467 24.4342 12.4319C24.4342 12.3171 24.39 12.2156 24.3017 12.1272L14.3728 2.19834C14.2844 2.10997 14.1829 2.06579 14.0681 2.06579C13.9533 2.06579 13.8518 2.10997 13.7634 2.19834L11.9995 3.96218C11.9114 4.05055 11.8673 4.14982 11.8673 4.26C11.8673 4.3704 11.9114 4.46979 11.9995 4.55816L21.9418 14.5005C22.0302 14.5886 22.1296 14.6327 22.24 14.6327C22.3502 14.6327 22.4494 14.5886 22.5378 14.5005ZM13.2022 23.8361L14.966 22.0509C15.0542 21.9628 15.0982 21.8635 15.0982 21.7531C15.0982 21.6427 15.0542 21.5434 14.966 21.4553L5.04473 11.534C4.95659 11.4458 4.85732 11.4018 4.74691 11.4018C4.63651 11.4018 4.53724 11.4458 4.4491 11.534L2.66391 13.2978C2.57554 13.3862 2.53136 13.4878 2.53136 13.6025C2.53136 13.7173 2.57554 13.8189 2.66391 13.9072L12.5928 23.8361C12.6811 23.9245 12.7827 23.9686 12.8975 23.9686C13.0122 23.9686 13.1138 23.9245 13.2022 23.8361ZM12.6114 16.1768L16.6638 12.1458L14.3542 9.83625L10.3232 13.8886L12.6114 16.1768ZM14.6613 25.2873C14.1864 25.7624 13.5985 26 12.8975 26C12.1965 26 11.6085 25.7624 11.1336 25.2873L1.2127 15.3664C0.737566 14.8915 0.5 14.3035 0.5 13.6025C0.5 12.9015 0.737566 12.3136 1.2127 11.8387L2.97654 10.0614C3.45144 9.58652 4.03801 9.34907 4.73624 9.34907C5.43471 9.34907 6.02139 9.58652 6.49629 10.0614L8.8506 12.4161L12.903 8.36403L10.5483 6.03072C10.0734 5.55582 9.83598 4.96558 9.83598 4.26C9.83598 3.55465 10.0734 2.96452 10.5483 2.48962L12.3256 0.712697C12.8005 0.237566 13.3871 0 14.0853 0C14.7835 0 15.3701 0.237566 15.845 0.712697L25.7873 10.655C26.2624 11.1299 26.5 11.7165 26.5 12.4147C26.5 13.1129 26.2624 13.6995 25.7873 14.1744L24.0104 15.9517C23.5355 16.4266 22.9454 16.664 22.24 16.664C21.5344 16.664 20.9442 16.4266 20.4693 15.9517L18.136 13.597L14.0839 17.6494L16.4386 20.0037C16.9135 20.4786 17.1509 21.0653 17.1509 21.7638C17.1509 22.462 16.9135 23.0486 16.4386 23.5235L14.6613 25.2873Z"
                            fill="black"
                          />
                        </g>
                        <defs>
                          <clipPath id="clip0_223_1020">
                            <rect
                              width="26"
                              height="26"
                              fill="white"
                              transform="translate(0.5)"
                            />
                          </clipPath>
                        </defs>
                      </svg>
                    )}
                    <div class="px-6 py-4">
                      <div class="font-bold text-xl mb-2 text-coal text-center">
                        {gym.gymName}
                      </div>
                      <p class="text-gray-700 text-base text-center">
                        {gym.gymAddress}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        {/* <div id="gym_details" className={`${selectedGym ? "flex" : "hidden"}`}>
          <div className="w-[80%] flex-col justify-start mx-auto font-iranyekan">
            <div className="flex w-full justify-between">
              <div className="w-1/2 aspect-video overflow-hidden rounded-[20px] h-[450px] max-md:text-center max-md:justify-center max-md:w-full max-md:mx-auto">
              {selectedGym ? (
                    <img
                      src={selectedGym.gymImage}
                      alt={selectedGym.gymName}
                      className="object-contain object-center w-full h-full scale-[110%] max-md:text-center max-md:justify-center max-md:w-full max-md:mx-auto max-md:scale-[120%] max-md:object-cover"
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
              </div>
            </div>
          </div>
        </div> */}
      </div>
      {/* Footer section */}
      <Footer_comp/>
    </>
  );
}
