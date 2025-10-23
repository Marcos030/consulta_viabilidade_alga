"""
Script de inicialização para carregar planilha automaticamente.
Executa antes do uvicorn iniciar.
"""
import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar módulos da aplicação
from app.database import db
from app.services import endereco_service


def main():
    """Carrega planilha se banco estiver vazio."""
    logger.info("=" * 60)
    logger.info("STARTUP: Verificando banco de dados...")
    logger.info("=" * 60)

    try:
        # Verificar se banco tem dados
        tem_dados = db.database_exists()

        if tem_dados:
            stats = db.get_stats()
            total = stats.get('total_registros', 0)
            logger.info(f"✅ Banco já contém {total:,} registros")
            logger.info("✅ Pulando carregamento de planilha")
            return 0

        logger.info("⚠️  Banco vazio - carregando planilha...")

        # Caminho da planilha
        planilha_path = Path(__file__).parent / "data" / "uploads" / "enderecos_nordeste.xlsx"

        if not planilha_path.exists():
            logger.error(f"❌ Planilha não encontrada: {planilha_path}")
            logger.error("❌ Continuando sem dados...")
            return 1

        logger.info(f"📄 Planilha: {planilha_path}")
        logger.info(f"📊 Tamanho: {planilha_path.stat().st_size / 1024 / 1024:.2f} MB")
        logger.info("🔄 Processando... (pode demorar 2-3 minutos)")

        # Processar planilha
        resultado = endereco_service.upload_planilha(planilha_path)

        if resultado.sucesso:
            logger.info("=" * 60)
            logger.info(f"✅ SUCESSO: {resultado.registros_inseridos:,} registros carregados")
            logger.info(f"⏱️  Tempo: {resultado.tempo_processamento:.2f}s")
            logger.info("=" * 60)
            return 0
        else:
            logger.error(f"❌ ERRO: {resultado.mensagem}")
            return 1

    except Exception as e:
        logger.error(f"❌ Erro fatal no startup: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
