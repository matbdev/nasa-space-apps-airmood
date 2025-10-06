# AirMood: Voice-Powered Personal Air Quality and Weather Assistant

**AirMood** is an interactive web application designed to transform how users access and understand weather and air quality forecasts. By merging real-time meteorological data from OpenWeatherMap with cutting-edge air quality insights from NASA’s TEMPO mission (via the NASA Earthdata platform), AirMood delivers personalized health recommendations—accessible by text or voice.

This project is a submission for the [NASA Space Apps Challenge 2025 – From Earthdata to Action: Cloud Computing with Earth Observation Data for Predicting Cleaner, Safer Skies](https://www.spaceappschallenge.org/2025/challenges/from-earthdata-to-action-cloud-computing-with-earth-observation-data-for-predicting-cleaner-safer-skies/?tab=details).

---

## ✨ Key Features

- **Personalized Recommendations:** Calculates an "activity score" (0–100) by cross-referencing weather data (temperature, humidity, wind), tropospheric NO₂ air quality data from NASA, the user’s planned activity, and physical condition.
- **Direct NASA Earthdata Integration:** Retrieves tropospheric NO₂ data from NASA’s TEMPO satellite using the [earthaccess library](https://nsidc.github.io/earthaccess/), providing robust, science-backed health advice. If TEMPO data is unavailable, the app gracefully falls back to OpenWeatherMap Air Quality data.
- **Full Voice Assistant:**
  - **Speech-to-Text:** Users can ask, “What’s the air quality in São Paulo?” and more using only their voice.
  - **Text-to-Speech:** The application reads back a comprehensive, user-tailored summary, including weather, air quality, and activity recommendations.
- **Detailed Data Visualization:**
  - **Modern Weather Dashboard:** Displays current temperature, feels-like, humidity, wind, and pressure.
  - **5-Day Forecast:** Offers clear, daily weather and air quality trends.
  - **Proactive Safety Alerts:** Notifies users of extreme events such as storms, high heat, or hazardous air quality, with actionable guidance.
- **Accessible and User-Centric:** Designed for health-sensitive groups, families, athletes, educators, and public decision-makers.

---

## 🛰️ NASA Data & Cloud-Native Architecture

- **TEMPO Satellite Data:** AirMood leverages NASA’s [Earthdata cloud platform](https://earthdata.nasa.gov/) to access real-time tropospheric NO₂ data from the TEMPO mission, using the [earthaccess Python library](https://nsidc.github.io/earthaccess/). This enables high-resolution, hourly air quality forecasts across North America.
- **Fallback Strategy:** If TEMPO data is inaccessible, the app automatically retrieves comparable air quality data (AQI, PM2.5, O₃, CO) from OpenWeatherMap’s Air Pollution API, ensuring continuous functionality.
- **Geospatial Processing:** netCDF4 and numpy are used to handle and extract insights from large, cloud-hosted Earth observation datasets.

---

## 🚀 Tech Stack

- **Backend:** Python
- **Frontend:** Streamlit
- **Data Visualization:** Pandas, Plotly
- **APIs and Data Sources:**
  - [OpenWeatherMap API](https://openweathermap.org/api): Real-time weather and air quality data.
  - [NASA Earthdata (earthaccess)](https://earthdata.nasa.gov/): Direct access to tropospheric NO₂ from TEMPO.
- **Voice Assistant:** Web Speech API (JavaScript) for speech recognition and synthesis ([MDN Docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)).
- **Data Processing:** [netCDF4](https://unidata.github.io/netcdf4-python/) and [NumPy](https://numpy.org/) for geospatial and scientific data manipulation.

---

## ⚙️ How to Run the Project

Follow these steps to set up and run AirMood locally.

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser supporting the Web Speech API (e.g., Chrome, Edge)
- A [NASA Earthdata](https://urs.earthdata.nasa.gov/) account (to access TEMPO data)

### 2. Project Structure

```
nasa-space-apps-airmood/
│
├── app.py              # Main Streamlit application
├── recognition.js      # Voice recognition script (JavaScript)
├── requirements.txt    # Python dependencies
└── README.md           # (This file)
```

### 3. Installation & Configuration

Clone the repository and navigate to the folder:

```bash
git clone https://github.com/matbdev/nasa-space-apps-airmood.git
cd nasa-space-apps-airmood
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

Install the dependencies:

```bash
pip install -r requirements.txt
```

#### Set Environment Variables

- **OpenWeatherMap API Key:**  
  Obtain a free key from [OpenWeatherMap](https://openweathermap.org/api) and set it:
  ```bash
  export OPENWEATHER_API_KEY="your_openweathermap_key_here"
  ```
- **NASA Earthdata Credentials:**  
  Create a free account at [URS](https://urs.earthdata.nasa.gov/).  
  Set your username and password as environment variables:
  ```bash
  export EARTHDATA_USERNAME="your_earthdata_username"
  export EARTHDATA_PASSWORD="your_earthdata_password"
  ```

> On Windows (PowerShell), use `$env:VAR_NAME="value"` syntax.

---

### 4. Run the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

The application will open automatically in your browser.  
Grant microphone permission when prompted to use the voice assistant.

---

## 📚 References & Data Sources

- [NASA Earthdata Cloud](https://earthdata.nasa.gov/)
- [TEMPO Mission](https://tempo.si.edu/)
- [earthaccess Python Library](https://nsidc.github.io/earthaccess/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [netCDF4 Python Library](https://unidata.github.io/netcdf4-python/)
- [NumPy](https://numpy.org/)
- [Web Speech API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Space Apps Challenge: From Earthdata to Action](https://www.spaceappschallenge.org/2025/challenges/from-earthdata-to-action-cloud-computing-with-earth-observation-data-for-predicting-cleaner-safer-skies/?tab=details)

---

## 👥 Potential Users

- Health-sensitive individuals and caregivers
- Schools, eldercare, and healthcare facilities
- Public health professionals and policy makers
- Outdoor athletes, event organizers, and coaches
- Emergency responders and disaster planners
- Environmental researchers and citizen scientists

---

## 🌟 Future Directions

- Live integration with additional NASA and partner datasets (e.g., OpenAQ, Pandora, TolNet)
- Mobile app and PWA support
- Automated historical air quality and weather trend analysis
- Advanced risk models using demographic and socioeconomic data
- Push notifications, SMS, or email alerts
- Multi-language and accessibility enhancements

---

## 📢 License & Credits

Developed for the [NASA Space Apps Challenge 2025](https://www.spaceappschallenge.org/2025/challenges/from-earthdata-to-action-cloud-computing-with-earth-observation-data-for-predicting-cleaner-safer-skies/?tab=details) by [Your Team/Name].  
This project is for educational and non-commercial purposes. Please credit NASA Earthdata and OpenWeatherMap as appropriate.

---