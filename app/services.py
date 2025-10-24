"""
Serviços de lógica de negócio para a API.
"""
from pathlib import Path
from typing import Optional
import logging
import time

from .database import db
from .utils import processar_planilha_excel, normalizar_cep, validar_cep
from .models import (
    ConsultaResponse,
    EnderecoDetalhes,
    UploadResponse,
    HealthResponse
)

logger = logging.getLogger(__name__)


class EnderecoService:
    """Serviço para operações relacionadas a endereços."""

    @staticmethod
    def consultar_viabilidade(cep: str, n_fachada: str) -> ConsultaResponse:
        """
        Consulta a viabilidade de um endereço.

        Args:
            cep: CEP do endereço
            n_fachada: Número da fachada

        Returns:
            ConsultaResponse com o resultado da consulta
        """
        # Validar CEP
        if not validar_cep(cep):
            return ConsultaResponse(
                encontrado=False,
                mensagem=f"CEP inválido: {cep}. Deve conter 8 dígitos."
            )

        # Normalizar entradas
        cep_normalizado = normalizar_cep(cep)
        n_fachada_normalizado = str(n_fachada).strip()

        # Consultar no banco
        resultado = db.consultar_viabilidade(cep_normalizado, n_fachada_normalizado)

        if resultado:
            # Endereço encontrado
            detalhes = EnderecoDetalhes(
                viabilidade_atual=resultado.get('viabilidade_atual'),
                uf=resultado.get('uf'),
                municipio=resultado.get('municipio'),
                localidade=resultado.get('localidade'),
                bairro=resultado.get('bairro'),
                logradouro=resultado.get('logradouro'),
                n_fachada=resultado.get('n_fachada'),
                comp_1=resultado.get('comp_1'),
                comp_2=resultado.get('comp_2'),
                comp_3=resultado.get('comp_3'),
                regiao=resultado.get('regiao'),
                cep=resultado.get('cep'),
                cod_logradouro=resultado.get('cod_logradouro'),
                total_hps=resultado.get('total_hps')
            )

            return ConsultaResponse(
                encontrado=True,
                viabilidade=resultado.get('viabilidade_atual'),
                detalhes=detalhes,
                mensagem="Endereço encontrado com sucesso"
            )
        else:
            # Endereço não encontrado
            return ConsultaResponse(
                encontrado=False,
                mensagem=f"Endereço não encontrado para CEP {cep} e Número {n_fachada}"
            )

    @staticmethod
    def upload_planilha(file_path: Path) -> UploadResponse:
        """
        Processa e carrega uma planilha Excel no banco de dados.

        Args:
            file_path: Caminho para o arquivo Excel

        Returns:
            UploadResponse com o resultado do upload
        """
        inicio = time.time()

        try:
            logger.info(f"Iniciando upload da planilha: {file_path}")

            # Validar se o arquivo existe
            if not file_path.exists():
                return UploadResponse(
                    sucesso=False,
                    mensagem=f"Arquivo não encontrado: {file_path}",
                    tempo_processamento=time.time() - inicio
                )

            # Processar a planilha
            logger.info("Processando planilha...")
            enderecos = processar_planilha_excel(file_path)

            if not enderecos:
                return UploadResponse(
                    sucesso=False,
                    mensagem="Nenhum registro encontrado na planilha",
                    tempo_processamento=time.time() - inicio
                )

            # Limpar dados antigos
            logger.info("Limpando banco de dados...")
            db.clear_all()

            # Inserir novos dados em lotes
            logger.info(f"Inserindo {len(enderecos)} registros no banco...")
            batch_size = 5000
            total_inseridos = 0

            for i in range(0, len(enderecos), batch_size):
                batch = enderecos[i:i + batch_size]
                inseridos = db.insert_enderecos(batch)
                total_inseridos += inseridos
                logger.info(f"Progresso: {total_inseridos}/{len(enderecos)} registros")

            tempo_total = time.time() - inicio

            return UploadResponse(
                sucesso=True,
                mensagem=f"Planilha processada com sucesso! {total_inseridos} registros inseridos.",
                registros_inseridos=total_inseridos,
                tempo_processamento=round(tempo_total, 2)
            )

        except Exception as e:
            logger.error(f"Erro ao processar planilha: {str(e)}")
            return UploadResponse(
                sucesso=False,
                mensagem=f"Erro ao processar planilha: {str(e)}",
                tempo_processamento=time.time() - inicio
            )

    @staticmethod
    def get_health() -> HealthResponse:
        """
        Retorna informações de saúde da API.

        Returns:
            HealthResponse com status da API
        """
        try:
            # Verificar se há dados no banco
            tem_dados = db.database_exists()

            if tem_dados:
                stats = db.get_stats()
                return HealthResponse(
                    status="healthy",
                    banco_de_dados="conectado",
                    total_registros=stats['total_registros'],
                    estatisticas=stats
                )
            else:
                return HealthResponse(
                    status="healthy",
                    banco_de_dados="vazio",
                    total_registros=0,
                    estatisticas={"mensagem": "Nenhum dado carregado. Use o endpoint /upload para carregar uma planilha."}
                )

        except Exception as e:
            logger.error(f"Erro ao verificar saúde: {str(e)}")
            return HealthResponse(
                status="unhealthy",
                banco_de_dados="erro",
                total_registros=0,
                estatisticas={"erro": str(e)}
            )

    @staticmethod
    def limpar_banco() -> dict:
        """
        Limpa todos os dados do banco.

        Returns:
            Dicionário com o resultado da operação
        """
        try:
            db.clear_all()
            return {
                "sucesso": True,
                "mensagem": "Banco de dados limpo com sucesso"
            }
        except Exception as e:
            logger.error(f"Erro ao limpar banco: {str(e)}")
            return {
                "sucesso": False,
                "mensagem": f"Erro ao limpar banco: {str(e)}"
            }


# Instância global do serviço
endereco_service = EnderecoService()
