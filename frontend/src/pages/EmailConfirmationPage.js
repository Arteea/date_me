import React, { useEffect, useState } from "react";
import { useNavigate,useLocation, } from "react-router-dom";
import axios from "axios";

const EmailConfirmation = () => {
    const [status, setStatus] = useState("loading");
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const token = queryParams.get("token");

        if (!token) {
            setStatus("error");
            return;
        }

        // Отправляем GET-запрос с токеном на бэкенд
    axios.get(`http://127.0.0.1:8000/confirm_email/?token=${token}`)
    .then((response) => {
        setStatus("success");  // Если подтверждение успешно
    })
    .catch((error) => {
        console.error("Ошибка подтверждения email:", error.response?.data || error.message);
        setStatus("error");  // Ошибка при подтверждении
    });
}, [location]);

useEffect(() => {
    if (status === "success") {
        // Устанавливаем таймер на 3 секунды
        const timer = setTimeout(() => {
            navigate("/api/token/"); // Перенаправляем на страницу логина
        }, 10000);

        return () => clearTimeout(timer); // Очищаем таймер при размонтировании
    }
}, [status, navigate]);

    if (status === "loading") {
        return <p>Подтверждение email...</p>;
    }

    if (status === "success") {
        return <div  style={{textAlign: "center"}}> <p>Ваш email успешно подтвержден! Теперь вы можете войти в систему.
            <br /> Вы будете перенаправлены через 10 секунд...
        </p></div>;
    }

    return <p>Ошибка подтверждения email. Возможно, ссылка недействительна или устарела.</p>;
};

export default EmailConfirmation;