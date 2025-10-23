"""
Modelos Pydantic para validação de dados da API.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ConsultaRequest(BaseModel):
    """Modelo para requisição de consulta de viabilidade."""
    cep: str = Field(..., description="CEP do endereço (com ou sem hífen)", example="60876-672")
    cod_logradouro: str = Field(..., description="Código do logradouro", example="13784")


class EnderecoDetalhes(BaseModel):
    """Modelo para detalhes do endereço."""
    viabilidade_atual: Optional[str] = None
    uf: Optional[str] = None
    municipio: Optional[str] = None
    localidade: Optional[str] = None
    bairro: Optional[str] = None
    logradouro: Optional[str] = None
    n_fachada: Optional[str] = None
    comp_1: Optional[str] = None
    comp_2: Optional[str] = None
    comp_3: Optional[str] = None
    regiao: Optional[str] = None
    cep: Optional[str] = None
    cod_logradouro: Optional[str] = None
    total_hps: Optional[int] = None


class ConsultaResponse(BaseModel):
    """Modelo para resposta de consulta de viabilidade."""
    encontrado: bool = Field(..., description="Se o endereço foi encontrado")
    viabilidade: Optional[str] = Field(None, description="Status de viabilidade (Viável, Não viável, etc)")
    detalhes: Optional[EnderecoDetalhes] = Field(None, description="Detalhes do endereço")
    mensagem: Optional[str] = Field(None, description="Mensagem adicional")


class UploadResponse(BaseModel):
    """Modelo para resposta de upload de planilha."""
    sucesso: bool = Field(..., description="Se o upload foi bem-sucedido")
    mensagem: str = Field(..., description="Mensagem sobre o resultado")
    registros_inseridos: int = Field(0, description="Número de registros inseridos")
    tempo_processamento: float = Field(0, description="Tempo de processamento em segundos")


class HealthResponse(BaseModel):
    """Modelo para resposta de health check."""
    status: str = Field(..., description="Status da API", example="healthy")
    banco_de_dados: str = Field(..., description="Status do banco de dados")
    total_registros: int = Field(0, description="Total de registros no banco")
    estatisticas: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Modelo para resposta de erro."""
    erro: str = Field(..., description="Descrição do erro")
    detalhes: Optional[str] = Field(None, description="Detalhes adicionais do erro")
