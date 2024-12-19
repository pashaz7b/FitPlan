import React from "react";

function VideoOverlay({ videoSrc, onClose }) {
  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        className="relative w-11/12 md:w-3/4 lg:w-1/2"
        onClick={(e) => e.stopPropagation()}
      >
        <video
          src={videoSrc}
          controls
          autoPlay
          className="w-full rounded-lg"
        ></video>
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-white text-2xl font-bold hover:text-red-500"
        >
          &times;
        </button>
      </div>
    </div>
  );
}

export default VideoOverlay;
