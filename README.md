CloudWalk – Real-Time Transactions Monitoring


Sistema de monitoramento contínuo de transações, construído para detectar anomalias operacionais em tempo quase real analisando comportamento por minuto, mantendo um histórico de janela deslizante e emitindo alertas quando padrões suspeitos surgem.


O objetivo é simular um ambiente de produção real, com:

arquitetura limpa e desacoplada

execução contínua

regras estatísticas claras

estado vivo em memória

alertas contextuais e explicáveis



🎯 O que este sistema faz

✔️ Lê e simula o fluxo de transações minuto a minuto
✔️ Mantém uma janela deslizante de histórico (ex: últimos 30 min)
✔️ Monitora métricas sensíveis operacionalmente
✔️ Detecta spikes estatísticos usando baseline + z-score
✔️ Emite alertas estruturados
✔️ Exibe um mini-dashboard textual em tempo real



🔎 Como o monitoramento funciona na prática

O serviço roda como um processo contínuo em Python. Ele percorre os eventos de transações em “tempo quase real”, minuto a minuto, mantendo uma janela deslizante de 30 minutos.

A cada minuto o sistema executa quatro etapas:

1️⃣ Atualiza o estado
Adiciona o bucket de transações daquele minuto na janela em memória.

2️⃣ Constrói um snapshot
Gera um mini dashboard textual com o estado atual
(approved, failed, denied, reversed, etc.).

3️⃣ Avalia anomalias
Aplica regras estatísticas baseadas em:

baseline histórico

média

desvio padrão

z-score

4️⃣ Emite alertas
Quando encontra uma anomalia, imprime um alerta estruturado com contexto completo.



🖥️ Exemplo real de execução


📡 Processing minute -> 2025-07-12 18:06:00
========= SNAPSHOT =========
Window Size    : 30 minutes
Latest Minute  : 2025-07-12 18:06:00

Approved       : 109
Failed         : 0
Denied         : 2
Reversed       : 0
============================
✅ No anomalies detected.


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
Baseline Std: 1.18
Z-Score: 3.26
Reason: reversed spiked: 5 vs baseline mean=1.17, std=1.18, z=3.26
----------------------------------------------

Isso simula uma operação real rodando, com vida, histórico e inteligência.



🧠 Regras de Detecção

O sistema avalia inicialmente os status mais críticos para operação:

failed

denied

reversed

A lógica segue:

✔️ só avalia quando há histórico suficiente
✔️ ignora ruído (volumes muito baixos)
✔️ calcula baseline (média + desvio padrão)
✔️ dispara alerta quando:

z-score > limiar (ex: 3.0)

Ou seja: detecta comportamentos estatisticamente anormais.



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
 │    └── snapshot.py      # mini dashboard textual
 │
 ├── engine/
 │    └── monitor.py       # loop principal / lifecycle do sistema
 │
 ├── ingest/
 │    └── csv_stream.py    # simulação de stream minuto a minuto
 │


Este desenho garante:

separação de responsabilidades

baixo acoplamento

fácil teste de componentes

clareza para leitura e evolução futura



▶️ Como rodar

1️⃣ Clone o repositório
2️⃣ Garanta Python 3.10+ instalado
3️⃣ Na raiz do projeto execute:

python main.py


O sistema começará a processar “tempo simulado” e exibirá:

snapshots a cada minuto

alertas quando necessário




🚀 Resultado

Você obtém um sistema de monitoramento que:

✔️ roda continuamente
✔️ mantém estado real em memória
✔️ gera visibilidade operacional
✔️ detecta incidentes antes que causem impacto
✔️ é simples de entender e evoluir