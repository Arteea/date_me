import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import SelectGenderPage from "./pages/SelectGenderPage";
import MainPage from "./pages/MainPage";
import EnterNameSurnamePage from "./pages/EnterNameSurnamePage";
import EnterContactInfoPage from "./pages/EnterContactInfoPage";
import LoginPage from "./pages/LoginPage"
import ProfilePage from "./pages/ProfilePage"
import EmailConfirmationPage from "./pages/EmailConfirmationPage"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/select_gender/" element={<SelectGenderPage />} />
        <Route path="/enter_name_surname/" element={<EnterNameSurnamePage />} />
        <Route path="/enter_contact_info/" element={<EnterContactInfoPage />} />
        <Route path="/api/token/" element={<LoginPage />} />
        <Route path="/profile/" element={<ProfilePage />} />
        <Route path="/confirm_email/" element={<EmailConfirmationPage />} />
      </Routes>
    </Router>
  );
}

export default App;








// import React from "react";
// import axios from "axios";

// function App() {
//   const handleAction = async (action) => {
//     try {
//       const response = await axios.post("http://127.0.0.1:8000/", {
//         action: action,
//       });

//       if (response.data.redirect_url) {
//         window.location.href = response.data.redirect_url; // Перенаправление на указанный URL
//       }
//     } catch (error) {
//       console.error("Error during API call:", error.response?.data || error.message);
//       alert("An error occurred. Please try again.");
//     }
//   };

//   return (
//     <div style={{ textAlign: "center", marginTop: "20%" }}>
//       <h1>Welcome to Date_Me Dating Service!</h1>
//       <button
//         onClick={() => handleAction("signup")}
//         style={{
//           marginRight: "10px",
//           padding: "10px 20px",
//           backgroundColor: "#4CAF50",
//           color: "white",
//           border: "none",
//           borderRadius: "5px",
//           cursor: "pointer",
//         }}
//       >
//         Регистрация
//       </button>
//       <button
//         onClick={() => handleAction("login")}
//         style={{
//           padding: "10px 20px",
//           backgroundColor: "#008CBA",
//           color: "white",
//           border: "none",
//           borderRadius: "5px",
//           cursor: "pointer",
//         }}
//       >
//         Войти
//       </button>
//     </div>
//   );
// }

// export default App;
