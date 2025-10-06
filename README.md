# AirMood: Your Personal Voice-Powered Air Quality & Weather Assistant

**AirMood** is an interactive web application that reimagines how people experience weather and air quality forecasts, putting health and accessibility at the center. Built for the NASA Space Apps Challenge, AirMood fuses real-time meteorological data, advanced air quality insights, and the power of voice interaction to help users make better, safer decisions—wherever they are.

---

## 🚀 Challenge Context

This project is a submission for the NASA Space Apps Challenge and directly addresses the [TEMPO Mission Challenge](https://www.nasa.gov/tempo/):

> **"Build a web-based app that forecasts air quality by integrating real-time TEMPO data with ground-based air quality measurements and weather data, notifying users of poor air quality, and helping to improve public health decisions."**

TEMPO (Tropospheric Emissions: Monitoring of Pollution) is revolutionizing air quality monitoring in North America by providing unprecedented, hourly resolution data from space. Combined with ground-based sensors (like Pandora, OpenAQ) and weather data, these datasets allow for actionable, hyperlocal air quality forecasts that empower communities and protect public health.

Outdoor air pollution is a leading global health risk, contributing to millions of deaths annually (WHO). Vulnerable groups—including children, the elderly, and people in industrial or fire-prone areas—are especially at risk. Our app is designed to help individuals, families, and communities limit exposure by making complex air quality and weather data simple, accessible, and actionable.

---

## ✨ Key Features

- **Integrated Data Sources:** Combines real-time weather (OpenWeatherMap), air quality (NASA's TEMPO, OpenAQ—simulated in this prototype), and satellite-based insights.
- **Personalized Recommendations:** Calculates a dynamic "activity score" (0–100) based on weather, air quality, user activity, and physical condition—for truly user-centric health advice.
- **Voice Assistant:** 
  - **Speech-to-Text:** Ask “What’s the air quality like in New York?” with your voice.
  - **Text-to-Speech:** The app speaks back a detailed, friendly summary—tailored to your planned activity and health sensitivities.
- **Clear Visualizations:**
  - **Modern Dashboard:** See temperature, humidity, wind, pressure, and air quality at a glance.
  - **5-Day Forecast:** Daily weather outlooks and air quality trends.
  - **Proactive Alerts:** Warnings for thunderstorms, extreme heat/cold, poor air quality, and more.
- **User-Centric Design:** 
  - Designed for health-sensitive groups, outdoor enthusiasts, families, and public decision-makers.
  - Simple, accessible interface for all ages and backgrounds.
- **Scalable Architecture:** Built with Streamlit and JavaScript, ready for cloud or local deployment.

---

## 🛰️ Data Integration & Novelty

AirMood is inspired by the challenge of merging **satellite**, **ground-based**, and **weather** data. In a production version, the app would:

- Fetch near real-time TEMPO data (e.g., NO₂, HCHO, ozone).
- Integrate ground-based measurements (Pandora, TolNet, OpenAQ).
- Cross-validate satellite and ground data for accuracy.
- Provide hyperlocal forecasts and historical trends.
- Visualize data with intuitive, user-friendly graphics.
- Alert users based on personalized thresholds and health risk factors.

*Note: This prototype simulates NASA air quality data but is architected to support live APIs (TEMPO, OpenAQ, etc.) as they become available.*

---

## 📊 Example Use Cases

- **Sensitive Groups:** Parents or school staff get instant alerts if outdoor conditions are unsafe for children.
- **Outdoor Athletes:** Runners, cyclists, or coaches receive tailored recommendations factoring in ozone, particulates, and weather.
- **Policy Makers:** Visualize local air quality trends, compare satellite and ground data in real time, and download reports.
- **Wildfire Response:** Emergency teams see live pollutant levels and get notified of spikes due to smoke events.
- **General Public:** Anyone can check if it’s a good day to exercise, walk, or simply relax outside.

---

## 🛠️ Tech Stack

- **Backend:** Python
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Data Visualization:** Pandas, Plotly
- **APIs:**
  - **OpenWeatherMap API:** Real-time weather and forecast data.
  - **NASA TEMPO API & OpenAQ (Simulated):** Air quality data.
- **Voice Assistant:** Web Speech API (JavaScript) for speech recognition and synthesis.

---

## 🗂️ Project Structure

```
your-project/
│
├── app.py              # Main Streamlit application
├── recognition.js      # Voice recognition (speech-to-text) script
├── requirements.txt    # Python dependencies
└── README.md           # (This file)
```

---

## ⚙️ How to Run the Project

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser (Chrome, Edge) supporting the Web Speech API

### 2. Installation

Clone this repository and navigate to the folder:

```bash
git clone https://github.com/your-repository.git
cd your-project
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Set these environment variables in your shell (replace with your keys):

- **OpenWeatherMap API Key:** Get from [OpenWeatherMap](https://openweathermap.org/api)
- **NASA API Key:** Get from [api.nasa.gov](https://api.nasa.gov)

```bash
# macOS/Linux
export OPENWEATHER_API_KEY="your_openweathermap_key_here"
export NASA_API_KEY="your_nasa_key_here"

# Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_openweathermap_key_here"
$env:NASA_API_KEY="your_nasa_key_here"
```

### 4. Run the App

```bash
streamlit run app.py
```

Open your browser to the displayed URL. Grant microphone permissions to use the voice assistant.

---

## 📚 Data Sources & References

- [NASA TEMPO Mission](https://www.nasa.gov/tempo/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [OpenAQ Platform](https://openaq.org/)
- [Pandora Air Quality Network](https://www-air.larc.nasa.gov/missions/Pandora/)
- [World Health Organization: Air Pollution](https://www.who.int/health-topics/air-pollution)
- [Web Speech API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

---

## 👥 Potential Users

- Health-sensitive individuals & caregivers
- Schools, eldercare, and healthcare facilities
- Public health and policy professionals
- Outdoor event organizers and coaches
- Emergency responders and disaster planners
- Environmental researchers and citizen scientists

---

## 🌟 Future Improvements

- Live integration with TEMPO and OpenAQ APIs
- Historical air quality and weather trend analysis
- Advanced risk models using demographic/socioeconomic data
- Enhanced alerting (push notifications, SMS, email)
- Mobile app & PWA support
- Support for more languages and accessibility features

---

## 📢 License & Credits

Developed for the NASA Space Apps Challenge by [Your Team/Name].  
This project is for educational and non-commercial purposes. Please cite NASA and OpenWeatherMap data as appropriate.

---