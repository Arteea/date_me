import React, { useEffect, useState } from "react";
import Background from "../components/background"; 
import axios from "../api/axios";
import "../App.css";

// Надписи для полей формы
const fieldLabels = {
    description: "Описание",
    birth_date: "Дата рождения",
    birth_place: "Место рождения",
    birth_time: "Время рождения",
    height: "Рост",
    gender: "Пол",
    compatability_preferences: "Предпочтения совместимости",
    zodiac: "Знак зодиака",
};

// Маппинг для пола
const genderMapping = {
    male: "Мужской",
    female: "Женский",
};

const reverseGenderMapping = {
    "Мужской": "male",
    "Женский": "female",
};

// Компонент для рендера поля формы
const FormField = ({ field, value, onChange }) => {
    const isGenderField = field === "gender";
    return (
        <div className="form-group">
            <label>{fieldLabels[field] || field}:</label>
            {isGenderField ? (
                <select name={field} value={genderMapping[value] || ""} onChange={onChange}>
                    <option value="">Выберите пол</option>
                    <option value="Мужской">Мужской</option>
                    <option value="Женский">Женский</option>
                </select>
            ) : (
                <input
                    type="text"
                    name={field}
                    value={value}
                    onChange={onChange}
                />
            )}
        </div>
    );
};

const App = () => {
    const [formData, setFormData] = useState({
        description: "",
        birth_date: "",
        birth_place: "",
        birth_time: "",
        height: "",
        gender: "",
        compatability_preferences: "",
        zodiac: "",
    });

    const [showConfirm, setShowConfirm] = useState(false); // Для отображения окна подтверждения

    // Универсальная функция для API-запросов
    const handleApiRequest = async (method, url, data = {}) => {
        try {
            const response = await axios({
                method,
                url,
                data: ["POST", "PUT", "PATCH"].includes(method) ? data : null,
            });

            if (response.status >= 200 && response.status < 300) {
                if (response.status === 202) {
                    alert("Данные успешно обновлены");
                }
                return response.data;
            } else {
                throw new Error(`Request failed with status ${response.status}`);
            }
        } catch (error) {
            console.error("API Error:", error.response?.data || error.message);
            alert("Ошибка запроса: " + (error.response?.data?.detail || error.message));
        }
    };

    // Получение данных при загрузке
    useEffect(() => {
        const fetchData = async () => {
            const data = await handleApiRequest("GET", "http://127.0.0.1:8000/profile/");
            if (data?.length) {
                setFormData((prevState) => ({
                    ...prevState,
                    ...data[0], // Берем первый объект
                }));
            }
        };
        fetchData();
    }, []);

    // Обработчик изменений в форме
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({
            ...prevState,
            [name]: name === "gender" ? reverseGenderMapping[value] || value : value,
        }));
    };

    // Обработчик отправки формы
    const handleSubmit = async (e) => {
        e.preventDefault();
        const dataToSend = { ...formData };

        if (dataToSend.gender) {
            dataToSend.gender = reverseGenderMapping[dataToSend.gender];
        }

        console.log("Отправляемые данные:", dataToSend);
        await handleApiRequest("PUT", "http://127.0.0.1:8000/profile/", dataToSend);
    };

    // Обработчик удаления профиля
    const handleDelete = async () => {
        await handleApiRequest("DELETE", "http://127.0.0.1:8000/profile/");
        alert("Профиль успешно удален");
        window.location.href = "/api/token/"; // Перенаправление после удаления
    };

    return (
        <div className="container">
            <Background />
            <div className="profile-container">
                <form onSubmit={handleSubmit} className="form">
                    <h1>Профиль пользователя</h1>
                    {Object.keys(formData).map((field) => (
                        <FormField
                            key={field}
                            field={field}
                            value={formData[field]}
                            onChange={handleChange}
                        />
                    ))}
                    <button type="submit" name="Update" className="form-button">
                        Сохранить
                    </button>
                </form>
    
                {/* Кнопка удаления профиля */}
                <div className="delete-profile-container" style={{ marginTop: "30px", textAlign: "center" }}>
                    <button
                        className="delete-button"
                        style={{
                            backgroundColor: "red",
                            color: "white",
                            padding: "10px 20px",
                            border: "none",
                            borderRadius: "5px",
                            cursor: "pointer",
                        }}
                        onClick={() => setShowConfirm(true)}
                    >
                        Удалить профиль
                    </button>
                </div>
            </div>
    
            {/* Модальное окно подтверждения */}
            {showConfirm && (
                <div
                    className="modal-overlay"
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: "100%",
                        backgroundColor: "rgba(0, 0, 0, 0.5)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        zIndex: 1000,
                    }}
                >
                    <div
                        className="confirm-modal"
                        style={{
                            backgroundColor: "white",
                            padding: "20px",
                            borderRadius: "10px",
                            textAlign: "center",
                            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
                        }}
                    >
                        <p>Вы точно хотите удалить ваш профиль?</p>
                        <button
                            className="confirm-yes"
                            style={{
                                marginRight: "10px",
                                backgroundColor: "green",
                                color: "white",
                                padding: "5px 15px",
                                borderRadius: "5px",
                                border: "none",
                                cursor: "pointer",
                            }}
                            onClick={handleDelete}
                        >
                            Да
                        </button>
                        <button
                            className="confirm-no"
                            style={{
                                backgroundColor: "gray",
                                color: "white",
                                padding: "5px 15px",
                                borderRadius: "5px",
                                border: "none",
                                cursor: "pointer",
                            }}
                            onClick={() => setShowConfirm(false)}
                        >
                            Нет
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default App;