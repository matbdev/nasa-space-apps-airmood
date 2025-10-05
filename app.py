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

# --- CONFIGURAÇÃO DA PÁGINA ---

def setup_page_config():
    """Configura as propriedades da página Streamlit."""
    st.set_page_config(
        page_title="Previsão do Tempo Avançada com Assistente de Voz",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    """Carrega o CSS customizado para a aplicação."""
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

# --- FUNÇÕES DE API ---

def get_weather(city: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Busca os dados do tempo atual para uma cidade."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "pt_br"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do tempo: {e}")
        return None

def get_forecast(city: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Busca a previsão de 5 dias para uma cidade."""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "pt_br", "cnt": 40}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados da previsão: {e}")
        return None

def get_air_quality(lat: float, lon: float, api_key: str) -> Optional[Dict[str, Any]]:
    """Busca dados da qualidade do ar por coordenadas."""
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": api_key}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

# --- FUNÇÕES DE CÁLCULO E ANÁLISE ---

def calculate_activity_score(weather_data: Dict, air_quality_data: Optional[Dict], activity: str, condition: str) -> Tuple[int, List[str]]:
    """Calcula um score para a atividade selecionada com base nas condições."""
    if not weather_data:
        return 0, ["Dados do tempo indisponíveis."]
    
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    weather_main = weather_data["weather"][0]["main"]
    aqi = air_quality_data["list"][0]["main"]["aqi"] if air_quality_data else 1
    
    score = 100.0
    recommendations = []
    
    # Análise específica por atividade
    if activity == "Corrida":
        if 15 <= temp <= 25:
            score += 10
        elif 10 <= temp < 15 or 25 < temp <= 30:
            score -= 10
        elif temp < 5 or temp > 35:
            score -= 30
            recommendations.append("Temperatura extrema para corrida")
        
        if humidity > 80:
            score -= 20
            recommendations.append("Umidade alta pode causar desconforto")
        
        if wind_speed > 8:
            score -= 15
            recommendations.append("Ventos fortes podem dificultar a corrida")
    
    elif activity == "Caminhada":
        if 10 <= temp <= 30:
            score += 5
        elif temp < 0 or temp > 35:
            score -= 20
            recommendations.append("Temperatura não ideal para caminhadas longas")
    
    elif activity == "Ciclismo":
        if wind_speed > 10:
            score -= 25
            recommendations.append("Ventos muito fortes para ciclismo seguro")
        elif 5 < wind_speed <= 10:
            score -= 10
        
        if 12 <= temp <= 28:
            score += 8
        elif temp < 5 or temp > 32:
            score -= 25
    
    elif activity == "Esportes ao ar livre":
        if weather_main in ["Rain", "Thunderstorm", "Snow"]:
            score -= 40
            recommendations.append("Condições climáticas inadequadas para esportes")
        elif weather_main in ["Drizzle", "Mist"]:
            score -= 20
    
    elif activity == "Exercícios leves":
        if temp < -5 or temp > 38:
            score -= 15
        if humidity > 90:
            score -= 10
    
    elif activity == "Descanso ao ar livre":
        if weather_main in ["Thunderstorm"]:
            score -= 30
            recommendations.append("Tempestades não são seguras para atividades externas")
        elif temp < -10 or temp > 40:
            score -= 10
    
    # Ajustes por condição física
    condition_multipliers = {
        "Excelente": 1.0,
        "Boa": 0.9,
        "Moderada": 0.8,
        "Sensível": 0.6,
        "Delicada": 0.4
    }
    score *= condition_multipliers.get(condition, 0.8)
    
    # Penalidades por qualidade do ar
    if aqi >= 4:
        score -= 40
        recommendations.append("Qualidade do ar muito ruim - evite atividades externas")
    elif aqi == 3:
        score -= 20
        recommendations.append("Qualidade do ar moderada - grupos sensíveis devem ter cuidado")
    elif aqi >= 2:
        score -= 5
    
    # Penalidades por condições climáticas
    if weather_main == "Thunderstorm":
        score -= 50
        recommendations.append("Tempestades são perigosas - fique em local seguro")
    elif weather_main == "Rain":
        score -= 25
        recommendations.append("Chuva pode tornar atividades desconfortáveis ou perigosas")
    elif weather_main == "Snow":
        score -= 20
        recommendations.append("Neve pode dificultar movimentação")
    
    return int(max(0, min(100, score))), recommendations

def get_recommendation_status(score: int) -> Tuple[str, str, str]:
    """Retorna o status da recomendação com base no score."""
    if score >= 70:
        return "Recomendado", "recommendation-excellent", "✅"
    elif score >= 40:
        return "Cautela", "recommendation-caution", "⚠️"
    else:
        return "Não Recomendado", "recommendation-not-recommended", "❌"

# --- FUNÇÕES DE SÍNTESE DE VOZ ---

def generate_comprehensive_speech_summary(weather_data: Dict, air_quality_data: Optional[Dict], 
                                        score: int, recommendations: List[str], 
                                        activity: str, condition: str, forecast_data: Optional[Dict] = None) -> str:
    """Gera um resumo completo e detalhado para síntese de voz."""
    if not weather_data:
        return "Não foi possível obter os dados do tempo."

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
    
    summary = f"Resumo completo do tempo para {city}, {country}. "
    summary += f"A temperatura atual é de {temp:.0f} graus Celsius, com sensação térmica de {feels_like:.0f} graus. "
    summary += f"O céu está com {description}. "
    summary += f"A umidade do ar é de {humidity} por cento. "
    summary += f"O vento está a {wind_speed:.1f} metros por segundo. "
    summary += f"A pressão atmosférica é de {pressure} hectopascais. "
    summary += f"O nascer do sol foi às {sunrise} e o pôr do sol será às {sunset}. "

    # Informações de qualidade do ar
    if air_quality_data:
        aqi = air_quality_data["list"][0]["main"]["aqi"]
        aqi_levels = {1: "boa", 2: "razoável", 3: "moderada", 4: "ruim", 5: "muito ruim"}
        summary += f"A qualidade do ar está {aqi_levels.get(aqi, 'desconhecida')}. "
        
        components = air_quality_data["list"][0]["components"]
        summary += f"Os níveis de poluentes são: PM 2.5 com {components['pm2_5']} microgramas por metro cúbico, "
        summary += f"ozônio com {components['o3']} microgramas por metro cúbico. "

    # Previsão para as próximas horas
    if forecast_data and forecast_data.get("list"):
        next_forecast = forecast_data["list"][0]
        next_time = datetime.fromtimestamp(next_forecast["dt"]).strftime("%H:%M")
        next_temp = next_forecast["main"]["temp"]
        summary += f"Para as próximas horas, às {next_time}, a temperatura será de {next_temp:.0f} graus. "

    # Recomendação para atividade
    status, _, _ = get_recommendation_status(score)
    summary += f"A recomendação para a atividade de {activity}, considerando sua condição física como {condition}, é: {status}, com uma pontuação de {score} de 100 pontos. "

    # Orientações específicas
    if recommendations:
        summary += "Orientações específicas: " + ". ".join(recommendations) + ". "
    
    # Dicas gerais baseadas nas condições
    if temp > 30:
        summary += "Lembre-se de se manter hidratado e usar protetor solar. "
    elif temp < 10:
        summary += "Vista roupas adequadas para o frio. "
    
    if humidity > 80:
        summary += "A alta umidade pode causar desconforto, beba bastante água. "
    
    if wind_speed > 10:
        summary += "Cuidado com ventos fortes, evite áreas com árvores altas. "

    summary += "Tenha um ótimo dia e pratique suas atividades com segurança!"
    
    return summary

def extract_city_from_transcript(text: str) -> Optional[str]:
    """Extrai o nome da cidade de uma transcrição de voz de forma mais robusta."""
    text = text.lower().strip()
    
    # Remove palavras comuns e conectores
    stop_words = ["tempo", "clima", "previsão", "em", "para", "de", "da", "do", "na", "no", "como", "está", "o"]
    
    # Procura por gatilhos específicos
    triggers = ["em ", "para ", "de ", "da ", "do ", "na ", "no "]
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
    """Cria o componente avançado de assistente de voz com síntese de fala."""
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
                utterance.lang = \'pt-BR\';
                utterance.rate = 0.9;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                // Eventos da síntese de voz
                utterance.onstart = function() {{
                    document.getElementById(\'speakStatus\').textContent = \'🔊 Falando...\';
                }};
                
                utterance.onend = function() {{
                    document.getElementById(\'speakStatus\').textContent = \'✅ Concluído\';
                    setTimeout(() => {{
                        document.getElementById(\'speakStatus\').textContent = \'\';
                    }}, 2000);
                }};
                
                utterance.onerror = function(e) {{
                    console.error(\'Erro na síntese de voz:\', e);
                    document.getElementById(\'speakStatus\').textContent = \'❌ Erro na fala\';
                }};
                
                window.speechSynthesis.speak(utterance);
            }} else {{
                console.warn(\'Speech Synthesis API não suportada neste navegador.\');
                document.getElementById(\'speakStatus\').textContent = \'API de Fala não suportada\';
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


def display_recommendation_card(score: int, recommendations: List[str], activity: str, condition: str):
    """Exibe o cartão de recomendação principal."""
    status, css_class, emoji = get_recommendation_status(score)
    
    st.markdown(f"""
    <div class="recommendation-card {css_class}">
        <h3>{emoji} Recomendação para {activity}</h3>
        <div class="score-display">{score}/100</div>
        <h4>{status}</h4>
        <p><strong>Condição física:</strong> {condition}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if recommendations:
        with st.expander("**📋 Ver Orientações Específicas**", expanded=True):
            for i, rec in enumerate(recommendations, 1):
                st.warning(f"**{i}.** {rec}")

def show_notifications(weather_data: Dict, air_quality_data: Optional[Dict]):
    """Exibe notificações de alerta no topo da página."""
    alerts = []
    
    if air_quality_data and air_quality_data["list"][0]["main"]["aqi"] >= 4:
        alerts.append("🚨 **Alerta de Qualidade do Ar**: A qualidade do ar está muito ruim. Evite atividades externas.")
    
    if weather_data and weather_data["weather"][0]["main"] == "Thunderstorm":
        alerts.append("⛈️ **Alerta de Tempestade**: Condições perigosas. Procure abrigo imediatamente.")
    
    temp = weather_data["main"]["temp"] if weather_data else 0
    if temp > 35:
        alerts.append("🔥 **Alerta de Calor Extremo**: Temperatura muito alta. Evite exposição prolongada ao sol.")
    elif temp < -5:
        alerts.append("🥶 **Alerta de Frio Extremo**: Temperatura muito baixa. Use roupas adequadas.")
    
    wind_speed = weather_data["wind"]["speed"] if weather_data else 0
    if wind_speed > 12:
        alerts.append("💨 **Alerta de Ventos Fortes**: Cuidado com objetos soltos e evite áreas com árvores.")
    
    for alert in alerts:
        st.error(alert)

def display_alerts_panel(weather_data: Dict, air_quality_data: Optional[Dict]):
    """Exibe painel detalhado de alertas de segurança."""
    alerts = []

    if air_quality_data and air_quality_data["list"][0]["main"]["aqi"] >= 4:
        alerts.append({
            "type": "danger",
            "icon": "😷",
            "title": "Qualidade do Ar Muito Ruim",
            "message": "Evite atividades físicas ao ar livre. Grupos sensíveis devem permanecer em ambientes fechados."
        })
    elif air_quality_data and air_quality_data["list"][0]["main"]["aqi"] == 3:
        alerts.append({
            "type": "warning",
            "icon": "😟",
            "title": "Qualidade do Ar Moderada",
            "message": "Grupos sensíveis (crianças, idosos, pessoas com doenças respiratórias) devem reduzir atividades ao ar livre."
        })

    if weather_data:
        weather_main = weather_data["weather"][0]["main"]
        temp = weather_data["main"]["temp"]
        wind_speed = weather_data["wind"]["speed"]

        if weather_main == "Thunderstorm":
            alerts.append({
                "type": "danger",
                "icon": "⛈️",
                "title": "Tempestade",
                "message": "Procure abrigo imediatamente. Risco de raios e ventos fortes."
            })
        elif weather_main == "Rain":
            alerts.append({
                "type": "info",
                "icon": "🌧️",
                "title": "Chuva",
                "message": "Leve um guarda-chuva. Superfícies podem estar escorregadias."
            })
        elif weather_main == "Snow":
            alerts.append({
                "type": "info",
                "icon": "❄️",
                "title": "Neve",
                "message": "Vista-se adequadamente. Cuidado com estradas escorregadias."
            })

        if temp > 35:
            alerts.append({
                "type": "danger",
                "icon": "🥵",
                "title": "Calor Extremo",
                "message": "Mantenha-se hidratado e evite exposição prolongada ao sol. Risco de insolação."
            })
        elif temp < 0:
            alerts.append({
                "type": "warning",
                "icon": "🥶",
                "title": "Frio Intenso",
                "message": "Vista camadas de roupa. Risco de hipotermia em exposições prolongadas."
            })

        if wind_speed > 15:
            alerts.append({
                "type": "warning",
                "icon": "💨",
                "title": "Ventos Fortes",
                "message": "Cuidado com objetos voadores e galhos de árvores. Evite áreas arborizadas."
            })

    if alerts:
        st.subheader("🚨 Alertas de Segurança")
        for alert in alerts:
            css_class = f"alert-{alert['type']}" if alert['type'] != 'danger' else 'alert-card'
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{alert['icon']} {alert['title']}</strong><br>
                {alert['message']}
            </div>
            """, unsafe_allow_html=True)

def display_weather(weather_data, forecast_data=None, air_quality_data=None):
    """Display detailed weather information"""
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
                <p>Sensação térmica: {feels_like:.0f}°C</p>
            </div>
        </div>
        <hr style="border-top: 1px solid rgba(255,255,255,0.5); margin: 15px 0;">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>💧 Umidade: {humidity}%</div>
            <div>💨 Vento: {wind_speed:.1f} m/s</div>
            <div> barometer Pressão: {pressure} hPa</div>
            {f"<div>👁️ Visibilidade: {visibility / 1000:.1f} km</div>" if visibility else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Exibir previsão de 5 dias
    if forecast_data and forecast_data.get('list'):
        st.subheader("Previsão para os Próximos Dias")
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

    # Exibir qualidade do ar
    if air_quality_data:
        st.subheader("Qualidade do Ar")
        aqi = air_quality_data['list'][0]['main']['aqi']
        aqi_levels = {
            1: "Boa",
            2: "Razoável",
            3: "Moderada",
            4: "Ruim",
            5: "Muito Ruim"
        }
        aqi_description = aqi_levels.get(aqi, "Desconhecida")

        components_data = air_quality_data['list'][0]['components']
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AQI", aqi_description, delta_color="off")
        with col2:
            st.metric("PM2.5", f"{components_data['pm2_5']:.1f} µg/m³")
        with col3:
            st.metric("O3", f"{components_data['o3']:.1f} µg/m³")
        with col4:
            st.metric("CO", f"{components_data['co']:.1f} µg/m³")

        st.info("**PM2.5**: Partículas finas | **O3**: Ozônio | **CO**: Monóxido de Carbono")

def display_world_map():
    """Exibe um mapa mundial interativo com base na localização do usuário ou padrão."""
    st.subheader("Explore o Clima Global")
    st.write("Use a barra lateral para buscar o clima de uma cidade específica.")

    # Coordenadas padrão (ex: centro do Brasil)
    default_lat, default_lon = -14.235, -53.132

    # Criar um DataFrame para o mapa (pode ser expandido com mais cidades)
    map_data = pd.DataFrame({
        'lat': [default_lat],
        'lon': [default_lon]
    })

    st.map(map_data, zoom=3)

# --- FUNÇÃO PRINCIPAL ---

def main():
    setup_page_config()
    load_custom_css()

    # Inicializa o estado da sessão para a cidade se não existir
    if 'city' not in st.session_state:
        st.session_state.city = ""
    if 'speech_summary' not in st.session_state:
        st.session_state.speech_summary = None

    # Chave da API do OpenWeatherMap (substitua pela sua chave real)
    api_key = os.getenv("OPENWEATHER_API_KEY", "a384af5e1c47ff5c3b3bb3c47491476f")
    if api_key == "SUA_CHAVE_API_AQUI":
        st.error("Por favor, defina a variável de ambiente OPENWEATHER_API_KEY com sua chave da API do OpenWeatherMap.")
        st.stop()

    st.sidebar.header("🌍 Configurações de Clima")

    with st.sidebar:
        st.header("🏙️ Seleção de Cidade")
        city_input = st.text_input(
            "Digite o nome da cidade:",
            placeholder="Ex: São Paulo, Rio de Janeiro, Tokyo",
            key="city_input_sidebar"
        )

        if st.button("Buscar Clima", key="search_button"):
            st.session_state.city = city_input
            st.rerun()

        st.markdown("---")

        # Componente de assistente de voz
        st.header("🎙️ Assistente de Voz")
        voice_assistant_component(st.session_state.get("speech_summary", None))

        # Captura a entrada de voz do componente JS

        if "voice_input_hidden" in st.session_state:
            voice_input = st.session_state.voice_input_hidden
            recognized_city = extract_city_from_transcript(voice_input)
            if recognized_city:
                st.session_state.city = recognized_city
                st.rerun()
            else:
                st.sidebar.warning("Não foi possível reconhecer uma cidade na sua fala.")

        st.markdown("---")

        # Seleção de atividade
        st.header("🏃‍♂️ Sua Atividade")
        activity = st.selectbox(
            "Que atividade você pretende fazer?",
            ["Corrida", "Caminhada", "Ciclismo", "Esportes ao ar livre", "Exercícios leves", "Descanso ao ar livre"],
            key="activity_selector",
            help="Selecione a atividade que você planeja realizar"
        )

        st.markdown("---")

        # Seleção de condição física
        st.header("💪 Condição Física")
        condition = st.selectbox(
            "Como está sua condição física?",
            ["Excelente", "Boa", "Moderada", "Sensível", "Delicada"],
            key="condition_selector",
            help="Sua condição física influencia as recomendações de segurança"
        )

        st.markdown("---")
        st.markdown("""
        **Legenda das Condições:**
        - **Excelente**: Atlético, sem limitações
        - **Boa**: Pratica exercícios regularmente
        - **Moderada**: Ativo ocasionalmente
        - **Sensível**: Problemas respiratórios/cardíacos leves
        - **Delicada**: Condições de saúde que requerem cuidados
        """)

    # Área de conteúdo principal
    if st.session_state.city:
        city_to_display = st.session_state.city
        # Busca dados do tempo
        with st.spinner(f"Buscando dados climáticos para {city_to_display}..."):
            weather_data = get_weather(city_to_display, api_key)
            forecast_data = None
            air_quality_data = None

            if weather_data:
                # Obtém dados adicionais
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']

                forecast_data = get_forecast(city_to_display, api_key)
                air_quality_data = get_air_quality(lat, lon, api_key)

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
                display_weather(weather_data, forecast_data, air_quality_data)
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

