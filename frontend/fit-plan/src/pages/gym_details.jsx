import { useEffect, useState } from "react";
import Footer_comp from "../components/footer_comp";
import Testing_header from "../components/testing_header";
import StarRating from "../components/starRating";
import { useParams, useSearchParams } from "react-router-dom";

export default function GymDetails() {
  const { gymId } = useParams;
  //   const [gymDetails, setGymDetails] = useState(null);
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState(null);
  const [isFormVisible, setIsFormVisible] = useState(false);
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);

  const toggleComment = () => {
    setIsFormVisible(!isFormVisible);
  };

  const handleRating = (newRating) => {
    setRating(newRating);
  };

  const handleSubmit = () => {
    if (comment.trim() === "") {
      alert("لطفا نظر و امتیاز خود را وارد کنید!");
      return;
    }

    const newComment = {
      writer: "کاربر ناشناس",
      commentDate: new Date().toLocaleDateString("fa-IR"),
      rate: rating,
      commentText: comment,
    };

    setComments([newComment, ...comments]);
    setComment("");
    setRating(0);
    setIsFormVisible(false);
  };

  //   useEffect(() => {
  //     const fetchGymDetails = async () => {
  //       setLoading(true);
  //       setError(null);
  //       try {
  //         // Simulate API call to your backend
  //         // Replace with your actual backend endpoint
  //         const response = await fetch(`YOUR_BACKEND_API_URL/gyms/${id}`);
  //         if (!response.ok) {
  //           throw new Error(`HTTP error! status: ${response.status}`);
  //         }
  //         const data = await response.json();
  //         setGymDetails(data);
  //       } catch (err) {
  //         setError(err.message);
  //       } finally {
  //         setLoading(false);
  //       }
  //     };

  //     if (id) {
  //       fetchGymDetails();
  //     }
  //   }, [id]); // Re-fetch if the ID changes (though usually it won't on this page)

  //   if (loading) {
  //     return (
  //       <div className="flex justify-center items-center h-screen">
  //         <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
  //         <p className="ml-4 text-xl text-gray-700">لطفا شکیبا باشید...</p>
  //       </div>
  //     );
  //   }

  //   if (error) {
  //     return (
  //       <div className="flex flex-col justify-center items-center h-screen text-red-600">
  //         <p className="text-2xl mb-4">Error: {error}</p>
  //         <button
  //           onClick={() => navigate("/")}
  //           className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
  //         >
  //           Go Back to Gym List
  //         </button>
  //       </div>
  //     );
  //   }

  const gymDetails = [
    {
      id: 1,
      name: "باشگاه طهماسبی",
      image: [
        "/Images/gym2.jpg",
        "/Images/gym3.jpg",
        "/Images/gym1.jpg",
        "/Images/gym4.jpg",
      ],
      address: "خیابان شریعتی، معلم 28",
      rate: 3.5,
      facilities:
        "تردمیل و وسایل به روز تمرینات هوازی - رختکن مجهز به سیستم ایمنی اثر انگشت",
      exercise_facility:
        "دستگاه پرس سینه - دستگاه بالا‌سینه - دستگاه پشت پا نشسته",
      coaches: [
        {
          name: "آرش فانی",
          image: "/Images/Coach-Arash-Faani.jpg",
          description: "قهرمان مسابقات بین‌المللی بدنسازی سال ۲۰۱۸ در اسپانیا",
          adjustmentClass: "object-top",
        },
        {
          name: "آرش فانی",
          image: "/Images/Coach-Arash-Faani.jpg",
          description: "قهرمان مسابقات بین‌المللی بدنسازی سال ۲۰۱۸ در اسپانیا",
        },
      ],
      services: [
        {
          numOfSessions: 1,
          expirationDays: 30,
          vip: false,
          cost: "700000",
        },
        {
          numOfSessions: 16,
          expirationDays: null,
          vip: true,
          cost: "1200000",
        },
      ],
      comments: [
        {
          writer: "اشکان درگاهی",
          commentDate: "6 بهمن 1403",
          rate: 4,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "عباس بوعذار",
          commentDate: "3 خرداد 1403",
          rate: 4.5,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "جاسم‌ابن‌عقیل",
          commentDate: "6 بهمن 1403",
          rate: 2,
          commentText: "راضی نبودم.",
        },
        {
          writer: "اشکان درگاهی",
          commentDate: "6 بهمن 1403",
          rate: 4,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "عباس بوعذار",
          commentDate: "3 خرداد 1403",
          rate: 4.5,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "جاسم‌ابن‌عقیل",
          commentDate: "6 بهمن 1403",
          rate: 2,
          commentText: "راضی نبودم.",
        },
        {
          writer: "اشکان درگاهی",
          commentDate: "6 بهمن 1403",
          rate: 4,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "عباس بوعذار",
          commentDate: "3 خرداد 1403",
          rate: 4.5,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "جاسم‌ابن‌عقیل",
          commentDate: "6 بهمن 1403",
          rate: 2,
          commentText: "راضی نبودم.",
        },
        {
          writer: "اشکان درگاهی",
          commentDate: "6 بهمن 1403",
          rate: 4,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "عباس بوعذار",
          commentDate: "3 خرداد 1403",
          rate: 4.5,
          commentText:
            "من با استاد آرش یک ساله کار میکنم و واقعا راضی‌ام. حتما کار کردن باهاشون رو پیشنهاد میکنم.",
        },
        {
          writer: "جاسم‌ابن‌عقیل",
          commentDate: "6 بهمن 1403",
          rate: 2,
          commentText: "راضی نبودم.",
        },
      ],
    },
  ];

  return (
    <>
      <div>
        <Testing_header />
        <div className="bg-mintCream font-iranyekan">
          <div className="w-[80%] flex-col justify-start mx-auto">
            <div className="md:hidden text-center">
              <p className="text-coal font-bold text-[45px] pt-10">
                {gymDetails[0].name}
              </p>
              <div className="flex gap-2">
                <StarRating rating={gymDetails[0]?.rate || 0} />
                <p>{gymDetails[0].rate}</p>
              </div>
              <div className="flex pt-4">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="24px"
                  viewBox="0 -960 960 960"
                  width="24px"
                  fill="#7F7F7F"
                >
                  <path d="M480-480q33 0 56.5-23.5T560-560q0-33-23.5-56.5T480-640q-33 0-56.5 23.5T400-560q0 33 23.5 56.5T480-480Zm0 294q122-112 181-203.5T720-552q0-109-69.5-178.5T480-800q-101 0-170.5 69.5T240-552q0 71 59 162.5T480-186Zm0 106Q319-217 239.5-334.5T160-552q0-150 96.5-239T480-880q127 0 223.5 89T800-552q0 100-79.5 217.5T480-80Zm0-480Z" />
                </svg>
                <p className="text-midtoneGray">{gymDetails[0].address}</p>
              </div>
            </div>
            <div className="flex gap-5 w-full justify-start">
              <div className="w-1/2 pt-10 max-md:w-full">
                {gymDetails[0]?.image && gymDetails[0].image.length > 0 ? (
                  <div className="carousel max-md:w-full rounded-[20px] overflow-hidden relative">
                    {gymDetails[0].image.map((imgSrc, index) => (
                      <div
                        key={index}
                        id={`slide${index + 1}`}
                        className="carousel-item relative w-full h-[450px]"
                      >
                        <img
                          src={imgSrc}
                          alt={`Slide ${index + 1}`}
                          className="w-full h-full object-cover rounded-[20px]"
                        />
                        <div className="absolute left-0 right-0 top-1/2 transform -translate-y-1/2 flex justify-between px-4">
                          <a
                            href={`#slide${
                              index === 0 ? gymDetails[0].image.length : index
                            }`}
                            className="btn btn-circle bg-black/50 text-white p-2 hover:bg-black/70 transition"
                          >
                            ❮
                          </a>
                          <a
                            href={`#slide${
                              (index + 2) % gymDetails[0].image.length || 1
                            }`}
                            className="btn btn-circle bg-black/50 text-white p-2 hover:bg-black/70 transition"
                          >
                            ❯
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
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

                <div className="max-md:flex md:hidden">
                  <div className="pt-10">
                    <p className="text-coal font-black text-[30px]">امکانات</p>
                    <p className="text-tableBrightGray font-regular text-[15px]">
                      {gymDetails[0].facilities}
                    </p>
                    <button className="border border-superRed w-full py-5 font-medium text-superRed rounded-[10px] mt-14 hover:bg-superRed hover:text-mintCream transition-all transform duration-300">
                      ثبت‌نام در این باشگاه
                    </button>
                  </div>
                </div>
              </div>
              <div className="max-md:hidden max-md:flex-col">
                <p className="text-coal font-bold text-[45px] pt-10">
                  {gymDetails[0].name}
                </p>
                <div className="flex gap-2">
                  <StarRating rating={gymDetails[0]?.rate || 0} />
                  <p>{gymDetails[0].rate}</p>
                </div>
                <div className="flex pt-4">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="24px"
                    viewBox="0 -960 960 960"
                    width="24px"
                    fill="#7F7F7F"
                  >
                    <path d="M480-480q33 0 56.5-23.5T560-560q0-33-23.5-56.5T480-640q-33 0-56.5 23.5T400-560q0 33 23.5 56.5T480-480Zm0 294q122-112 181-203.5T720-552q0-109-69.5-178.5T480-800q-101 0-170.5 69.5T240-552q0 71 59 162.5T480-186Zm0 106Q319-217 239.5-334.5T160-552q0-150 96.5-239T480-880q127 0 223.5 89T800-552q0 100-79.5 217.5T480-80Zm0-480Z" />
                  </svg>
                  <p className="text-midtoneGray">{gymDetails[0].address}</p>
                </div>
                <div className="pt-10">
                  <p className="text-coal font-black text-[30px]">امکانات</p>
                  <p className="text-tableBrightGray font-regular text-[15px]">
                    {gymDetails[0].facilities}
                  </p>
                  <button className="border border-superRed w-full py-5 font-medium text-superRed rounded-[10px] mt-14 hover:bg-superRed hover:text-mintCream transition-all transform duration-300">
                    ثبت‌نام در این باشگاه
                  </button>
                </div>
              </div>
            </div>
            <div className="pt-[100px]">
              <h1 className="text-coal font-black text-[30px] mb-5">
                امکانات ورزشی
              </h1>
              <p className="text-tableBrightGray font-regular text-[15px]">
                {gymDetails[0].exercise_facility}
              </p>
            </div>
            <div className="pt-[100px]">
              <h1 className="text-coal font-black text-[30px] mb-5">
                مربی‌های این باشگاه
              </h1>
              <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                {gymDetails[0].coaches.map((coach, index) => (
                  <div
                    key={index}
                    onClick={() => setSelectedCoach(coach)} // Set selected coach
                    className="rounded-lg p-4 group text-center mx-auto transition-all transform hover:scale-105 duration-300 cursor-pointer"
                  >
                    {coach.image ? (
                      <img
                        src={coach.image}
                        alt={coach.name}
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
                        {coach.name}
                      </h3>
                      <p className="text-coal mt-2">{coach.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="pt-[100px]">
              <h1 className="text-coal font-black text-[30px] mb-5">
                خدمات قابل ارائه
              </h1>
              <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 ">
                {gymDetails[0].services.map((services, index) => (
                  <div className="relative bg-cardOrnge flex-col text-center justify-center shadow-xl w-60 h-auto p-7 rounded-[10px] hover:scale-105 hover:shadow-2xl transition-all duration-300">
                    {services.vip && (
                      <span className="absolute top-3 left-3 bg-superRed text-mintCream font-semibold text-[20px] px-2 py-1 rounded-md">
                        VIP
                      </span>
                    )}
                    <h1 className="text-coal font-semibold text-[80px]">
                      {services.numOfSessions}
                    </h1>
                    <p className="text-coal text-[50px]">جلسه</p>
                    <p className="text-coal text-[30px]">
                      {services.cost} تومان
                    </p>
                    <button className="bg-mintCream text-superRed border border-superRed text-[30px] px-5 rounded-[10px] hover:bg-superRed hover:text-mintCream transition-all transform duration-300">
                      پرداخت
                    </button>
                  </div>
                ))}
              </div>
            </div>
            <div className="pt-[100px]">
              <h1 className="text-coal font-black text-[30px]">دیدگاه‌ها</h1>
              <div className="flex gap-6 max-md:flex-col">
                <div className="w-1/4 max-md:w-full max-md:text-center max-md:justify-center max-md:mx-auto flex-col">
                  <div className="flex">
                    <p className="text-coal text-[60px] font-bold">
                      {gymDetails[0].rate}
                    </p>
                    <p className="text-coal text-[20px]">از 5</p>
                  </div>
                  <StarRating rating={gymDetails[0].rate || 0} />
                  <p className="text-coal text-[15px] mt-3">
                    شما هم دیدگاهتان را ثبت کنید
                  </p>
                  <div className="p-4 max-w-md mx-auto bg-gray-100 rounded-lg shadow-md">
                    <button
                      onClick={() => setIsFormVisible(!isFormVisible)}
                      className="w-full py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
                    >
                      ثبت دیدگاه
                    </button>

                    {isFormVisible && (
                      <div className="mt-4">
                        <textarea
                          value={comment}
                          onChange={(e) => setComment(e.target.value)}
                          placeholder="از اینجا نظرتان را با دیگر کاربران به اشتراک بگذارید..."
                          className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-300 resize-none mb-4"
                          rows="4"
                        />
                        {/* <p className="text-center text-gray-700 mb-2">
                          از 1 تا 5 چند ستاره میدهید؟
                        </p>
                        <div className="flex justify-center items-center gap-1 mb-4">
                          <StarRating
                            rating={rating}
                            onRatingChange={handleRating}
                          />
                        </div> */}
                        <button
                          onClick={handleSubmit}
                          className="w-full py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
                        >
                          ارسال نظر
                        </button>
                      </div>
                    )}

                    {comments.length > 0 && (
                      <div className="mt-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">
                          نظرات کاربران:
                        </h3>
                        {comments.map((comment, index) => (
                          <div
                            key={index}
                            className="mb-4 p-4 bg-white rounded-lg shadow"
                          >
                            <div className="flex items-center justify-between mb-2">
                              <p className="text-sm text-gray-600">
                                {comment.writer}
                              </p>
                              <p className="text-sm text-gray-600">
                                {comment.commentDate}
                              </p>
                            </div>
                            <StarRating rating={comment.rate} />
                            <p className="mt-2 text-gray-800">
                              {comment.commentText}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                <div
                  onClick={() => toggleComment()}
                  className="w-3/4 max-md:w-full h-[600px] overflow-y-scroll mb-[70px]"
                >
                  {gymDetails[0].comments.map((comments, index) => (
                    <div key={index} className="flex-col mt-4">
                      <div className="flex items-center gap-2">
                        <p className="text-midtoneGray text-[12px]">
                          {comments.writer}
                        </p>
                        <div className="bg-[#D9D9D9] rounded-full w-[5px] h-[5px]"></div>
                        <p className="text-midtoneGray text-[12px]">
                          {comments.commentDate}
                        </p>
                      </div>
                      <StarRating rating={comments.rate || 0} />

                      <p className="mt-5 text-coal text-[15px]">
                        {comments.commentText}
                      </p>
                      <div className="bg-midtoneGray h-[1px] w-full"></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <Footer_comp />
      </div>
    </>
  );
}
