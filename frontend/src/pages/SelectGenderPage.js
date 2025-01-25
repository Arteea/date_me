import React, { useState } from "react";
import Background from "../components/background"; // Импортируем компонент с фоном
import axios from "axios";
import "../App.css";

function App() {
  const [gender, setGender] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [validatedData, setValidatedData] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault(); // Предотвращаем перезагрузку страницы

    try {
      // Отправка данных на сервер
      const response = await axios.post("http://127.0.0.1:8000/select_gender/", {
        gender: gender,
        birth_date: birthDate,
      });

      // Обработка ответа сервера
      if (response.status === 200) {
        const validated = response.data.user_info; // Получаем валидированные данные
        // console.log("Validated data:", validated);
        setValidatedData(validated);
        const zodiacId = validated.zodiac_id
        
        // Сохраняем валидированные данные в localStorage
        localStorage.setItem("user_info_data", JSON.stringify({'gender':gender, 'birth_date': birthDate, 'zodiac_id': zodiacId}));
        alert("Данные успешно сохранены!");
        window.location.href = response.data.redirect_url;  // Клиент выполняет редирект
      }
    } catch (error) {
      console.error("Error during API call:", error.response?.data || error.message);
      alert("Вход строго 18+.");
    }
  };

  return (
    <div className="container"> {/* Основной контейнер для всей страницы */}
      <Background />  {/* Вставляем фон на страницу */}
      <div className="select-gender" style={{ position: "relative", zIndex: 1 }}>
        <div style={{ maxWidth: "400px", margin: "50px auto", textAlign: "center" }}>
          <h1>Выбор пола и даты рождения</h1>
          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
            <label>
              Пол:
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                required
                style={{ padding: "5px", fontSize: "16px" }}
              >
                <option value="" disabled>Выберите пол</option>
                <option value="male">Мужчина</option>
                <option value="female">Женщина</option>
              </select>
            </label>

            <label>
              Дата рождения:
              <input
                type="date"
                value={birthDate}
                onChange={(e) => setBirthDate(e.target.value)}
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
              Отправить
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
