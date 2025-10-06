import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from PIL import Image
import io
import os
from typing import Optional, Dict, Any, Tuple, List
import earthaccess
import netCDF4 as nc
import numpy as np

# --- PAGE SETUP ---

def setup_page_config():
    """Configures the Streamlit page properties."""
    st.set_page_config(
        page_title="Advanced Weather Forecast with Voice Assistant",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    """Loads custom CSS for the application."""
    st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        .big-font { font-size: 20px !important; font-weight: bold; }
        .weather-container { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px; 
            padding: 25px; 
            margin-top: 15px; 
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .temperature { 
            font-size: 56px; 
            font-weight: bold; 
            color: #ffffff; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .weather-icon { font-size: 36px; }
        .forecast-card { 
            background-color: #ffffff; 
            border-radius: 12px; 
            padding: 18px; 
            margin: 8px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            text-align: center;
            transition: transform 0.2s ease;
        }
        .forecast-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }
        .recommendation-card { 
            border: 3px solid; 
            border-radius: 15px; 
            padding: 25px; 
            margin-bottom: 25px; 
            text-align: center;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }
        .recommendation-excellent { 
            border-color: #28a745; 
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        }
        .recommendation-caution { 
            border-color: #ffc107; 
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        }
        .recommendation-not-recommended { 
            border-color: #dc3545; 
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        }
        .score-display { 
            font-size: 42px; 
            font-weight: bold; 
            margin: 15px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .alert-card { 
            border-left: 6px solid #dc3545; 
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            padding: 18px; 
            margin: 12px 0; 
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .alert-warning { 
            border-left-color: #ffc107; 
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        }
        .alert-info { 
            border-left-color: #17a2b8; 
            background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        }
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        .voice-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 50%;
            width: 70px;
            height: 70px;
            color: white;
            font-size: 28px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .voice-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        .voice-button:active {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            transform: scale(0.95);
        }
        .voice-status {
            margin-top: 12px;
            font-style: italic;
            text-align: center;
            font-weight: 500;
        }
        .stSelectbox > div > div { background-color: white; }
        .stTextInput > div > div > input { background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- API FUNCTIONS ---

def get_weather(city: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Fetches current weather data for a city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "en"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_forecast(city: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Fetches the 5-day forecast for a city."""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "en", "cnt": 40}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None

def get_air_quality(lat: float, lon: float, api_key: str) -> Optional[Dict[str, Any]]:
    """Fetches air quality data by coordinates using OpenWeatherMap (fallback)."""
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": api_key}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def get_tempo_air_quality(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetches air quality data (NO2) from NASA's TEMPO satellite."""
    try:
        # Autenticação usando variáveis de ambiente
        # O earthaccess.login() busca automaticamente por EARTHDATA_USERNAME e EARTHDATA_PASSWORD
        earthdata_username = os.getenv('EARTHDATA_USERNAME')
        earthdata_password = os.getenv('EARTHDATA_PASSWORD')
        
        if not earthdata_username or not earthdata_password:
            print("EARTHDATA credentials not found in environment variables.")
            return None
        
        # Fazer login - earthaccess detecta automaticamente as variáveis de ambiente
        auth = earthaccess.login()
        
        # Definir o período de tempo para o dia atual
        today = datetime.utcnow().strftime("%Y-%m-%d")
        date_start = f"{today} 00:00:00"
        date_end = f"{today} 23:59:59"

        # Pesquisar por grânulos de dados de NO2 do TEMPO (Nível 3)
        # short_name = "TEMPO_NO2_L3" # Coleção de NO2
        # version = "V03" # Versão mais recente disponível no tutorial
        
        # Usando TEMPO_NO2_L2 para dados mais brutos e próximos do tempo real, se necessário
        # O tutorial usa L3, mas para qualidade do ar em tempo real, L2 pode ser mais apropriado
        # No entanto, L3 é mais fácil de usar por ser gridded.
        # Vamos usar L3 como no tutorial para simplificar a integração inicial.
        short_name = "TEMPO_NO2_L3"
        version = "V03"

        # Pesquisar dados para a localização e período de tempo
        results = earthaccess.search_data(
            short_name=short_name,
            version=version,
            temporal=(date_start, date_end),
            point=(lon, lat),
            cloud_hosted=True # Priorizar dados hospedados na nuvem para acesso mais rápido
        )

        if not results:
            print("No TEMPO data found for the location and period.")
            return None

        # Baixar o grânulo mais recente (ou o primeiro, para simplificar)
        # O earthaccess.download pode exigir credenciais Earthdata se não estiverem em cache
        # Para evitar interação, vamos tentar abrir diretamente se possível, ou baixar para um temp file
        # Para este exemplo, vamos baixar o primeiro resultado para um diretório temporário
        temp_dir = "/tmp/tempo_data"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Baixar apenas o primeiro arquivo para simplificar
        files = earthaccess.download(results[0:1], local_path=temp_dir)

        if not files:
            print("Failed to download TEMPO data.")
            return None

        file_path = files[0]

        # Ler o arquivo netCDF4
        with nc.Dataset(file_path) as ds:
            prod = ds.groups["product"]
            # NO2 troposférico é um bom indicador de qualidade do ar
            trop_NO2_column = prod.variables["vertical_column_troposphere"][:]
            fv_trop_NO2 = prod.variables["vertical_column_troposphere"].getncattr("_FillValue")
            
            # Obter latitude e longitude para mapeamento
            lats = ds.variables["latitude"][:]
            lons = ds.variables["longitude"][:]

            # Encontrar o pixel mais próximo da localização fornecida
            lat_idx = np.abs(lats - lat).argmin()
            lon_idx = np.abs(lons - lon).argmin()

            # Extrair o valor de NO2 para o pixel mais próximo
            no2_value = trop_NO2_column[0, lat_idx, lon_idx]

            # Tratar valores de preenchimento/inválidos
            if no2_value == fv_trop_NO2 or no2_value < 0:
                print("Invalid or filled NO2 value.")
                return None
            
            # Converter para uma unidade mais comum se necessário, ou usar a unidade original
            # A unidade é molecules/cm^2. Para uma integração simples, podemos retornar este valor.
            # Para converter para µg/m³, seria necessário mais cálculo e massa molar.
            # Para fins de demonstração, vamos retornar o valor bruto e um AQI simplificado.

            # Mapeamento simplificado de NO2 para AQI (exemplo, não cientificamente preciso)
            # Valores de referência (mol/cm^2):
            # Bom: < 5e15
            # Moderado: 5e15 - 10e15
            # Ruim: > 10e15
            
            aqi_tempo = 1 # Bom por padrão
            if no2_value > 10e15:
                aqi_tempo = 4 # Ruim
            elif no2_value > 5e15:
                aqi_tempo = 3 # Moderado
            
            # Retornar um dicionário similar ao da API OpenWeatherMap para facilitar a integração
            return {
                "list": [{
                    "main": {"aqi": aqi_tempo},
                    "components": {"no2": float(no2_value), "o3": 0.0, "pm2_5": 0.0} # Apenas NO2 do TEMPO
                }]
            }

    except Exception as e:
        print(f"Error fetching TEMPO data: {e}")
        return None

# --- CALCULATION AND ANALYSIS FUNCTIONS ---

def calculate_activity_score(weather_data: Dict, air_quality_data: Optional[Dict], activity: str, condition: str) -> Tuple[int, List[str]]:
    """Calculates an activity score based on weather conditions, air quality, and user input."""
    if not weather_data:
        return 0, ["Weather data unavailable."]
    
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    weather_main = weather_data["weather"][0]["main"]
    aqi = air_quality_data["list"][0]["main"]["aqi"] if air_quality_data else 1
    
    score = 100.0
    recommendations = []
    
    # Análise específica por atividade
    if activity == "Running":
        if 15 <= temp <= 25:
            score += 10
        elif 10 <= temp < 15 or 25 < temp <= 30:
            score -= 10
        elif temp < 5 or temp > 35:
            score -= 30
            recommendations.append("Extreme temperature for running")
        
        if humidity > 80:
            score -= 20
            recommendations.append("High humidity can cause discomfort")
        
        if wind_speed > 8:
            score -= 15
            recommendations.append("Strong winds can make running difficult")
    
        elif activity == "Walking":
            if 10 <= temp <= 30:
                score += 5
            elif temp < 0 or temp > 35:
                score -= 20
                recommendations.append("Temperature not ideal for long walks")
    
        elif activity == "Cycling":
            if wind_speed > 10:
                score -= 25
                recommendations.append("Very strong winds for safe cycling")
            elif 5 < wind_speed <= 10:
                score -= 10
            
            if 12 <= temp <= 28:
                score += 8
            elif temp < 5 or temp > 32:
                score -= 25
    
        elif activity == "Outdoor Sports":
            if weather_main in ["Rain", "Thunderstorm", "Snow"]:
                score -= 40
                recommendations.append("Inadequate weather conditions for sports")
            elif weather_main in ["Drizzle", "Mist"]:
                score -= 20
        
        elif activity == "Light Exercises":
            if temp < -5 or temp > 38:
                score -= 15
            if humidity > 90:
                score -= 10
        
        elif activity == "Outdoor Rest":
            if weather_main in ["Thunderstorm"]:
                score -= 30
                recommendations.append("Storms are not safe for outdoor activities")
            elif temp < -10 or temp > 40:
                score -= 10
        
    # Ajustes por condição física
    condition_multipliers = {
        "Excellent": 1.0,
        "Good": 0.9,
        "Moderate": 0.8,
        "Sensitive": 0.6,
        "Delicate": 0.4
    }
    score *= condition_multipliers.get(condition, 0.8)
    
    # Penalidades por qualidade do ar
    if aqi >= 4:
        score -= 40
        recommendations.append("Very poor air quality - avoid outdoor activities")
    elif aqi == 3:
        score -= 20
        recommendations.append("Moderate air quality - sensitive groups should be careful")
    elif aqi >= 2:
        score -= 5
    
    # Penalidades por condições climáticas
    if weather_main == "Thunderstorm":
        score -= 50
        recommendations.append("Storms are dangerous - stay in a safe place")
    elif weather_main == "Rain":
        score -= 25
        recommendations.append("Rain can make activities uncomfortable or dangerous")
    elif weather_main == "Snow":
        score -= 20
        recommendations.append("Snow can make movement difficult")
    
    return int(max(0, min(100, score))), recommendations

def get_recommendation_status(score: int) -> Tuple[str, str, str]:
    """Returns the recommendation status based on the score."""
    if score >= 70:
        return "Recommended", "recommendation-excellent", "✅"
    elif score >= 40:
        return "Caution", "recommendation-caution", "⚠️"
    else:
        return "Not Recommended", "recommendation-not-recommended", "❌"

# --- SPEECH SYNTHESIS FUNCTIONS ---

def generate_comprehensive_speech_summary(weather_data: Dict, air_quality_data: Optional[Dict], 
                                        score: int, recommendations: List[str], 
                                        activity: str, condition: str, forecast_data: Optional[Dict] = None) -> str:
    """Generates a comprehensive and detailed summary for speech synthesis."""
    if not weather_data:
        return "Could not retrieve weather data."

    city = weather_data["name"]
    country = weather_data["sys"]["country"]
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    description = weather_data["weather"][0]["description"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    pressure = weather_data["main"]["pressure"]
    
    # Informações de nascer e pôr do sol
    sunrise = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%H:%M")
    
    summary = f"Complete weather summary for {city}, {country}. "
    summary += f"The current temperature is {temp:.0f} degrees Celsius, with a feels like temperature of {feels_like:.0f} degrees. "
    summary += f"The sky is {description}. "
    summary += f"The humidity is {humidity} percent. "
    summary += f"The wind speed is {wind_speed:.1f} meters per second. "
    summary += f"The atmospheric pressure is {pressure} hectopascals. "
    summary += f"Sunrise was at {sunrise} and sunset will be at {sunset}. "

    # Informações de qualidade do ar
    if air_quality_data:
        aqi = air_quality_data["list"][0]["main"]["aqi"]
        aqi_levels = {1: "good", 2: "fair", 3: "moderate", 4: "poor", 5: "very poor"}
        summary += f"The air quality is {aqi_levels.get(aqi, 'unknown')}. "
        
        components = air_quality_data["list"][0]["components"]
        summary += f"Pollutant levels are: PM 2.5 at {components['pm2_5']} micrograms per cubic meter, "
        summary += f"ozone at {components['o3']} micrograms per cubic meter. "

    # Previsão para as próximas horas
    if forecast_data and forecast_data.get("list"):
        next_forecast = forecast_data["list"][0]
        next_time = datetime.fromtimestamp(next_forecast["dt"]).strftime("%H:%M")
        next_temp = next_forecast["main"]["temp"]
        summary += f"For the next few hours, at {next_time}, the temperature will be {next_temp:.0f} degrees. "

    # Recomendação para atividade
    status, _, _ = get_recommendation_status(score)
    summary += f"The recommendation for {activity}, considering your physical condition as {condition}, is: {status}, with a score of {score} out of 100 points. "

    # Specific guidance
    if recommendations:
        summary += "Specific guidance: " + ". ".join(recommendations) + ". "
    
    # General tips based on conditions
    if temp > 30:
        summary += "Remember to stay hydrated and use sunscreen. "
    elif temp < 10:
        summary += "Wear appropriate clothing for the cold. "
    
    if humidity > 80:
        summary += "High humidity can cause discomfort, drink plenty of water. "
    
    if wind_speed > 10:
        summary += "Beware of strong winds, avoid areas with tall trees. "

    summary += "Have a great day and practice your activities safely!"
    
    return summary

def extract_city_from_transcript(text: str) -> Optional[str]:
    """Extracts the city name from a voice transcript more robustly."""
    text = text.lower().strip()
    
    # Remove palavras comuns e conectores
    stop_words = ["weather", "forecast", "in", "for", "of", "the", "how", "is", "a"]
    
    # Look for specific triggers
    triggers = ["in ", "for "]
    for trigger in triggers:
        if trigger in text:
            parts = text.split(trigger)
            if len(parts) > 1:
                city = parts[-1].strip()
                # Remove pontuação e palavras de parada
                city = city.replace("?", "").replace(".", "").replace(",", "")
                words = city.split()
                filtered_words = [word for word in words if word not in stop_words]
                if filtered_words:
                    return " ".join(filtered_words).title()
    
    # Se não encontrar gatilhos, processa a transcrição inteira
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    if filtered_words:
        city = " ".join(filtered_words).replace("?", "").replace(".", "").replace(",", "")
        return city.title() if city else None
    
    return None

# --- COMPONENTES DE INTERFACE ---

def voice_assistant_component(text_to_speak: Optional[str] = None):
    """Creates the advanced voice assistant component with speech synthesis."""
    speak_script = ""
    if text_to_speak:
        # Sanitiza o texto para JavaScript
        sanitized_text = text_to_speak.replace("\"", "\\\"").replace("\"", "\\\"").replace("\n", " ")
        speak_script = f"""
            if (\'speechSynthesis\' in window) {{
                // Cancela qualquer fala anterior
                window.speechSynthesis.cancel();
                
                // Cria nova utterance
                const utterance = new SpeechSynthesisUtterance("{sanitized_text}");
                                utterance.lang = \'en-US\';
                utterance.rate = 0.9;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                // Eventos da síntese de voz
                utterance.onstart = function() {{
                    document.getElementById(\'speakStatus\').textContent = \'🔊 Speaking...\';
                }};
                
                utterance.onend = function() {{
                                        document.getElementById(\'speakStatus\').textContent = \'✅ Speech Finished\';
                    setTimeout(() => {{
                        document.getElementById(\'speakStatus\').textContent = \'\';
                    }}, 2000);
                }};
                
                utterance.onerror = function(e) {{
                    console.error(\'Speech synthesis error:\', e);
                    document.getElementById(\'speakStatus\').textContent = \'❌ Speech Error\';
                }};
                
                window.speechSynthesis.speak(utterance);
            }} else {{
                console.warn(\'Speech Synthesis API not supported in this browser.\');
                document.getElementById(\'speakStatus\').textContent = \'Speech API Not Supported\';
            }}
        """

    # JavaScript para reconhecimento de voz
    # Este script será movido para recognition.js e modificado para incluir o recarregamento da página
    # Carrega o script de reconhecimento de voz externo
    with open("recognition.js", "r") as f:
        recognition_script = f.read()


    components.html(
        f"""
        <button id="voiceButton" class="voice-button">🎙️</button>
        <div id="voiceStatus" class="voice-status"></div>
        <div id="speakStatus" class="voice-status"></div>
        <script>
            {recognition_script}
            {speak_script}
        </script>
        """,
        height=150,
        scrolling=False
    )


def display_air_quality_section(air_quality_data: Optional[Dict], city: str):
    """Displays comprehensive air quality information with WHO guidelines at the top of the page."""
    if not air_quality_data:
        return
    
    st.markdown("---")
    st.header("🌬️ Air Quality Index")
    st.markdown(f"**Current air quality conditions for {city}**")
    
    aqi = air_quality_data['list'][0]['main']['aqi']
    aqi_levels = {
        1: ("Good", "🟢", "#28a745"),
        2: ("Fair", "🟡", "#ffc107"),
        3: ("Moderate", "🟠", "#fd7e14"),
        4: ("Poor", "🔴", "#dc3545"),
        5: ("Very Poor", "🟣", "#6f42c1")
    }
    aqi_description, aqi_emoji, aqi_color = aqi_levels.get(aqi, ("Unknown", "⚪", "#6c757d"))
    
    # Display main AQI card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {aqi_color}22 0%, {aqi_color}44 100%); 
                border-left: 6px solid {aqi_color}; 
                border-radius: 10px; 
                padding: 20px; 
                margin-bottom: 20px;">
        <h2 style="margin: 0; color: {aqi_color};">{aqi_emoji} {aqi_description}</h2>
        <p style="margin: 5px 0 0 0; font-size: 1.1em;">Air Quality Index: {aqi}/5</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Health recommendations based on AQI
    health_recommendations = {
        1: "Air quality is satisfactory, and air pollution poses little or no risk.",
        2: "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.",
        3: "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
        4: "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.",
        5: "Health alert: The risk of health effects is increased for everyone."
    }
    
    st.info(f"**Health Advisory:** {health_recommendations.get(aqi, 'No information available.')}")
    
    # Display pollutant levels with WHO guidelines
    st.subheader("Pollutant Levels & WHO Guidelines")
    
    components_data = air_quality_data['list'][0]['components']
    
    # WHO Air Quality Guidelines (2021)
    who_guidelines = {
        'pm2_5': {'annual': 5, 'daily': 15, 'unit': 'µg/m³', 'name': 'PM2.5'},
        'pm10': {'annual': 15, 'daily': 45, 'unit': 'µg/m³', 'name': 'PM10'},
        'no2': {'annual': 10, 'daily': 25, 'unit': 'µg/m³', 'name': 'NO₂'},
        'o3': {'peak_season': 60, 'daily': 100, 'unit': 'µg/m³', 'name': 'O₃'},
        'co': {'daily': 4000, 'unit': 'µg/m³', 'name': 'CO'},
        'so2': {'daily': 40, 'unit': 'µg/m³', 'name': 'SO₂'}
    }
    
    # Create columns for pollutants
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pm25 = components_data.get('pm2_5', 0)
        pm25_status = "✅ Good" if pm25 <= 15 else "⚠️ Exceeds WHO guideline"
        st.metric("PM2.5 (Fine Particles)", f"{pm25:.1f} µg/m³", delta=None)
        st.caption(f"WHO 24h guideline: ≤15 µg/m³")
        st.caption(pm25_status)
        
        no2 = components_data.get('no2', 0)
        no2_status = "✅ Good" if no2 <= 25 else "⚠️ Exceeds WHO guideline"
        st.metric("NO₂ (Nitrogen Dioxide)", f"{no2:.1f} µg/m³", delta=None)
        st.caption(f"WHO 24h guideline: ≤25 µg/m³")
        st.caption(no2_status)
    
    with col2:
        pm10 = components_data.get('pm10', 0)
        pm10_status = "✅ Good" if pm10 <= 45 else "⚠️ Exceeds WHO guideline"
        st.metric("PM10 (Coarse Particles)", f"{pm10:.1f} µg/m³", delta=None)
        st.caption(f"WHO 24h guideline: ≤45 µg/m³")
        st.caption(pm10_status)
        
        so2 = components_data.get('so2', 0)
        so2_status = "✅ Good" if so2 <= 40 else "⚠️ Exceeds WHO guideline"
        st.metric("SO₂ (Sulfur Dioxide)", f"{so2:.1f} µg/m³", delta=None)
        st.caption(f"WHO 24h guideline: ≤40 µg/m³")
        st.caption(so2_status)
    
    with col3:
        o3 = components_data.get('o3', 0)
        o3_status = "✅ Good" if o3 <= 100 else "⚠️ Exceeds WHO guideline"
        st.metric("O₃ (Ozone)", f"{o3:.1f} µg/m³", delta=None)
        st.caption(f"WHO 8h guideline: ≤100 µg/m³")
        st.caption(o3_status)
        
        co = components_data.get('co', 0)
        co_status = "✅ Good" if co <= 4000 else "⚠️ Exceeds WHO guideline"
        st.metric("CO (Carbon Monoxide)", f"{co:.1f} µg/m³", delta=None)
        st.caption(f"WHO 24h guideline: ≤4000 µg/m³")
        st.caption(co_status)
    
    # Additional pollutants if available
    if 'nh3' in components_data:
        st.metric("NH₃ (Ammonia)", f"{components_data['nh3']:.1f} µg/m³")
    
    # Pollutant information
    with st.expander("ℹ️ Learn about air pollutants"):
        st.markdown("""
        **PM2.5 (Fine Particulate Matter):** Particles with diameter ≤2.5 micrometers. Can penetrate deep into lungs and bloodstream.
        
        **PM10 (Coarse Particulate Matter):** Particles with diameter ≤10 micrometers. Can irritate airways and worsen respiratory conditions.
        
        **NO₂ (Nitrogen Dioxide):** Gas produced by combustion. Can inflame airways and reduce immunity to lung infections.
        
        **O₃ (Ozone):** Ground-level ozone formed by chemical reactions. Can cause breathing problems and trigger asthma.
        
        **CO (Carbon Monoxide):** Odorless gas from incomplete combustion. Reduces oxygen delivery to body organs.
        
        **SO₂ (Sulfur Dioxide):** Gas from burning fossil fuels. Can affect respiratory system and lung function.
        
        *Guidelines based on WHO Global Air Quality Guidelines 2021*
        """)
    
    st.markdown("---")

def display_recommendation_card(score: int, recommendations: List[str], activity: str, condition: str):
    """Displays the main recommendation card."""
    status, css_class, emoji = get_recommendation_status(score)
    
    st.markdown(f"""
    <div class="recommendation-card {css_class}">
        <h3>{emoji} Recommendation for {activity}</h3>
        <div class="score-display">{score}/100</div>
        <h4>{status}</h4>
        <p><strong>Physical condition:</strong> {condition}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if recommendations:
        with st.expander("**📋 View Specific Guidance**", expanded=True):
            for i, rec in enumerate(recommendations, 1):
                st.warning(f"**{i}.** {rec}")

def show_notifications(weather_data: Dict, air_quality_data: Optional[Dict]):
    """Displays alert notifications at the top of the page."""
    alerts = []
    
    if air_quality_data and air_quality_data["list"][0]["main"]["aqi"] >= 4:
        alerts.append("🚨 **Air Quality Alert**: Air quality is very poor. Avoid outdoor activities.")
    
    if weather_data and weather_data["weather"][0]["main"] == "Thunderstorm":
        alerts.append("⛈️ **Storm Alert**: Dangerous conditions. Seek shelter immediately.")
    
    temp = weather_data["main"]["temp"] if weather_data else 0
    if temp > 35:
        alerts.append("🔥 **Extreme Heat Alert**: Very high temperature. Avoid prolonged sun exposure.")
    elif temp < -5:
        alerts.append("🥶 **Extreme Cold Alert**: Very low temperature. Wear appropriate clothing.")
    
    wind_speed = weather_data["wind"]["speed"] if weather_data else 0
    if wind_speed > 12:
        alerts.append("💨 **Strong Wind Alert**: Beware of loose objects and avoid areas with trees.")
    
    for alert in alerts:
        st.error(alert)

def display_alerts_panel(weather_data: Dict, air_quality_data: Optional[Dict]):
    """Displays a detailed safety alerts panel."""
    alerts = []

    if air_quality_data and air_quality_data["list"][0]["main"]["aqi"] >= 4:
        alerts.append({
            "type": "danger",
            "icon": "😷",
            "title": "Very Poor Air Quality",
            "message": "Avoid outdoor physical activities. Sensitive groups should remain indoors."
        })
    elif air_quality_data and air_quality_data["list"][0]["main"]["aqi"] == 3:
        alerts.append({
            "type": "warning",
            "icon": "😟",
            "title": "Moderate Air Quality",
            "message": "Sensitive groups (children, elderly, people with respiratory diseases) should reduce outdoor activities."
        })

    if weather_data:
        weather_main = weather_data["weather"][0]["main"]
        temp = weather_data["main"]["temp"]
        wind_speed = weather_data["wind"]["speed"]

        if weather_main == "Thunderstorm":
            alerts.append({
                "type": "danger",
                "icon": "⛈️",
            "title": "Thunderstorm",
            "message": "Seek shelter immediately. Risk of lightning and strong winds."
            })
        elif weather_main == "Rain":
            alerts.append({
                "type": "info",
                "icon": "🌧️",
            "title": "Rain",
            "message": "Take an umbrella. Surfaces may be slippery."
            })
        elif weather_main == "Snow":
            alerts.append({
                "type": "info",
                "icon": "❄️",
            "title": "Snow",
            "message": "Dress appropriately. Beware of slippery roads."
            })

        if temp > 35:
            alerts.append({
                "type": "danger",
                "icon": "🥵",
            "title": "Extreme Heat",
            "message": "Stay hydrated and avoid prolonged sun exposure. Risk of heatstroke."
            })
        elif temp < 0:
            alerts.append({
                "type": "warning",
                "icon": "🥶",
            "title": "Intense Cold",
            "message": "Wear layers of clothing. Risk of hypothermia in prolonged exposures."
            })

        if wind_speed > 15:
            alerts.append({
                "type": "warning",
                "icon": "💨",
            "title": "Strong Winds",
            "message": "Beware of flying objects and tree branches. Avoid wooded areas."
            })

    if alerts:
        st.subheader("🚨 Safety Alerts")
        for alert in alerts:
            css_class = f"alert-{alert['type']}" if alert['type'] != 'danger' else 'alert-card'
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{alert['icon']} {alert['title']}</strong><br>
                {alert['message']}
            </div>
            """, unsafe_allow_html=True)

def display_weather(weather_data, forecast_data=None):
    """Displays detailed weather information."""
    if not weather_data:
        return

    city = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    description = weather_data['weather'][0]['description']
    icon = weather_data['weather'][0]['icon']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    pressure = weather_data['main']['pressure']
    visibility = weather_data.get('visibility')

    st.markdown(f"""
    <div class="weather-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>{city}, {country}</h2>
                <p style="font-size: 1.2em;">{description.capitalize()}</p>
            </div>
            <div style="text-align: right;">
                <img src="http://openweathermap.org/img/wn/{icon}@2x.png" width="100">
                <div class="temperature">{temp:.0f}°C</div>
                <p>Feels like: {feels_like:.0f}°C</p>
            </div>
        </div>
        <hr style="border-top: 1px solid rgba(255,255,255,0.5); margin: 15px 0;">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>💧 Humidity: {humidity}%</div>
            <div>💨 Wind: {wind_speed:.1f} m/s</div>
            <div> barometer Pressure: {pressure} hPa</div>
            {f"<div>👁️ Visibility: {visibility / 1000:.1f} km</div>" if visibility else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Exibir previsão de 5 dias
    if forecast_data and forecast_data.get('list'):
        st.subheader("Next Days Forecast")
        forecast_df = pd.DataFrame(forecast_data['list'])
        forecast_df['dt_txt'] = pd.to_datetime(forecast_df['dt_txt'])
        forecast_df['date'] = forecast_df['dt_txt'].dt.date

        # Agrupar por dia e pegar a previsão do meio do dia (ex: 12:00 ou mais próximo)
        daily_forecasts = []
        for date, group in forecast_df.groupby('date'):
            # Tenta pegar a previsão das 12:00, senão pega a mais próxima
            noon_forecast = group.iloc[(group['dt_txt'].dt.hour - 12).abs().argsort()[:1]]
            daily_forecasts.append(noon_forecast.iloc[0])
        
        # Limitar a 5 dias
        daily_forecasts = daily_forecasts[:5]

        cols = st.columns(len(daily_forecasts))
        for i, forecast in enumerate(daily_forecasts):
            with cols[i]:
                date_str = forecast['dt_txt'].strftime('%d/%m')
                temp_max = forecast['main']['temp_max']
                temp_min = forecast['main']['temp_min']
                description = forecast['weather'][0]['description']
                icon = forecast['weather'][0]['icon']
                
                st.markdown(f"""
                <div class="forecast-card">
                    <h5>{date_str}</h5>
                    <img src="http://openweathermap.org/img/wn/{icon}.png" width="50">
                    <p><strong>{temp_max:.0f}°C</strong> / {temp_min:.0f}°C</p>
                    <p>{description.capitalize()}</p>
                </div>
                """, unsafe_allow_html=True)



def display_world_map():
    """Displays an interactive world map based on user or default location."""
    st.subheader("Explore Global Weather")
    st.write("Use the sidebar to search for weather in a specific city.")

    # Coordenadas padrão (ex: centro do Brasil)
    default_lat, default_lon = -14.235, -53.132

    # Criar um DataFrame para o mapa (pode ser expandido com mais cidades)
    map_data = pd.DataFrame({
        'lat': [default_lat],
        'lon': [default_lon]
    })

    st.map(map_data, zoom=3)

# --- MAIN FUNCTION ---

def main():
    setup_page_config()
    load_custom_css()

    # Inicializa o estado da sessão para a cidade se não existir
    if 'city' not in st.session_state:
        st.session_state.city = ""
    if 'speech_summary' not in st.session_state:
        st.session_state.speech_summary = None

    # Chave da API do OpenWeatherMap
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        st.error("Please set the OPENWEATHER_API_KEY environment variable with your OpenWeatherMap API key.")
        st.stop()

    # Credenciais da NASA Earthdata para earthaccess
    # Para usar a API TEMPO da NASA, você precisa de uma conta Earthdata e configurar suas credenciais.
    # Visite https://urs.earthdata.nasa.gov/users/new para criar uma conta.
    # As credenciais devem ser configuradas via variáveis de ambiente EARTHDATA_USERNAME e EARTHDATA_PASSWORD
    earthdata_username = os.getenv('EARTHDATA_USERNAME')
    earthdata_password = os.getenv('EARTHDATA_PASSWORD')
    
    if not earthdata_username or not earthdata_password:
        st.warning("NASA Earthdata credentials not found. TEMPO air quality data will not be available. Please set EARTHDATA_USERNAME and EARTHDATA_PASSWORD environment variables.")
        st.info("You can create a free account at https://urs.earthdata.nasa.gov/users/new")


    st.sidebar.header("🌍 Weather Settings")

    with st.sidebar:
        st.header("🏙️ City Selection")
        city_input = st.text_input(
            "Enter city name:",
            placeholder="E.g., New York, Los Angeles, Chicago",
            key="city_input_sidebar"
        )

        if st.button("Search Weather", key="search_button"):
            st.session_state.city = city_input
            st.rerun()

        st.markdown("---")

        # Componente de assistente de voz
        st.header("🎙️ Voice Assistant")
        voice_assistant_component(st.session_state.get("speech_summary", None))

        # Captura a entrada de voz do componente JS

        if "voice_input_hidden" in st.session_state:
            voice_input = st.session_state.voice_input_hidden
            recognized_city = extract_city_from_transcript(voice_input)
            if recognized_city:
                st.session_state.city = recognized_city
                st.rerun()
            else:
                st.sidebar.warning("Could not recognize a city in your speech.")

        st.markdown("---")

        # Seleção de atividade
        st.header("🏃‍♂️ Your Activity")
        activity = st.selectbox(
            "What activity do you plan to do?",
            ["Running", "Walking", "Cycling", "Outdoor Sports", "Light Exercises", "Outdoor Rest"],
            key="activity_selector",
            help="Select the activity you plan to do"
        )

        st.markdown("---")

        # Seleção de condição física
        st.header("💪 Physical Condition")
        condition = st.selectbox(
            "How is your physical condition?",
            ["Excellent", "Good", "Moderate", "Sensitive", "Delicate"],
            key="condition_selector",
            help="Your physical condition influences safety recommendations"
        )

        st.markdown("---")
        st.markdown("""
        **Condition Legend:**
        - **Excellent**: Athletic, no limitations
        - **Good**: Exercises regularly
        - **Moderate**: Occasionally active
        - **Sensitive**: Mild respiratory/cardiac issues
        - **Delicate**: Health conditions requiring care
        """)

    # Área de conteúdo principal
    if st.session_state.city:
        city_to_display = st.session_state.city
        # Busca dados do tempo
        with st.spinner(f"Fetching weather data for {city_to_display}..."):
            weather_data = get_weather(city_to_display, api_key)
            forecast_data = None
            air_quality_data = None

            if weather_data:
                # Obtém dados adicionais
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']

                forecast_data = get_forecast(city_to_display, api_key)
                # Tentar obter dados de qualidade do ar da API TEMPO da NASA
                air_quality_data = get_tempo_air_quality(lat, lon)
                
                # Se a API TEMPO não retornar dados, usar a API OpenWeatherMap como fallback
                if not air_quality_data:
                    air_quality_data = get_air_quality(lat, lon, api_key)


                # Display Air Quality Section FIRST (top of the page)
                display_air_quality_section(air_quality_data, city_to_display)

                # Calcula o score da atividade e mostra a recomendação
                score, recommendations = calculate_activity_score(
                    weather_data, air_quality_data, activity, condition
                )

                # Exibe o cartão de recomendação
                display_recommendation_card(score, recommendations, activity, condition)

                # Gera o resumo de voz completo
                speech_summary = generate_comprehensive_speech_summary(
                    weather_data, air_quality_data, score, recommendations, activity, condition, forecast_data
                )
                # Renderiza o componente de assistente de voz com o texto para falar
                # O componente de voz agora é chamado no sidebar, então apenas atualizamos o estado da sessão
                st.session_state.speech_summary = speech_summary

                # Exibe informações detalhadas do tempo
                display_weather(weather_data, forecast_data)
            else:
                st.error(
                    f"Não foi possível encontrar dados para a cidade '{city_to_display}'. Verifique o nome e tente novamente.")
                # Limpa a cidade do estado da sessão se não for encontrada
                st.session_state.city = ""
    else:
        # Exibe o mapa mundial quando nenhuma cidade é selecionada
        display_world_map()

if __name__ == "__main__":
    main()