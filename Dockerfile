# Imagem base oficial do Python
FROM python:3.10-slim

# Configurações essenciais
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PRÉ-CARREGA MODELO LLM (CORREÇÃO CRÍTICA)
RUN apt-get update && apt-get install -y curl
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz | tar xz -C /usr/local/bin
RUN ollama pull phi3
RUN ollama create aurax-model --from phi3

# Copia código fonte
COPY . .

# Executa o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
