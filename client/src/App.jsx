
import { useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000/api";

export default function App() {
  const [query, setQuery] = useState("streetwear black");
  const [items, setItems] = useState([]);

  async function getRecs() {
    const { data } = await axios.post(`${API}/recommend`, { query });
    setItems(data.results);
  }

  return (
    <div style={{padding:20}}>
      <h1>AI Fashion Recommender</h1>
      <input value={query} onChange={(e)=>setQuery(e.target.value)} />
      <button onClick={getRecs}>Recommend</button>
      <ul>
        {items.map(p => (
          <li key={p.id}>{p.name} - ₹{p.price}</li>
        ))}
      </ul>
    </div>
  );
}
