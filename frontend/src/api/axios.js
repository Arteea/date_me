import axios from "axios";

// Ключи для хранения токенов в localStorage
const ACCESS_TOKEN_KEY = "access";
const REFRESH_TOKEN_KEY = "refresh";

// Создаем экземпляр Axios
const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/", // Базовый URL API
  timeout: 5000, // Тайм-аут
  headers: {
    "Content-Type": "application/json",
  },
});

// Добавляем interceptor для запросов
axiosInstance.interceptors.request.use(
  (config) => {
    // Извлекаем access токен из localStorage
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Обработка ошибок отправки запроса
    return Promise.reject(error);
  }
);

// Добавляем interceptor для ответов
axiosInstance.interceptors.response.use(
  (response) => {
    // Успешный ответ
    return response;
  },
  async (error) => {
    // Если ошибка связана с токеном (401), можно попытаться обновить токен
    if (error.response?.status === 401) {
      try {
        // Извлекаем refresh токен из localStorage
        const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
        if (!refreshToken) {
          throw new Error("Refresh token отсутствует");
        }

        // Обновляем access токен
        const response = await axios.post("http://127.0.0.1:8000/api/token/refresh/", {
          refresh: refreshToken,
        });

        // Сохраняем новый access токен в localStorage
        localStorage.setItem(ACCESS_TOKEN_KEY, response.data.access);

        // Повторяем исходный запрос с новым токеном
        error.config.headers["Authorization"] = `Bearer ${response.data.access}`;
        return axiosInstance.request(error.config);
      } catch (refreshError) {
        console.error("Refresh token failed", refreshError);

        // Если обновление токена не удалось, выполняем логаут
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        window.location.href = "/api/token";
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;

