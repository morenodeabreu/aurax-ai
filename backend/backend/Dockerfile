# Etapa 1: Builder para dependências
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Imagem final otimizada
FROM python:3.10-slim

# Configurações de segurança
USER nonroot:nonroot
WORKDIR /app

# Copia apenas dependências necessárias
COPY --from=builder /root/.local /root/.local
COPY . .

# Configurações de produção
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1 \
    OLLAMA_HOST=0.0.0.0 \
    OLLAMA_PORT=11434

# Verifica integridade do modelo
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:11434/api/tags || exit 1

# Executa com segurança e monitoramento
CMD ["sh", "-c", "ollama serve & uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info"]
