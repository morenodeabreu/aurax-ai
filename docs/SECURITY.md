# Segurança do AURAX

## Camadas de Segurança

### 1. Autenticação Segura
- **JWT + Device Fingerprint**
  - Token válido só para 1 dispositivo por conta
  - Exemplo de implementação:
    ```python
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
    ```

### 2. Proteção contra Abuso
- **Rate Limiting**:
  - Máximo de 5 requests/segundo por usuário
  - Implementação com Redis + Token Bucket
  ```python
  def verificar_rate_limit(user_id):
      now = time.time()
      window_start = now - 1  # 1 segundo
      requests = redis.zrangebyscore(f"rl:{user_id}", window_start, now)
      if len(requests) >= 5:
          return False
      redis.zadd(f"rl:{user_id}", {now: now})
      redis.expire(f"rl:{user_id}", 1)
      return True
