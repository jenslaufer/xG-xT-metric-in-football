# ⚽ xG & xT Football Analytics Demo

This Streamlit app is designed to **teach** and **explore** two core football analytics metrics:

- **Expected Goals (xG):** Estimates the chance of a shot resulting in a goal  
- **Expected Threat (xT):** Measures how actions (like passes or carries) increase scoring potential

It provides a dual experience:  
- 👶 **For Laypeople**: Simple, visual explanations with real-pitch examples  
- 🧠 **For Professionals**: Upload match data and explore shot and pass-level metrics with interactive pitch maps

---

## 🚀 Features

- 📊 Visual introduction to xG and xT  
- 📈 Interactive pitch heatmaps  
- 🗃 Upload your own match data as CSV  
- 🔍 Explore by event type (shots, passes)  
- 🎨 Dynamic size/position/heat overlays  
- 🧰 Built with [`mplsoccer`](https://github.com/andrewRowlinson/mplsoccer) and `Streamlit`

---

## 📂 Example CSV Format

The uploaded file should look like this:

```csv
x,y,event_type,xg,xT
88,34,shot,0.45,
65,45,pass,,0.12
```

---

## 🛠 Run Locally

1. Clone the repository:
```bash
git clone https://github.com/jenslaufer/xG-xT-metric-in-football
cd xG-xT-metric-in-football
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the app:
```bash
streamlit run app.py
```

---

## 📦 Docker

1. :
```bash
docker compose up
```


---

## 📖 Learn More

- [StatsBomb xG Model Guide](https://statsbomb.com/articles/soccer/statsbomb-xg-model/)  
- [Expected Threat (xT) by Karun Singh](https://karun.in/blog/expected-threat.html)

---

## 💡 Interested in Modeling, Uncertainty, or Decision Support Tools?

This demo was built by [Solytics](https://www.solytics.de), a team passionate about helping people make better decisions under uncertainty.

👉 Visit [https://www.solytics.de](https://www.solytics.de) if you're interested in:

- Custom analytics or simulation tools  
- Forecasting, risk modeling, or decision intelligence  
- Data-driven product development  

We’d love to hear from you.
