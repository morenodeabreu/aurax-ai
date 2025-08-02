# Imagem base oficial
FROM python:3.10-slim

# Configurações essenciais
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código fonte
COPY . .

# Executa o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
