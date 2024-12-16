import { BrowserRouter, Route, Router, Routes } from "react-router-dom";
import Landing from "./pages/landing";
import Articles from "./pages/articles";
import User_login from "./pages/user_login";
import Admin_login from "./pages/admin_login";
import Forgot_Password from "./pages/forgot_password";
import User_signup from "./pages/user_signup";
import Otp_page from "./pages/otp_page";
import User_panel from "./pages/user_panel";
import Coach_panel from "./pages/coach_panel";
import Admin_panel from "./pages/admin_panel";
import About_us from "./pages/about_us";
import Coaches from "./pages/coaches";
import Podcasts from "./pages/podcasts";
import User_info_edit from "./pages/user_info_edit";

function App() {
  // const [count, setCount] = useState(0);

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/articles" element={<Articles />} />
          <Route path="/otp_page/:role" element={<Otp_page />} />
          <Route path="/user_login" element={<User_login />} />
          <Route path="/admin_login" element={<Admin_login />} />
          <Route path="/forgot_password" element={<Forgot_Password />} />
          <Route path="/forgot_password/:role" element={<Forgot_Password />} />
          <Route path="/user_signup" element={<User_signup />} />
          <Route path="/user_panel" element={<User_panel />} />
          <Route path="/user_panel/info_edit" element={<User_info_edit />} />
          <Route path="/coach_panel" element={<Coach_panel />} />
          <Route path="/admin_panel" element={<Admin_panel />} />
          <Route path="/about_us" element={<About_us />} />
          <Route path="/coaches" element={<Coaches />} />
          <Route path="/podcasts" element={<Podcasts />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;