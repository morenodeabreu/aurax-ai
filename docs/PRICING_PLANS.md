# Planos de Assinatura do AURAX

## Estrutura de Planos

| Recurso                     | Gratuito       | Pro ($19/mês)  | Master ($59/mês) |
|-----------------------------|----------------|----------------|------------------|
| **Contexto Máximo**         | 8k tokens      | 32k tokens     | 128k tokens      |
| **Limite de Uso**           | 10h/mês        | 55h/mês        | 170h/mês         |
| **Dispositivos**            | 1              | 1              | 2                |
| **Geração de Código**       | ✘              | ✔              | ✔                |
| **Geração de Imagens**      | ✘              | ✔ (5/dia)      | ✔ (ilimitado)    |
| **Prioridade na GPU**       | Baixa          | Média          | Alta             |
| **Suporte**                 | Comunidade     | 24h            | 2h               |

## Política Anti-Compartilhamento

### 1. Device Fingerprinting
- Geração de hash único por dispositivo
- Bloqueio automático se detectar múltiplos dispositivos

### 2. Limites de Uso Justo
- **Janela de contexto dinâmica**:
  - Reduz contexto máximo se detectar padrão de compartilhamento
  ```python
  if uso_anormal(user_id):
      contexto_max = 8000  # Reduz de 32k para 8k
