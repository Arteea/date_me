import React, { useEffect, useState } from "react";
import Background from "../components/background"; 
import axios from "axios";
import "../App.css";

function App() {
  const [email, setEmail] = useState("");
  const [username, setUserName] = useState("");
  const [phone_number, setPhoneNumber] = useState("");
  const [password, setPassword] = useState("");
  const [userData, setUserData] = useState({}); // Для хранения всех данных (gender, birth_date, first_name, last_name)

  // Загрузка данных из localStorage при загрузке компонента
  useEffect(() => {
    const savedData = localStorage.getItem("user_info_data");
    if (savedData) {
      setUserData(JSON.parse(savedData)); // Загружаем данные
    }
  }, []); 

  const handleSubmit = async (event) => {
    event.preventDefault(); // Предотвращаем перезагрузку страницы

    try {

      // Отправка данных на сервер
      const response = await axios.post("http://127.0.0.1:8000/enter_contact_info/", {user_data:userData,email:email,phone_number:phone_number,username:username,password:password});

      // Обработка ответа сервера
      if (response.status === 200) {
        const validated = response.data.user_data; // Получаем валидированные данные
        // const existingData = userData ? JSON.parse(localStorage.getItem("user_info_data")) : {};

        // Объединяем старые и новые данные
        const updatedData = {
          ...validated,
          ...userData,

        }
        // Сохраняем объединенные данные в localStorage

        localStorage.setItem("user_info_data", JSON.stringify(updatedData));
        
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
        <h1>Введите контактную информацию</h1>

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
          {/* Поле для имени */}
          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{ padding: "5px", fontSize: "16px" }}
            />
          </label>

          {/* Поле для фамилии */}
          <label>
            Юзернейм
            <input
              type="text"
              value={username}
              onChange={(e) => setUserName(e.target.value)}
              required
              style={{ padding: "5px", fontSize: "16px" }}
            />
          </label>
          <label>
            Номер телефона
            <input
              type="tel"
              value={phone_number}
              onChange={(e) => setPhoneNumber(e.target.value)}
              required
              style={{ padding: "5px", fontSize: "16px" }}
            />
          </label>
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
            Далее
          </button>
        </form>
      </div>
    </div>
    </div>
  );
}

export default App;