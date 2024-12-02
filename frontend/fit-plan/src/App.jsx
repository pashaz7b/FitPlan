import { BrowserRouter, Route, Router, Routes } from "react-router-dom";
import Landing from "./pages/landing";
import Articles from "./pages/articles";
import User_login from "./pages/user_login";
import Admin_login from "./pages/admin_login";
import Forgot_Password from "./pages/forgot_password";
import User_signup from "./pages/user_signup";

function App() {
  // const [count, setCount] = useState(0);

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/articles" element={<Articles />} />
          <Route path="/user_login" element={<User_login />} />
          <Route path="/admin_login" element={<Admin_login />} />
          <Route path="/forgot_password" element={<Forgot_Password />} />
          <Route path="/forgot_password/:role" element={<Forgot_Password />} />
          <Route path="/user_signup" element={<User_signup />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;