from flask import Flask, jsonify, request , send_from_directory
from flask_cors import CORS  # Permite comunicação entre frontend/backend
from weather_service import get_weather
# import requests # para fazer requisições HTTP
# import os 
# from urllib.parse import quote # <-- importa para codificar a cidade

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend") # Cria a aplicação Flask
CORS(app) # Habilita CORS para o frontend acessar
# API_KEY = os.getenv("SECRET_KEY") or "SECRET_KEY=4511b5d287d201522e2c9bc7a23c9f9c" # minha chave da API de clima

@app.route("/")
def index():
    # return "Servidor funcionando! Use /clima?cidade=NomeDaCidade"
    return send_from_directory("../frontend", "index.html")

# Rota de API → consulta clima
@app.route("/api/weather")
def weather():
    # Pega a cidade da query string (?city=Lisboa)
    city = request.args.get("city", "Rio de Janeiro")

    # Chama a função de serviço que consulta Open-Meteo
    data = get_weather(city)

    # Mostra no terminal para debug (didático em aula)
    print(f"🔍 DEBUG Consulta de clima para {city}:", data)

    # Retorna JSON para o frontend
    return jsonify(data)


# Rota de arquivos estáticos (CSS, JS, imagens)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("../frontend/static", filename)


if __name__ =="__main__":
    app.run(debug=True)

"""código fez uma requisição para: https://api.openweathermap.org/data/2.5/weather?q=Rio%20de%20Janeiro,br&appid=4511b5d287d201522e2c9bc7a23c9f9c&units=metric&lang=pt_br

você consome dados em tempo real de serviços especializados! Mesmo não colocando os dados no codigo 
Como funciona:
Você pede: "Quero o clima do Rio de Janeiro"

Seu código pergunta para OpenWeatherMap: "Me dá dados do Rio"

OpenWeatherMap retorna: "Tá 22.76°C, nublado, 73% umidade"

Seu código formata e devolve para você 
"""