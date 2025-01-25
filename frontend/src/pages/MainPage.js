import React from "react";
import axios from "axios";
import "../App.css";

function App() {
  const handleAction = async (action) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/", { action: action });
  
      if (response.data.redirect_url) {
        window.location.href = response.data.redirect_url;  // Клиент выполняет редирект
      }
    } catch (error) {
      console.error("Error during API call:", error.response?.data || error.message);
      alert("An error occurred. Please try again.");
    }
  };
  

  return (
    <div 
      style={{
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        backgroundColor: "#ADD8E6", // Пастельно-голубой фон
        overflow: "hidden",
      }}
    >
      {/* Волны в нижней части экрана */}
      <svg
        style={{
          position: "absolute",
          bottom: "0",
          left: "0",
          width: "100%",
          height: "50%", // Размер волны
          fill: "none", // Без заливки
        }}
        viewBox="0 0 1340 320"
      >
        <path
          d="M0,160 C300,200 500,100 720,160 C940,220 1200,120 1440,180 L1440,320 L0,320 Z"
          fill="#7EC8E3" // Темнее фонового цвета
          stroke="white" // Белая окантовка
          strokeWidth="2" // Толщина окантовки
        />
      </svg>

      {/* Левая половина сердечка */}
      <div
        style={{
          position: "absolute",
          left: "0",
          top: "50%",
          transform: "translateY(-50%)",
          width: "50%",
          height: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <svg
          viewBox="0 0 100 100"
          style={{
            width: "100%",
            height: "100%",
            cursor: "pointer",
          }}
          onClick={() => handleAction("signup")}
        >
          <path
            d="M50,80 Q10,50 30,20 A15,15 0 0,1 50,35 A15,15 0 0,1 70,20 Q90,50 50,80 Z"
            fill="#FF6666"
            stroke="white" // Белая окантовка
            strokeWidth="2" // Толщина окантовки
          />
          <text
            x="50"
            y="50"
            textAnchor="middle"
            dominantBaseline="middle"
            fontSize="6"
            fill="white"
            fontWeight="bold"
          >
            Регистрация
          </text>
        </svg>
      </div>

      {/* Правая половина сердечка */}
      <div
        style={{
          position: "absolute",
          right: "0",
          top: "50%",
          transform: "translateY(-50%)",
          width: "50%",
          height: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <svg
          viewBox="0 0 100 100"
          style={{
            width: "100%",
            height: "100%",
            cursor: "pointer",
          }}
          onClick={() => handleAction("login")}
        >
          <path
            d="M50,80 Q90,50 70,20 A15,15 0 0,0 50,35 A15,15 0 0,0 30,20 Q10,50 50,80 Z"
            fill="#6666FF"
            stroke="white" // Белая окантовка
            strokeWidth="2" // Толщина окантовки
          />
          <text
            x="50"
            y="50"
            textAnchor="middle"
            dominantBaseline="middle"
            fontSize="6"
            fill="white"
            fontWeight="bold"
          >
            Войти
          </text>
        </svg>
      </div>
    </div>
  );
}

export default App;