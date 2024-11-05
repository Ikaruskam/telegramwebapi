import { useState } from 'react'
import axios from 'axios'

function AddItemForm({ onItemAdded }) {
  const [name, setName] = useState("")
  const [weight, setWeight] = useState("")
  const [height, setHeight] = useState("")

  const handleAddItem = () => {
    // Отправляем данные на сервер
    axios.post('https://api.tvoitrenerbot.ru/add_item', {
      name,
      weight: parseFloat(weight),
      height: parseFloat(height),
      img: "https://example.com/default-image.png"
    })
    .then(response => {
      onItemAdded() // Сообщаем родительскому компоненту, что элемент добавлен
    })
    .catch(error => {
      console.error("Ошибка при добавлении элемента!", error)
    })
  }

  return (
    <div>
      <h3>Добавить новый элемент</h3>
      <input
        type="text"
        placeholder="Имя"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Вес"
        value={weight}
        onChange={(e) => setWeight(e.target.value)}
      />
      <input
        type="number"
        placeholder="Рост"
        value={height}
        onChange={(e) => setHeight(e.target.value)}
      />
      <button onClick={handleAddItem}>Добавить</button>
    </div>
  )
}

export default AddItemForm
