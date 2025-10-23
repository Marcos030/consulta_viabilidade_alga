"""
Funções utilitárias para processamento de dados.
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def processar_planilha_excel(file_path: Path) -> List[Dict[str, Any]]:
    """
    Processa a planilha Excel e retorna uma lista de dicionários com os dados.

    A planilha tem uma estrutura especial:
    - Linha 1: vazia
    - Linha 2: headers reais
    - Linha 3+: dados

    Args:
        file_path: Caminho para o arquivo Excel

    Returns:
        Lista de dicionários com os dados dos endereços

    Raises:
        Exception: Se houver erro ao processar a planilha
    """
    logger.info(f"Processando planilha: {file_path}")

    try:
        # Ler o arquivo Excel
        xl = pd.ExcelFile(file_path)
        logger.info(f"Abas encontradas: {xl.sheet_names}")

        todos_enderecos = []

        # Processar cada aba
        for sheet_name in xl.sheet_names:
            logger.info(f"Processando aba: {sheet_name}")

            # Ler a aba, pulando a primeira linha e usando a segunda como header
            df = pd.read_excel(
                xl,
                sheet_name=sheet_name,
                skiprows=1,  # Pular a primeira linha vazia
                header=0     # Usar a primeira linha após skip como header
            )

            # Remover linhas completamente vazias
            df = df.dropna(how='all')

            # Renomear colunas para nomes padronizados
            # A primeira coluna contém a viabilidade
            colunas_mapeamento = {
                df.columns[0]: 'viabilidade_atual',
                df.columns[1]: 'uf',
                df.columns[2]: 'municipio',
                df.columns[3]: 'localidade',
                df.columns[4]: 'bairro',
                df.columns[5]: 'logradouro',
                df.columns[6]: 'cod_logradouro',
                df.columns[7]: 'n_fachada',
                df.columns[8]: 'comp_1',
                df.columns[9]: 'comp_2',
                df.columns[10]: 'comp_3',
                df.columns[11]: 'regiao',
                df.columns[12]: 'cep',
                df.columns[13]: 'total_hps',
            }

            df = df.rename(columns=colunas_mapeamento)

            # Converter CEP para string sem hífen (normalizar)
            df['cep'] = df['cep'].astype(str).str.replace('-', '').str.replace('.', '').str.strip()

            # Converter cod_logradouro para string
            df['cod_logradouro'] = df['cod_logradouro'].astype(str).str.strip()

            # Converter total_hps para inteiro (tratando valores nulos)
            df['total_hps'] = pd.to_numeric(df['total_hps'], errors='coerce').fillna(0).astype(int)

            # Remover linhas onde viabilidade_atual é vazia ou é o próprio header repetido
            df = df[df['viabilidade_atual'].notna()]
            df = df[df['viabilidade_atual'] != 'VIABILIDADE_ATUAL']

            # Converter para lista de dicionários
            enderecos = df.to_dict('records')
            todos_enderecos.extend(enderecos)

            logger.info(f"Aba '{sheet_name}': {len(enderecos)} registros processados")

        logger.info(f"Total de registros processados: {len(todos_enderecos)}")
        return todos_enderecos

    except Exception as e:
        logger.error(f"Erro ao processar planilha: {str(e)}")
        raise


def normalizar_cep(cep: str) -> str:
    """
    Normaliza o CEP removendo hífen, pontos e espaços.

    Args:
        cep: CEP original

    Returns:
        CEP normalizado (apenas números)
    """
    return cep.replace('-', '').replace('.', '').replace(' ', '').strip()


def formatar_cep(cep: str) -> str:
    """
    Formata o CEP no padrão XXXXX-XXX.

    Args:
        cep: CEP sem formatação

    Returns:
        CEP formatado
    """
    cep_limpo = normalizar_cep(cep)
    if len(cep_limpo) == 8:
        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
    return cep_limpo


def validar_cep(cep: str) -> bool:
    """
    Valida se o CEP tem formato válido.

    Args:
        cep: CEP a ser validado

    Returns:
        True se válido, False caso contrário
    """
    cep_limpo = normalizar_cep(cep)
    return len(cep_limpo) == 8 and cep_limpo.isdigit()
