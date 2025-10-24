"""
API FastAPI para consulta de viabilidade de endereços.
"""
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import logging

from .models import (
    ConsultaResponse,
    UploadResponse,
    HealthResponse,
    ErrorResponse
)
from .services import endereco_service

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="API de Consulta de Viabilidade de Endereços",
    description="""
    API para consultar a viabilidade de endereços no Nordeste do Brasil.

    ## Funcionalidades

    * **Consultar viabilidade** - Consulta por CEP e código do logradouro
    * **Upload de planilha** - Carrega dados de uma planilha Excel
    * **Health check** - Verifica status da API e estatísticas
    * **Limpar banco** - Remove todos os dados do banco

    ## Como usar

    1. Primeiro, faça upload de uma planilha usando `/upload`
    2. Depois, consulte endereços usando `/consultar`
    3. Use `/health` para verificar quantos registros estão carregados
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS - IMPORTANTE: deve ser o primeiro middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, DELETE, OPTIONS, etc)
    allow_headers=["*"],  # Permite todos os headers
    expose_headers=["*"],  # Expõe todos os headers na resposta
)


# Handler para requisições OPTIONS (preflight)
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """
    Handler para requisições OPTIONS (CORS preflight).
    Garante que o navegador aceite requisições de outras origens.
    """
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400",  # Cache preflight por 24h
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz da API.
    """
    return {
        "mensagem": "API de Consulta de Viabilidade de Endereços",
        "versao": "1.0.0",
        "documentacao": "/docs",
        "endpoints": {
            "health": "/health",
            "consultar": "/consultar?cep=60876672&cod_logradouro=13784",
            "upload": "/upload",
            "limpar": "/limpar"
        }
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Verificar saúde da API"
)
async def health_check():
    """
    Verifica o status da API e retorna estatísticas sobre os dados carregados.

    Retorna:
    - Status da API
    - Status do banco de dados
    - Total de registros
    - Estatísticas por viabilidade e município
    """
    return endereco_service.get_health()


@app.get(
    "/consultar",
    response_model=ConsultaResponse,
    tags=["Consultas"],
    summary="Consultar viabilidade de endereço"
)
async def consultar_viabilidade(
    cep: str = Query(
        ...,
        description="CEP do endereço (com ou sem hífen)",
        example="60876672"
    ),
    numero: str = Query(
        ...,
        description="Número da fachada",
        example="144"
    )
):
    """
    Consulta a viabilidade de um endereço pelo CEP e número da fachada.

    ## Parâmetros
    - **cep**: CEP do endereço (pode ser com ou sem hífen: 60876-672 ou 60876672)
    - **numero**: Número da fachada

    ## Resposta
    - **encontrado**: Se o endereço foi encontrado
    - **viabilidade**: Status de viabilidade ("Viável", "Não viável", etc)
    - **detalhes**: Informações completas do endereço (UF, município, bairro, etc)
    - **mensagem**: Mensagem adicional

    ## Exemplo
    ```
    GET /consultar?cep=60876672&numero=144
    ```
    """
    logger.info(f"Consultando viabilidade: CEP={cep}, NUMERO={numero}")
    return endereco_service.consultar_viabilidade(cep, numero)


@app.post(
    "/upload",
    response_model=UploadResponse,
    tags=["Upload"],
    summary="Upload de planilha Excel"
)
async def upload_planilha(
    file: UploadFile = File(..., description="Arquivo Excel (.xlsx) com os endereços")
):
    """
    Faz upload de uma planilha Excel com dados de endereços.

    ## Formato esperado da planilha
    - Arquivo Excel (.xlsx)
    - Pode ter múltiplas abas (uma para cada município)
    - Estrutura esperada:
        - Linha 1: vazia
        - Linha 2: headers (VIABILIDADE_ATUAL, UF, MUNICIPIO, etc)
        - Linha 3+: dados

    ## Colunas esperadas
    1. VIABILIDADE_ATUAL
    2. UF
    3. MUNICIPIO
    4. LOCALIDADE
    5. BAIRRO
    6. LOGRADOURO
    7. COD_LOGRADOURO
    8. N_FACHADA
    9. COMP_1
    10. COMP_2
    11. COMP_3
    12. REGIAO
    13. CEP
    14. TOTAL_HPS

    ## Comportamento
    - Remove todos os dados antigos do banco
    - Processa todas as abas da planilha
    - Insere os novos dados

    ## Resposta
    - **sucesso**: Se o upload foi bem-sucedido
    - **mensagem**: Mensagem sobre o resultado
    - **registros_inseridos**: Quantidade de registros inseridos
    - **tempo_processamento**: Tempo gasto em segundos
    """
    # Validar extensão do arquivo
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(
            status_code=400,
            detail="Arquivo inválido. Apenas arquivos .xlsx são aceitos."
        )

    # Salvar arquivo temporário
    upload_dir = Path(__file__).parent.parent / "data" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    temp_file_path = upload_dir / file.filename

    try:
        logger.info(f"Salvando arquivo: {file.filename}")

        # Salvar arquivo
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Arquivo salvo em: {temp_file_path}")

        # Processar planilha
        resultado = endereco_service.upload_planilha(temp_file_path)

        return resultado

    except Exception as e:
        logger.error(f"Erro ao fazer upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )
    finally:
        # Limpar arquivo temporário (opcional - você pode querer manter)
        # if temp_file_path.exists():
        #     temp_file_path.unlink()
        pass


@app.delete(
    "/limpar",
    tags=["Admin"],
    summary="Limpar banco de dados"
)
async def limpar_banco():
    """
    Remove todos os dados do banco de dados.

    **Atenção**: Esta operação não pode ser desfeita!

    Use este endpoint quando quiser recarregar uma nova planilha do zero.
    """
    logger.warning("Limpando banco de dados...")
    resultado = endereco_service.limpar_banco()

    if resultado["sucesso"]:
        return JSONResponse(
            status_code=200,
            content=resultado
        )
    else:
        raise HTTPException(
            status_code=500,
            detail=resultado["mensagem"]
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handler global para exceções não tratadas.
    """
    logger.error(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "erro": "Erro interno do servidor",
            "detalhes": str(exc)
        }
    )


# Evento de inicialização
@app.on_event("startup")
async def startup_event():
    """Executado quando a API inicia."""
    logger.info("=== API de Consulta de Viabilidade Iniciada ===")
    logger.info("Documentação disponível em: /docs")


# Evento de finalização
@app.on_event("shutdown")
async def shutdown_event():
    """Executado quando a API é desligada."""
    logger.info("=== API Finalizada ===")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
