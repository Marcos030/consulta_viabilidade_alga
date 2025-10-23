"""
Script para carregar a planilha Excel no banco de dados.

Usage:
    python scripts/load_excel.py <caminho_planilha>

Example:
    python scripts/load_excel.py "D:/Alga/Enderecos Nordeste.xlsx"
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
    if len(sys.argv) < 2:
        print("[ERRO] Caminho da planilha nao fornecido")
        print("\nUso:")
        print('  python scripts/load_excel.py "D:/Alga/Enderecos Nordeste.xlsx"')
        sys.exit(1)

    planilha_path = Path(sys.argv[1])

    if not planilha_path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {planilha_path}")
        sys.exit(1)

    print("=" * 60)
    print("CARREGADOR DE PLANILHA - API DE VIABILIDADE")
    print("=" * 60)
    print(f"\nPlanilha: {planilha_path}")
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

        print(f"\n   Por municipio:")
        for mun, count in sorted(
            stats['por_municipio'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]:  # Top 10
            print(f"      {mun}: {count:,}")

    else:
        print("[ERRO] Falha ao processar planilha!")
        print(f"   {resultado.mensagem}")

    print("=" * 60)


if __name__ == "__main__":
    main()
