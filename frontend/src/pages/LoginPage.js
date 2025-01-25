import React, { useEffect, useState } from "react";
import Background from "../components/background"; 
import axios from "axios";
import "../App.css";
import { clearLocalStorageExceptTokens } from "../utils/authUtils";



function App() {
    const [username, setUserName] = useState("");
    const [password, setPassword] = useState("");
  

  
    const handleSubmit = async (event) => {
      event.preventDefault(); // Предотвращаем перезагрузку страницы
  
      try {
  
        // Отправка данных на сервер
        const response = await axios.post("http://127.0.0.1:8000/api/token/", {username:username,password:password});
  
        // Обработка ответа сервера
        if (response.status === 200) {
          const validated = response.data; // Получаем валидированные данные
          Object.keys(validated).forEach((key) => {
            localStorage.setItem(key, validated[key]);
          });
          clearLocalStorageExceptTokens();
          window.location.href = response.data.redirect_url; // Клиент выполняет редирект
        }
      } catch (error) {
        console.error("Error during API call:", error.response?.data || error.message);
        alert("Произошла ошибка, попробуйте еще раз.");
      }
    };
  
    return (
      <div className="container"> {/* Основной контейнер для всей страницы */}
      <Background />  {/* Вставляем фон на страницу */}
      <div className="select-gender">
        <div style={{ maxWidth: "400px", margin: "50px auto", textAlign: "center" }}>
          <h1>Введите username и пароль</h1>
  
  
          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
            {/* Поле для логина */}
            <label>
              Username
              <input
                value={username}
                onChange={(e) => setUserName(e.target.value)}
                required
                style={{ padding: "5px", fontSize: "16px" }}
              />
            </label>
  
            {/* Поле для пароля */}
            <label>
              Пароль
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ padding: "5px", fontSize: "16px" }}
              />
            </label>
  
            <button
              type="submit"
              style={{
                padding: "10px 20px",
                fontSize: "16px",
                backgroundColor: "#4CAF50",
                color: "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Войти
            </button>
          </form>
        </div>
      </div>
      </div>
    );
  }

  export default App;