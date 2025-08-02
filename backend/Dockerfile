# Imagem base oficial
FROM python:3.10-slim

# Configurações essenciais
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PRÉ-CARREGA MODELO LLM (CORREÇÃO FINAL)
RUN apt-get update && apt-get install -y curl libgl1 libglib2.0-0
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz | tar xz -C /usr/local/bin
# Garante que o PATH está correto e usa caminho absoluto
ENV PATH="/usr/local/bin:${PATH}"
RUN /usr/local/bin/ollama pull phi3
RUN /usr/local/bin/ollama create aurax-model --from phi3

# Copia código fonte
COPY . .

# Executa o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
