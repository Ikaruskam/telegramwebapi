import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios'
import AddItemForm from './AddItemForm'

function App() {
  const [items, setItems] = useState([])

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
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      <AddItemForm onItemAdded={fetchItems} />
      <div>
        {items.map(item => (
          <span style={{ padding: '0px 4px' }} key={item.id} className="roll-out">
            <span>{item.name} — Вес: {item.weight} кг, Рост: {item.height} см</span>
          </span>
        ))}
      </div>
    </div>
  )
}

export default App
