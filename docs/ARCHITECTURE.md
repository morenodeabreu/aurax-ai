# Arquitetura do AURAX

## Visão Geral
```mermaid
graph TD
    A[Usuário] --> B(Roteador de Intenções)
    B --> C{Análise de Domínio}
    C -->|Código| D[Qwen3 Coder + CodeLlama]
    C -->|Design| E[Stable Diffusion 3]
    C -->|Pesquisa| F[Suna-like Web Scanner]
    F --> G[Qdrant + RAG Vetorial]
    G --> H[Atualiza Modelo com Novos Dados]
    D & E & H --> I[Geração Autônoma de App Completo]
    I --> J[Deploy Automático no Vercel/AWS]
def classificar_intencao(query):
    prompt = f"Classifique a intenção: {query}. Opções: [código, design, pesquisa, vídeo]"
    return kimi_k2.generate(prompt, max_tokens=5)
def buscar_tendencias_delivery():
    resultados = apify_scrape("delivery sustentável 2024", max_pages=50)
    chunks = processar_dados(resultados)
    qdrant.upload(chunks, collection="tendencias_delivery")
// frontend.js
const fingerprint = await FingerprintJS.load().then(fp => fp.get());
def validar_dispositivo(user_id, device_hash):
    # 1. Verifica se o dispositivo está registrado
    usuario = db.buscar_usuario(user_id)
    if device_hash not in usuario['dispositivos']:
        return False
    
    # 2. Verifica atividade anormal (múltiplos dispositivos em 24h)
    atividade = db.buscar_atividade(user_id, ultimas_24h=True)
    dispositivos_unicos = set([a['device_hash'] for a in atividade])
    if len(dispositivos_unicos) > 1:
        db.bloquear_conta(user_id, motivo="Dispositivos múltiplos")
        return False
    
    # 3. Atualiza último acesso
    db.atualizar_ultimo_acesso(user_id, device_hash)
    return True
---

