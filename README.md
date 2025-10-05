# 🌤️ AirMood: Personal Voice-Powered Weather Assistant

**AirMood** is an interactive web application that redefines the weather forecast experience.  
Powered by the **OpenWeatherMap API** and a sleek **Streamlit** interface, it delivers **personalized climate insights** focused on user health and well-being.

The highlight feature is the **integrated voice assistant**, enabling users to ask for the weather in any city using only their voice — and receive a complete **spoken summary** in return.

---

## ✨ Key Features

### 🔹 Smart Personalization
- **Personalized recommendations**: Calculates an *activity score* (0–100) by cross-referencing weather conditions (temperature, humidity, wind) and air quality with the user’s planned activity and physical condition.

### 🔹 Complete Voice Assistant
- **Speech-to-Text Recognition**: Ask for the weather in any city using your voice.  
- **Text-to-Speech Synthesis**: Hear a detailed spoken summary of weather, air quality, and activity recommendations.

### 🔹 Rich Data Visualization
- **Modern Weather Dashboard**: Displays temperature, “feels like” temperature, humidity, wind, pressure, and visibility.  
- **5-Day Forecast**: Clear, concise daily weather outlook.  
- **Air Quality (AQI)**: Shows overall index and pollutant levels (*PM2.5, Ozone, CO*).  
- **Proactive Safety Alerts**: Warnings for extreme conditions like thunderstorms, intense heat, or unhealthy air quality.

---

## 🚀 Tech Stack

- **Backend**: Python  
- **Frontend**: Streamlit  
- **Data Visualization**: Plotly Express, Pandas  
- **APIs**:  
  - OpenWeatherMap API → Weather, forecast, and air quality  
  - Web Speech API (JavaScript) → Speech recognition & synthesis  

---

## ⚙️ How to Run

### 1. Prerequisites
- Python **3.8+**  
- **pip** (Python package manager)

---

### 2. Project Structure



---

### 3. Installation

**a. Clone the repository and navigate to the project folder:**
```bash
git clone https://your-repository.git
cd your-project

**b. Create and activate a virtual environment (recommended):**
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
