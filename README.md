# 🎙️ AirMood: Voice-Powered Personal Air Quality and Weather Assistant — 2025 NASA Space Apps Challenge

<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/NASA%20Earthdata-blue?style=for-the-badge" alt="NASA Earthdata" />
  <img src="https://img.shields.io/badge/OpenWeatherMap-orange?style=for-the-badge" alt="OpenWeatherMap" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

---

## Introduction

### The Problem
Access to clean air is vital for human health. However, understanding and tracking air quality can be complex, often requiring individuals to search through scattered datasets that lack immediate, personal relevance. Ground-based sensors provide localized readings but suffer from sparse geographic coverage. Meanwhile, advanced satellite observations, such as those from NASA's Tropospheric Emissions: Monitoring of Pollution (TEMPO) mission, offer revolutionary, high-resolution hourly air quality mapping, but raw satellite files are heavy, cloud-hosted, and difficult for average citizens to access and interpret. 

To bridge this gap, public health decisions and daily activities must be supported by intuitive tools that synthesize satellite data, ground measurements, and local weather forecasts into clear, personalized, and easily accessible health insights.

### Program & Project Description
**AirMood** is an interactive, voice-powered web application designed to democratize access to weather and air quality forecasts. By seamlessly merging real-time meteorological data with cutting-edge tropospheric NO₂ insights from NASA’s TEMPO satellite mission, AirMood translates complex environmental parameters into personalized health recommendations—delivered dynamically via voice or text.

This project was developed for the **2025 NASA Space Apps Challenge** on October 4-5, 2025.

- **Award Status**: Global Nominee
- **Registered On**: July 17, 2025
- **Team**: Tropa do Booleano
- **Local Event**: Lajeado
- **Challenge Theme**: *From EarthData to Action: Cloud Computing with Earth Observation Data for Predicting Cleaner, Safer Skies*

---

## Technology Stack

This project leverages a modern Python-based and cloud-native stack designed for swift execution and interactive geospatial processing:

- **Core Language**: Python (3.8+)
- **Frontend & Web Framework**: **Streamlit** (interactive web dashboard with highly customized CSS overrides).
- **Satellite Data Access**: NASA Earthdata Login and the **`earthaccess`** library for querying cloud-hosted datasets.
- **Geospatial Processing**: `netCDF4` and `numpy` (for handling gridded, high-resolution satellite arrays).
- **APIs & Data Feeds**:
  - **OpenWeatherMap API**: Real-time meteorological forecasts, historical trends, and fallback air quality data.
  - **NASA TEMPO Mission L3 NO₂ Products**: High-resolution hourly tropospheric columns.
- **Voice Synthesis & Recognition**: **Web Speech API** (JavaScript integration with Streamlit components for offline Speech-to-Text and Text-to-Speech synthesis).
- **Data Engineering & Visualization**: `pandas` and `plotly` (interactive trend charts).

---

## Key Features Implemented

Unlike standard weather dashboards, AirMood goes far beyond simple tabular displays to deliver a complete, accessibility-focused environmental advisor:

### 1. Direct NASA Earthdata & TEMPO Integration
* **Cloud-Native Data Queries**: Seamlessly authenticates with NASA Earthdata using `earthaccess` to search, retrieve, and download the latest TEMPO `TEMPO_NO2_L3_V03` products.
* **Geospatial Pixel Selection**: Parses large multi-dimensional netCDF4 files and calculates the closest satellite grid coordinates to the user's target city using nearest-neighbor index matching in NumPy.
* **Reliable Failover Strategy**: If TEMPO satellite coverage is unavailable (e.g., coordinates outside North America or processing limits), the app gracefully falls back to OpenWeatherMap's Air Pollution API, guaranteeing constant service availability.

### 2. Intelligent & Personalized Activity Score
* **Dynamic Score Engine**: Calculates a tailored Activity Score (0–100) by cross-referencing multi-variable weather variables (temperature, humidity, wind, and precipitation) and tropospheric air quality.
* **User-Specific Constraints**: Adjusts predictions dynamically according to the user's planned activity (*Running, Walking, Cycling, Outdoor Sports, Light Exercises, Outdoor Rest*) and their physical profile (*Excellent, Good, Moderate, Sensitive, Delicate*).
* **Granular Guidance**: Generates actionable, context-aware warnings (e.g., "High humidity can cause discomfort," "Very poor air quality - avoid outdoor activities").

### 3. Seamless Voice Assistant Integration
* **Speech-to-Text (Voice Search)**: Integrated via a Web Speech API component. Users can tap the microphone button and state queries naturally (e.g., "What is the air quality in Lajeado?"), which are parsed to extract locations.
* **Tailored Text-to-Speech**: Synthesizes a comprehensive spoken report outlining current temperatures, wind speeds, air quality status, current WHO guideline thresholds, and customized activity scores.

### 4. Interactive Dashboard & WHO Safety Guidelines
* **Interactive Historical Trends**: Plots 5-day weather forecasts and pollutant levels using Plotly graphs.
* **WHO Guidelines Checker**: Cross-checks current pollutant levels ($PM_{2.5}, PM_{10}, NO_2, O_3, CO, SO_2$) against official **World Health Organization (2021) thresholds**, flagging whenever limits are exceeded.
* **Proactive Safety Alerts**: Highlights severe environmental events (such as intense storms, extreme heatwaves, or hazardous pollution levels) right at the top of the interface.

---

## 📂 Repository Structure

The project has been cleanly structured to separate backend business logic, UI assets, and client-side integrations:

```bash
.
├── app.py              # Main Streamlit application (Page configurations, APIs, algorithms, and layouts)
├── recognition.js      # Client-side JavaScript for Speech-to-Text recognition and page integration
├── requirements.txt    # Python library dependencies (Streamlit, earthaccess, netCDF4, numpy, etc.)
├── README.md           # This comprehensive documentation
└── readme-template.md  # Template layout reference for repository restructuring
```

---

## Getting Started & Execution Workflow

Follow these steps to run AirMood locally or prepare it for a cloud deployment.

### Step 1: Environment Setup
1. Clone the repository and navigate into the project directory:
   ```bash
   git clone https://github.com/matbdev/nasa-space-apps-airmood.git
   cd nasa-space-apps-airmood
   ```
2. Create and activate a Python virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Credentials & API Configurations
To enable all data integrations, configure the following credentials as environment variables:

1. **OpenWeatherMap API**: Create a free account at [OpenWeatherMap](https://openweathermap.org/) to get an API key.
2. **NASA Earthdata**: Create a free account at [URS Earthdata](https://urs.earthdata.nasa.gov/) to access TEMPO satellite products.

Set these variables in your terminal before launching the application:

```bash
# Linux / macOS
export OPENWEATHER_API_KEY="your_open_weather_key"
export EARTHDATA_USERNAME="your_earthdata_username"
export EARTHDATA_PASSWORD="your_earthdata_password"

# Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_open_weather_key"
$env:EARTHDATA_USERNAME="your_earthdata_username"
$env:EARTHDATA_PASSWORD="your_earthdata_password"
```

### Step 3: Running the Application
Launch the web-based interactive app with Streamlit:
```bash
streamlit run app.py
```
The application will automatically spin up on `http://localhost:8501`. Grant microphone permissions in your browser when prompted to fully experience the Voice Assistant.

---

## Future Steps & Improvements

- [ ] **Expanded NASA Datasets**: Integrate ground-level validation measurements from networks like OpenAQ and Pandora.
- [ ] **Hyper-Local Atmospheric Modeling**: Utilize localized landscape and altitude features to adjust dispersion models of air pollutants.
- [ ] **Push & SMS Notification System**: Deliver automated warnings directly to sensitive users when air quality degrades in their area.
- [ ] **PWA Support**: Wrap the Streamlit-based web dashboard as a Progressive Web App for offline-first and mobile-friendly usability.

---

## Copyright & License

This project was built by team **Tropa do Booleano** for the **2025 NASA Space Apps Challenge** (Local Event: Lajeado / Global Nominee).

This project is licensed under the MIT License - feel free to customize, extend, and adapt it for educational and public health purposes. Please credit **NASA Earthdata** and **OpenWeatherMap** as data providers.