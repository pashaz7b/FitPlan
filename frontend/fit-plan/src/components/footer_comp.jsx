import fit_logo from "/Images/Fit-Logo-Resized.png";

export default function Footer_comp() {
    return(
        <>
            <div className="bg-black text-mintCream flex gap-[12%] justify-start px-[200px] py-[50px] max-md:flex-col max-md:px-[50px] max-md:gap-[80px] max-md:max-h-full max-md:justify-center max-md:text-center max-lg:px-[50px]">
                {/* logo and contact info */}
                <div className="flex flex-col gap-4 text-right max-md:text-center max-md:justify-center max-md:mx-auto">
                    <div className="h-[70px]">
                        <img src={fit_logo} alt="" className="object-contain h-full" />
                    </div>
                    <div className="flex justify-start gap-3 max-md:justify-center max-md:text-center">
                        <svg width="40" height="40" viewBox="0 0 40 40" fill="#FFF7ED" xmlns="http://www.w3.org/2000/svg">
                            <path d="M7.17954 32.5C6.3376 32.5 5.62496 32.2083 5.04163 31.625C4.45829 31.0417 4.16663 30.329 4.16663 29.4871V10.5129C4.16663 9.67097 4.45829 8.95833 5.04163 8.375C5.62496 7.79167 6.3376 7.5 7.17954 7.5H32.8204C33.6623 7.5 34.375 7.79167 34.9583 8.375C35.5416 8.95833 35.8333 9.67097 35.8333 10.5129V29.4871C35.8333 30.329 35.5416 31.0417 34.9583 31.625C34.375 32.2083 33.6623 32.5 32.8204 32.5H7.17954ZM33.3333 12.4038L20.8108 20.42C20.6827 20.4925 20.5502 20.5496 20.4133 20.5913C20.2766 20.6329 20.1388 20.6538 20 20.6538C19.8611 20.6538 19.7233 20.6329 19.5866 20.5913C19.4497 20.5496 19.3172 20.4925 19.1891 20.42L6.66663 12.4038V29.4871C6.66663 29.6368 6.71468 29.7597 6.81079 29.8558C6.9069 29.9519 7.02982 30 7.17954 30H32.8204C32.9701 30 33.093 29.9519 33.1891 29.8558C33.2852 29.7597 33.3333 29.6368 33.3333 29.4871V12.4038ZM20 18.3333L33.077 10H6.92288L20 18.3333ZM6.66663 12.7883V10.8829V10.9325V10.8796V12.7883Z" fill="#FFF7ED"/>
                        </svg>
                        <p className="pt-2">Fitplan@gmail.com</p>
                    </div>
                    <div className="flex justify-start gap-3 max-md:justify-center max-md:text-center">
                        <svg width="40" height="40" viewBox="0 0 40 40" fill="#FFF7ED" xmlns="http://www.w3.org/2000/svg">
                            <path d="M7.59962 34.1666C7.0949 34.1666 6.67435 33.9999 6.33796 33.6666C6.00157 33.3333 5.83337 32.9166 5.83337 32.4166V27.0128C5.83337 26.6089 5.96643 26.2478 6.23254 25.9295C6.49865 25.6112 6.84212 25.3964 7.26296 25.2853L11.8909 24.3428C12.2906 24.2873 12.6757 24.3139 13.0463 24.4228C13.4171 24.532 13.733 24.7223 13.9938 24.9937L17.7338 28.7662C18.9282 28.0909 20.0405 27.3612 21.0705 26.577C22.1005 25.7928 23.0727 24.9434 23.9871 24.0287C24.9146 23.1078 25.7763 22.1416 26.5721 21.1299C27.3682 20.118 28.076 19.0448 28.6955 17.9103L24.8463 14.1633C24.6027 13.941 24.4338 13.6664 24.3396 13.3395C24.2457 13.0126 24.2318 12.6216 24.298 12.1666L25.2534 7.26284C25.3409 6.85895 25.5455 6.51978 25.8671 6.24534C26.1888 5.97061 26.56 5.83325 26.9809 5.83325H32.4167C32.9167 5.83325 33.3334 6.00145 33.6667 6.33783C34 6.67422 34.1667 7.09478 34.1667 7.5995C34.1667 10.7403 33.4364 13.893 31.9759 17.0574C30.5153 20.2221 28.4577 23.1346 25.803 25.7949C23.148 28.4549 20.2356 30.5152 17.0659 31.9758C13.8959 33.4363 10.7405 34.1666 7.59962 34.1666ZM29.8525 15.5449C30.3675 14.376 30.7688 13.2039 31.0563 12.0287C31.3435 10.8537 31.5299 9.69672 31.6155 8.55784C31.6155 8.49367 31.5941 8.4402 31.5513 8.39742C31.5085 8.35464 31.455 8.33325 31.3909 8.33325H27.8525C27.767 8.33325 27.6975 8.35464 27.6442 8.39742C27.5909 8.4402 27.5535 8.50423 27.5321 8.5895L26.7821 12.3141C26.7607 12.3783 26.7581 12.4477 26.7742 12.5224C26.79 12.5971 26.8248 12.6559 26.8784 12.6987L29.8525 15.5449ZM15.3525 29.8974L12.4105 26.9228C12.3568 26.8695 12.306 26.8348 12.258 26.8187C12.2099 26.8028 12.1538 26.8056 12.0896 26.827L8.58962 27.5641C8.50435 27.5855 8.44032 27.6228 8.39754 27.6762C8.35476 27.7295 8.33337 27.7989 8.33337 27.8845V31.3908C8.33337 31.4549 8.35476 31.5084 8.39754 31.5512C8.44032 31.5939 8.49379 31.6153 8.55796 31.6153C9.60046 31.5639 10.7174 31.3935 11.9088 31.1041C13.0999 30.8146 14.2478 30.4124 15.3525 29.8974Z" fill="#FFF7ED"/>
                        </svg>

                        <p className="pt-2">989123456789+</p>
                    </div>
                </div>

                {/* social media */}
                <div className="felx flex-col">
                    <p className="text-[25px] font-semibold mb-[13px]">شبکه‌های اجتماعی</p>
                    <div className="h-[30px] flex justify-between max-md:justify-center max-md:gap-5">
                        <img src="/Images/YouTube.png" alt="YouTube_Logo" className="h-full object-contain hover:scale-[120%] transition-all duration-300"/>
                        <img src="/Images/Telegram.png" alt="" className="h-full object-contain hover:scale-[120%] transition-all duration-300"/>
                        <img src="/Images/Instagram.png" alt="" className="h-full object-contain hover:scale-[120%] transition-all duration-300"/>
                        <img src="/Images/Facebook.png" alt="" className="h-full object-contain hover:scale-[120%] transition-all duration-300"/>
                    </div>
                </div>

                <div className="max-md:flex max-md:flex-col max-md:justify-center max-md:text-center max-md:mx-auto">
                    <p className="text-[25px] font-semibold mb-[13px]">درباره ما</p>
                    <p className="text-justify max-w-[547px] max-h-[200px] overflow-hidden max-md:text-center">تیم ما از مربیان با تجربه و علاقه‌مندان به ورزش تشکیل شده که همواره در کنار شما هستند تا شما را در هر مرحله از مسیر پیشرفت حمایت کنند. به ما بپیوندید تا با هم به هدف‌های ورزشی‌تان دست یابیم و از تجربه‌ای لذت‌بخش در بدنسازی بهره‌مند شوید.</p>
                </div>
            </div>  
            <div className="bg-black flex justify-center text-center w-full max-h-[40px] max-sm:max-h-[80px]">
                <div className="w-[50%] py-1 max-lg:py-0 max-lg:w-[80%] max-lg:max-h-[80px] max-sm:px-1 bg-superRed text-mintCream rounded-t-[15px]">
                    <p>طراحی شده و توسعه یافته توسط ارمیا زواری و امیرحسین پاشا - پائیز 1403</p>
                </div>
            </div>
        </>
    );
}