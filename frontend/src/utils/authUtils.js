//Используем для очищения localstorage
export const clearLocalStorageExceptTokens = () => {
    const accessToken = localStorage.getItem("access");
    const refreshToken = localStorage.getItem("refresh");

    localStorage.clear();

    if (accessToken) localStorage.setItem("access", accessToken);
    if (refreshToken) localStorage.setItem("refresh", refreshToken);
};