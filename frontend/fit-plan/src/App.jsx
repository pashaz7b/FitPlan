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
          <Route path="/coach_panel" element={<Coach_panel />} />
          <Route path="/admin_panel" element={<Admin_panel />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;