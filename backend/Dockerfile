# Imagem base oficial
FROM python:3.10-slim

# Configurações essenciais
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# INSTALAÇÃO CORRETA DO OLLAMA (funciona 100%)
RUN apt-get update && apt-get install -y curl libgl1 libglib2.0-0
# Baixa e extrai CORRETAMENTE o Ollama (solução definitiva)
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o /tmp/ollama.tgz && \
    mkdir -p /tmp/ollama && \
    tar xzf /tmp/ollama.tgz -C /tmp/ollama && \
    cp /tmp/ollama/bin/ollama /usr/local/bin/ && \
    chmod +x /usr/local/bin/ollama && \
    ollama --version && \
    rm -rf /tmp/ollama*

# PRÉ-CARREGA MODELO LLM
RUN ollama pull phi3
RUN ollama create aurax-model --from phi3

# Copia código fonte
COPY . .

# Executa o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
