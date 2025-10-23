"""
Script para carregar a planilha Excel automaticamente (busca arquivo na pasta D:/Alga).
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services import endereco_service
from app.database import db


def main():
    """Função principal do script."""

    # Buscar arquivo Excel na pasta D:/Alga
    base_path = Path("D:/Alga")
    excel_files = list(base_path.glob("*.xlsx"))

    if not excel_files:
        print("[ERRO] Nenhum arquivo .xlsx encontrado em D:/Alga")
        sys.exit(1)

    planilha_path = excel_files[0]

    print("=" * 60)
    print("CARREGADOR DE PLANILHA - API DE VIABILIDADE")
    print("=" * 60)
    print(f"\nPlanilha encontrada em: D:/Alga")
    print(f"Tamanho: {planilha_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Confirmar antes de prosseguir
    resposta = input("\n[ATENCAO] Isso ira LIMPAR todos os dados existentes. Continuar? (s/N): ")
    if resposta.lower() != 's':
        print("[CANCELADO] Operacao cancelada")
        sys.exit(0)

    print("\n[PROCESSANDO] Iniciando processamento...")

    # Processar planilha
    resultado = endereco_service.upload_planilha(planilha_path)

    print("\n" + "=" * 60)
    if resultado.sucesso:
        print("[SUCESSO] Planilha processada com sucesso!")
        print(f"Registros inseridos: {resultado.registros_inseridos:,}")
        print(f"Tempo de processamento: {resultado.tempo_processamento:.2f}s")

        # Mostrar estatísticas
        stats = db.get_stats()
        print(f"\nESTATISTICAS:")
        print(f"   Total de registros: {stats['total_registros']:,}")

        print(f"\n   Por viabilidade:")
        for viab, count in stats['por_viabilidade'].items():
            print(f"      {viab}: {count:,}")

        print(f"\n   Por municipio (Top 10):")
        for mun, count in sorted(
            stats['por_municipio'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]:
            print(f"      {mun}: {count:,}")

    else:
        print("[ERRO] Falha ao processar planilha!")
        print(f"   {resultado.mensagem}")

    print("=" * 60)


if __name__ == "__main__":
    main()
