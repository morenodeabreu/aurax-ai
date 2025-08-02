
# Pré-carrega modelo LLM
RUN ollama pull phi3
RUN ollama create aurax-model --from phi3
