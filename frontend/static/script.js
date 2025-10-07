// 🔹 Captura o clique no botão "Buscar" e chama a função buscarClima()
document.getElementById("buscar").addEventListener("click", buscarClima);


// 🔹 Função principal de busca de clima
// Agora lida também com cidades não encontradas (erro do backend)
async function buscarClima() {
  // 1️⃣ Captura o valor digitado no input
  // Se estiver vazio, usa "Rio de Janeiro" como padrão
  const cidade = document.getElementById("cidade").value || "Rio de Janeiro";

  // 2️⃣ Elemento onde exibiremos os resultados
  const el = document.getElementById("resultado");

  // Mostra feedback enquanto a requisição é feita
  el.textContent = "Carregando...";

  try {
    // 3️⃣ Faz chamada ao backend Flask → rota /api/weather
    // encodeURIComponent garante que nomes com espaço funcionem (ex: "São Paulo")
    const res = await fetch(`/api/weather?city=${encodeURIComponent(cidade)}`);

    // Converte resposta em JSON
    const data = await res.json();

    // 4️⃣ Verifica se houve erro (ex: cidade não encontrada ou falha na API)
    if (data.error) {
      console.error("Erro retornado do backend:", data);
      el.innerHTML = `
    <p style="color:red;">
      ❌ Não foi possível obter o clima para <strong>${cidade}</strong>.<br>
      <em>${data.message || "Erro desconhecido"}</em>
    </p>
  `;
      return; // Interrompe execução
    }

    // ===================================================
    // 🔹 Extração e preparação dos dados (quando sucesso)
    // ===================================================

    // Clima → descrição e ícone
    const clima = data.weather[0];

    // Temperatura (em °C)
    const temp = data.main.temp;

    // Umidade → pode ser "null", então mostramos "—"
    const hum = data.main.humidity !== null ? data.main.humidity + "%" : "—";

    // Velocidade do vento
    const wind = data.wind.speed;

    // Ícone → se vier URL completa, usa direto; se vier código (ex: "01d"), monta URL padrão
    const iconUrl = clima.icon.startsWith("http")
      ? clima.icon
      : `https://openweathermap.org/img/wn/${clima.icon}@2x.png`;

    // ===================================================
    // 🔹 Renderização no HTML
    // ===================================================
    el.innerHTML = `
      <h2>${data.name}, ${data.sys.country}</h2>
      <p>
        <span style="font-size: 2em;">${clima.icon}</span>
        <strong>${temp}°C</strong> — ${clima.description}
      </p>
      <p>Umidade: ${hum} | Vento: ${wind} km/h</p>
    `;
  } catch (err) {
    // 5️⃣ Caso a comunicação falhe (servidor fora do ar, internet caída, etc.)
    el.textContent = "Erro ao buscar clima.";
    console.error("Erro inesperado:", err);
  }
}
