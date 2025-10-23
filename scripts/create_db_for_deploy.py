"""
Script para criar banco de dados SQLite populado para deploy.

Este script:
1. Carrega a planilha Excel local
2. Popula o banco de dados SQLite
3. Gera o arquivo data/enderecos.db pronto para deploy

Usage:
    python scripts/create_db_for_deploy.py
"""
import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services import endereco_service
from app.database import db

def main():
    """Gera banco de dados populado."""
    print("=" * 70)
    print("CRIAR BANCO DE DADOS PARA DEPLOY")
    print("=" * 70)

    # Caminho da planilha
    planilha_path = Path(__file__).parent.parent / "data" / "uploads" / "enderecos_nordeste.xlsx"

    if not planilha_path.exists():
        print(f"\n❌ ERRO: Planilha não encontrada!")
        print(f"📁 Esperado em: {planilha_path}")
        print("\n💡 Coloque o arquivo 'enderecos_nordeste.xlsx' na pasta data/uploads/")
        return 1

    print(f"\n📄 Planilha encontrada: {planilha_path.name}")
    print(f"📊 Tamanho: {planilha_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Confirmar
    print("\n⚠️  ATENÇÃO: Isso vai LIMPAR o banco atual e criar um novo!")
    resposta = input("Continuar? (s/N): ")

    if resposta.lower() != 's':
        print("\n❌ Operação cancelada.")
        return 0

    print("\n🔄 Processando planilha...")
    print("⏱️  Isso pode demorar alguns minutos...\n")

    # Processar planilha
    resultado = endereco_service.upload_planilha(planilha_path)

    if resultado.sucesso:
        print("\n" + "=" * 70)
        print("✅ SUCESSO!")
        print("=" * 70)
        print(f"📊 Registros inseridos: {resultado.registros_inseridos:,}")
        print(f"⏱️  Tempo: {resultado.tempo_processamento:.2f}s")

        # Verificar arquivo gerado
        db_path = Path(__file__).parent.parent / "data" / "enderecos.db"
        if db_path.exists():
            db_size = db_path.stat().st_size / 1024 / 1024
            print(f"💾 Banco gerado: {db_path}")
            print(f"📏 Tamanho: {db_size:.2f} MB")

            print("\n" + "=" * 70)
            print("📝 PRÓXIMOS PASSOS:")
            print("=" * 70)
            print("1. O arquivo 'data/enderecos.db' está pronto!")
            print("2. Execute: git add data/enderecos.db")
            print("3. Execute: git commit -m 'Add: banco populado para deploy'")
            print("4. Execute: git push")
            print("5. O Render vai usar esse banco já populado!")
            print("=" * 70)

        return 0
    else:
        print(f"\n❌ ERRO: {resultado.mensagem}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
