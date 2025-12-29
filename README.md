CloudWalk – Real-Time Transactions Monitoring


Sistema de monitoramento quase em tempo real para análise operacional de transações, com engine contínua, detecção de anomalias e dashboard visual.



O objetivo foi simular um ambiente próximo de produção, entregando:

arquitetura limpa e desacoplada

execução contínua

janela deslizante de histórico

regras estatísticas explicáveis

estado vivo em memória

alertas estruturados

dashboard operacional em tempo quase real



🎯 O que este sistema faz

✔️ simula fluxo de transações minuto a minuto
✔️ mantém janela deslizante de 30 minutos
✔️ calcula métricas operacionais
✔️ detecta anomalias com baseline + z-score
✔️ gera snapshots estruturados e persistidos
✔️ emite alertas com contexto
✔️ disponibiliza dashboard visual contínuo



🔎 Como o monitoramento funciona

O motor percorre os eventos de transações minuto a minuto, mantendo um estado vivo.
A cada minuto ele:

1️⃣ Atualiza a janela de histórico
2️⃣ Gera um snapshot operacional
3️⃣ Avalia anomalias estatísticas
4️⃣ Emite alertas quando necessário



🧠 Regras de Detecção

O sistema monitora principalmente:

failed

denied

reversed


E aplica:

baseline histórico

média

desvio padrão

z-score


Dispara alerta quando:

z-score > 3.0



🖥️ Real-Time Dashboard

O dashboard em Streamlit:

exibe último snapshot

mostra métricas operacionais

apresenta gráfico de evolução

atualiza continuamente enquanto o motor gera dados

Os snapshots são gravados em:

data/monitor_snapshots.jsonl


Formato JSONL foi escolhido porque:

permite leitura incremental

suporta escrita contínua

simples e resiliente

perfeito como “ponte” engine → dashboard



🏗️ Arquitetura do Projeto
src/
 ├── alerting/      alertas e formatação
 ├── core/          estado, eventos e regras
 ├── dashboard/     snapshot interface
 ├── engine/        lifecycle do monitoramento
 ├── ingest/        simulação de fluxo



🧾 Comportamento do Sistema (Design Decision)

Este sistema processa um dataset histórico e reproduz transações minuto a minuto.

o engine gera snapshots incrementalmente

o dashboard consome o snapshot mais recente válido

quando o dataset termina, o dashboard mantém o último estado

não “inventa” novos valores

não retrocede no tempo

Esse comportamento é intencional e alinhado com sistemas reais de observabilidade:
se não há novos dados, o sistema permanece estável.



🔁 Como reproduzir / testar novamente

Para reiniciar o replay do zero:

1️⃣ Pare o engine e o dashboard
2️⃣ Vá até a pasta data/
3️⃣ Delete ou renomeie:

monitor_snapshots.jsonl


4️⃣ Rode o motor:

python main.py


5️⃣ Em outro terminal, rode o dashboard:

streamlit run dashboard.py


O dashboard irá:

iniciar com poucos snapshots

crescer ao longo do processamento

evoluir até o último timestamp do dataset



💡 Observação Importante

O sistema foi desenhado como monitor real:

Não cria dados quando não há novos eventos
Não “anda para trás no tempo”
Mantém o último estado válido do ambiente

Caso desejado, é trivial habilitar um modo contínuo (loop infinito) no engine.



▶️ Execução Rápida

Motor:

python main.py


Dashboard:

streamlit run dashboard.py



🚀 Resultado

Você obtém um sistema que:

✔️ roda continuamente
✔️ mantém estado real
✔️ detecta anomalias
✔️ gera evidências operacionais
✔️ fornece dashboard quase em tempo real
✔️ é simples de executar, entender e evoluir