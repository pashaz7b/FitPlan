import Testing_header from "../components/testing_header";
import { useState } from "react";

export default function Articles() {

    const articles = [
        {
            image: "/Images/edgar-chaparro-sHfo3WOgGTU-unsplash.jpg",
            title: "چه کسی بدنساز است؟",
            summary: "بدن‌ساز واقعی کسی است که فراتر از هدف‌های ظاهری و زیبایی جسمانی، به خودسازی و بهبود مستمر درونی و بیرونی خود اهمیت می‌دهد. او با تعهد و نظم..."
        }
    ];

    return (
        <>
            <Testing_heder />
            <div className="z-20 pt-[200px] bg-mintCream w-full h-full">
                <div className="w-[80%] flex justify-start mx-auto">
                <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                        {coaches.map((coach, index) => (
                            <div
                                key={index}
                                className="rounded-lg p-4 group transition-all transform hover:scale-105 duration-300"
                            >
                                <img
                                    src={coach.image}
                                    alt={coach.name}
                                    className={`h-60 w-60 mx-auto object-cover rounded-full group-hover:shadow-2xl transition-all duration-300
                                    ${
                                        coach.adjustmentClass || "object-top"
                                    }`}
                                />
                                <div className="mt-4">
                                    <h3 className="text-[40px] font-semibold">{coach.name}</h3>
                                    <p className="text-coal mt-2">{coach.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                
                </div>
            </div>
        </>
    );
}