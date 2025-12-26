CloudWalk – Real-Time Transactions Monitoring

Sistema de monitoramento contínuo de transações, construído para detectar anomalias operacionais em tempo quase real analisando comportamento por minuto.
Mantém um estado vivo em memória, aplica regras estatísticas, gera alertas estruturados e agora também disponibiliza um dashboard visual em tempo quase real.

O objetivo foi simular um ambiente de produção real, com:

• arquitetura limpa e desacoplada
• execução contínua
• regras estatísticas claras
• estado vivo em memória
• alertas contextuais e explicáveis
• visualização operacional em tempo quase real

🎯 O que este sistema faz

✔️ Lê e simula o fluxo de transações minuto a minuto
✔️ Mantém uma janela deslizante de histórico (ex: últimos 30 min)
✔️ Monitora métricas sensíveis operacionalmente
✔️ Detecta spikes estatísticos usando baseline + z-score
✔️ Emite alertas estruturados automaticamente
✔️ Exibe um mini-dashboard textual no terminal
✔️ Disponibiliza um dashboard visual contínuo com gráficos em tempo quase real

🔎 Como o monitoramento funciona na prática

O serviço roda como um processo contínuo em Python. Ele percorre os eventos de transações em “tempo quase real”, minuto a minuto, mantendo uma janela deslizante de 30 minutos.

A cada minuto o sistema executa quatro etapas:

1️⃣ Atualiza o estado

Adiciona o bucket de transações daquele minuto na janela em memória.

2️⃣ Constrói um snapshot

Gera um mini dashboard textual com o estado atual (approved, failed, denied, reversed, etc.).

3️⃣ Avalia anomalias

Aplica regras estatísticas baseadas em:

– baseline histórico
– média
– desvio padrão
– z-score

4️⃣ Emite alertas

Quando encontra comportamento suspeito → imprime um alerta estruturado com contexto completo.

🖥️ Exemplo real de execução
📡 Processing minute -> 2025-07-12 18:07:00
========= SNAPSHOT =========
Window Size    : 30 minutes
Latest Minute  : 2025-07-12 18:07:00

Approved       : 116
Failed         : 0
Denied         : 5
Reversed       : 5
============================
⚠️  1 anomaly signal(s) detected!

🚨 ALERT DETECTED 🚨
Time: 2025-07-12 18:07:00
Dimension: status
Key: reversed
Current Value: 5
Baseline Mean: 1.17
Baseline Std : 1.18
Z-Score      : 3.26
----------------------------------------------


Isso simula uma operação real rodando, com vida, histórico e inteligência.

🧠 Regras de Detecção

O sistema avalia inicialmente os status mais críticos:

• failed
• denied
• reversed

A lógica segue:

✔️ só avalia quando há histórico suficiente
✔️ ignora ruído de volumes baixos
✔️ calcula baseline (média + desvio padrão)
✔️ dispara alerta quando:

z-score > 3.0


Ou seja — detecta comportamentos estatisticamente anormais.

🖥️ Real-Time Dashboard

Além do engine contínuo, o projeto inclui um dashboard em tempo quase real, desenvolvido em Streamlit, que consome snapshots gerados pelo engine e exibe:

✔️ último estado do sistema
✔️ métricas operacionais
✔️ gráficos de evolução por status
✔️ atualização contínua enquanto o serviço roda

O dashboard lê snapshots estruturados gerados pelo engine em um arquivo incremental (monitor_snapshots.jsonl) e atualiza automaticamente.

📌 Design Decision – JSONL
Snapshots são gravados em formato JSONL (um JSON por linha) porque:
✔ permite leitura incremental em tempo real
✔ suporta escrita contínua sem reprocessar o arquivo
✔ funciona bem como “ponte” entre engine e dashboard
✔ é simples, robusto e operacionalmente eficiente

🏗️ Arquitetura do Projeto

Organizado para ser claro, extensível e fácil de evoluir.

src/
 ├── alerting/
 │    └── alerts.py        # formatação e emissão de alertas
 │
 ├── core/
 │    ├── event.py         # contrato do evento por minuto
 │    ├── state.py         # janela deslizante e estado global
 │    ├── rules.py         # regras de anomalia
 │
 ├── dashboard/
 │    └── snapshot.py      # snapshots e export para dashboard
 │
 ├── engine/
 │    └── monitor.py       # loop principal / lifecycle do sistema
 │
 ├── ingest/
 │    └── csv_stream.py    # simulação de stream minuto a minuto

▶️ Como executar
1️⃣ Iniciar o serviço de monitoramento

Na raiz do projeto:

python main.py


Isso irá:

– simular tempo real
– exibir snapshots no terminal
– gerar snapshots estruturados para o dashboard

2️⃣ Iniciar o dashboard visual

Em outro terminal, na raiz do projeto:

streamlit run dashboard.py


O navegador abrirá automaticamente exibindo:

– último snapshot
– métricas
– gráfico de evolução
– atualização contínua

🚀 Resultado

Você obtém um sistema que:

✔️ roda continuamente
✔️ mantém estado vivo
✔️ detecta anomalias proativamente
✔️ gera visibilidade operacional real
✔️ combina engine + análise + dashboard
✔️ é simples de rodar, entender e evoluir