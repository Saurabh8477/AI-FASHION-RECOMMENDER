
import express from "express";
import cors from "cors";
import axios from "axios";

const app = express();
app.use(cors());
app.use(express.json());

const ML_URL = "http://127.0.0.1:8001";

app.post("/api/recommend", async (req, res) => {
  try {
    const r = await axios.post(`${ML_URL}/recommend`, req.body);
    res.json(r.data);
  } catch (e) {
    res.status(500).json({ error: "ML service not reachable" });
  }
});

app.listen(8000, () => console.log("Server running on http://127.0.0.1:8000"));
