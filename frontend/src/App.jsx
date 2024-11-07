import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");

  // Получаем данные пользователя через Telegram Web App
  useEffect(() => {
    const tg = window.Telegram.WebApp;
    setUsername(tg.initDataUnsafe?.user?.username || "Guest");
  }, []);

  // Отправка данных на сервер
  const handleSubmit = async () => {
    try {
      await axios.post("https://api.tvoitrenerbot.ru/api/user_data", {
        user_id: Math.random(),  // Тестовый user_id для примера
        username,
        text: message,
      });
      alert("Message sent successfully!");
    } catch (error) {
      console.error("Failed to send message:", error);
    }
  };

  return (
    <div className="App">
      <h1>Hello, {username}!</h1>
      <input
        type="text"
        placeholder="Enter your message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={handleSubmit}>Send Message</button>
    </div>
  );
}

export default App;
