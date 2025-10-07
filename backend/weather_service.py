import requests

# 🔹 URLs base da Open-Meteo
BASE_URL_WEATHER = "https://api.open-meteo.com/v1/forecast"  # Clima
BASE_URL_GEOCODE = "https://geocoding-api.open-meteo.com/v1/search"  # Geocoding (converter cidade -> lat/lon)

def get_weather_emoji(weather_code):
    """
    Mapeia códigos de clima da Open-Meteo para emojis.
    Baseado na documentação: https://open-meteo.com/en/docs
    """
    if weather_code == 0:
        return "☀️"  # Céu limpo
    elif weather_code in [1, 2, 3]:
        return "🌤️"  # Parcialmente nublado
    elif weather_code in [45, 48]:
        return "🌫️"  # Nevoeiro
    elif weather_code in [51, 53, 55]:
        return "🌦️"  # Chuvisco
    elif weather_code in [61, 63, 65]:
        return "🌧️"  # Chuva
    elif weather_code in [71, 73, 75]:
        return "🌨️"  # Neve
    elif weather_code in [77]:
        return "❄️"  # Grãos de neve
    elif weather_code in [80, 81, 82]:
        return "🌧️"  # Pancadas de chuva
    elif weather_code in [85, 86]:
        return "🌨️"  # Neve intensa
    elif weather_code in [95, 96, 99]:
        return "⛈️"  # Tempestade
    else:
        return "🌡️"  # Emoji padrão para condições desconhecidas

def get_coordinates(city: str):
    """
    Usa a API gratuita de Geocoding da Open-Meteo para converter
    o nome de uma cidade em coordenadas (latitude, longitude e país).
    Retorna um dicionário com lat, lon e country.
    """
    params = {"name": city, "count": 1, "language": "pt", "format": "json"}

    try:
        r = requests.get(BASE_URL_GEOCODE, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        
        # Se não encontrar resultados, retorna None
        if "results" not in data or len(data["results"]) == 0:
            return None

        result = data["results"][0]  # Pegamos o primeiro resultado
        return {
            "lat": result["latitude"],
            "lon": result["longitude"],
            "country": result.get("country_code", "??")  # Código do país (BR, PT, US...)
        }
    except requests.RequestException as e:
        return None


def get_weather(city: str = "Rio de Janeiro"):
    """
    Consulta o clima atual de QUALQUER cidade do mundo usando Open-Meteo.
    Fluxo:
      1. Geocoding → transforma "Lisboa" em latitude/longitude.
      2. Weather → busca clima atual dessas coordenadas.
      3. Normaliza os dados para manter o formato esperado pelo frontend.
    """

    # 1️⃣ Obter coordenadas pelo nome da cidade
    coords = get_coordinates(city)
    if not coords:
        return {
            "error": True,
            "message": f"Não foi possível encontrar a cidade '{city}'."
        }

    lat, lon, country = coords["lat"], coords["lon"], coords["country"]

    # 2️⃣ Montar parâmetros para consulta do clima
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "timezone": "auto"  # Ajusta fuso automaticamente baseado no local
    }

    try:
        # 🔹 Requisição do clima atual
        r = requests.get(BASE_URL_WEATHER, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Obter o emoji baseado no código do clima
        weather_code = data["current_weather"]["weathercode"]
        weather_emoji = get_weather_emoji(weather_code)


        # 3️⃣ Normalização do formato → compatível com OpenWeather
        return {
            "name": city.title(),  # Nome formatado (ex: "Lisboa")
            "main": {
                "temp": data["current_weather"]["temperature"],  # Temperatura em °C
                "humidity": None  # API básica não traz umidade
            },
            "weather": [{
                "description": "Condições atuais",
                "icon": weather_emoji  # Placeholder de ícone
            }],
            "wind": {
                "speed": data["current_weather"]["windspeed"]  # Velocidade do vento
            },
            "sys": {
                "country": country  # País do local consultado
            }
        }

    except requests.RequestException as e:
        return {"error": f"Erro ao consultar Open-Meteo: {e}"}
