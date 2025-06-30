import { StarIcon } from "@heroicons/react/24/solid";
import { StarIcon as OutlineStarIcon } from "@heroicons/react/24/outline";

const StarRating = ({ rating = 0 }) => {
  // Ensure rating is a valid number and falls within the range 0–5
  const validRating = Math.max(0, Math.min(5, Number(rating) || 0));
  const fullStars = Math.floor(validRating);
  const halfStar = validRating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

  return (
    <div className="flex items-center text-yellow-500">
      {/* Render full stars */}
      {Array.from({ length: fullStars }, (_, index) => (
        <StarIcon key={`full-${index}`} className="w-5 h-5" />
      ))}
      {/* Render a single half star if applicable */}
      {halfStar && <OutlineStarIcon className="w-5 h-5 text-yellow-300" />}
      {/* Render empty stars */}
      {Array.from({ length: emptyStars }, (_, index) => (
        <OutlineStarIcon key={`empty-${index}`} className="w-5 h-5 text-gray-400" />
      ))}
    </div>
  );
};

export default StarRating;
