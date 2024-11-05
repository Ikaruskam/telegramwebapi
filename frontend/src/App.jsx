import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios'
import AddItemForm from './AddItemForm' // Импортируем новый компонент

function App() {
  const [items, setItems] = useState(null)

  const fetchItems = () => {
    axios.get('https://api.tvoitrenerbot.ru/items').then(r => {
      setItems(r.data)
    })
  }

  useEffect(() => {
    fetchItems()
    const interval = setInterval(() => {
      fetchItems()
    }, 2000)
    return () => clearInterval(interval)  // Очищаем интервал при размонтировании
  }, [])

  return (
    <div>
      <AddItemForm onItemAdded={fetchItems} /> {/* Передаем функцию обновления */}
      <div>
        {items && items.map(item => (
          <span style={{ padding: '0px 4px' }} key={item.id} className="roll-out">
            <img src={item.img} alt='logo' width="16" style={{ padding: '0px 5px' }} />
            <span>{item.name} — Вес: {item.weight} кг, Рост: {item.height} см</span>
          </span>
        ))}
      </div>
    </div>
  )
}

export default App
