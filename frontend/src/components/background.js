import React from "react";

const Background = () => {
  return (
    <div
      style={{
        position: "absolute", // Фон будет на абсолютном положении
        top: "0", // Вверх
        left: "0", // Влево
        width: "100%", // Ширина на весь экран
        height: "100vh", // Высота на весь экран
        backgroundColor: "#ADD8E6", // Пастельно-голубой фон
        overflow: "hidden", // Не показывать части, выходящие за пределы экрана
        zIndex: -1, // Фон будет находиться позади всех других элементов
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
    </div>
  );
};

export default Background;