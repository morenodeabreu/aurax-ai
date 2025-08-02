from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

def check_model_ready():
    import time
    import requests
    max_wait = 1200  # 20 minutos máximo
    start_time = time.time()
    
    while True:
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200 and "models" in response.json():
                return True
        except Exception as e:
            print(f"Health check error: {str(e)}")
            
        if time.time() - start_time > max_wait:
            return False
            
        time.sleep(5)

@router.post("/generate")
async def generate(request: Request):
    # Verifica se o modelo está pronto
    if not check_model_ready():
        raise HTTPException(
            status_code=503,
            detail="Modelo carregando. Tente novamente em 5 minutos."
        )
    
    # Seu código existente para processar a requisição
    return {"response": "Resposta do modelo"}
