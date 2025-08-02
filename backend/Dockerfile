# Imagem base oficial
FROM python:3.10-slim

# Configurações essenciais
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PRÉ-CARREGA MODELO LLM (SOLUÇÃO DEFINITIVA)
RUN apt-get update && apt-get install -y curl libgl1 libglib2.0-0
# Baixa e extrai CORRETAMENTE o Ollama
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o /tmp/ollama.tgz
RUN tar xzf /tmp/ollama.tgz -C /usr/local/bin --strip-components=1
# Verifica instalação
RUN ls -la /usr/local/bin/ollama && chmod +x /usr/local/bin/ollama
# Pré-carrega o modelo
RUN ollama pull phi3
RUN ollama create aurax-model --from phi3

# Copia código fonte
COPY . .

# Executa o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
