"""
Módulo de gerenciamento do banco de dados SQLite.
"""
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho do banco de dados
DB_PATH = Path(__file__).parent.parent / "data" / "enderecos.db"


class Database:
    """Classe para gerenciar conexões e operações no banco de dados SQLite."""

    def __init__(self, db_path: Path = DB_PATH):
        """
        Inicializa a conexão com o banco de dados.

        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()

    def get_connection(self) -> sqlite3.Connection:
        """
        Cria e retorna uma conexão com o banco de dados.

        Returns:
            Conexão SQLite
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        return conn

    def _create_tables(self):
        """Cria as tabelas necessárias se não existirem."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Criar tabela de endereços
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enderecos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    viabilidade_atual TEXT,
                    uf TEXT,
                    municipio TEXT,
                    localidade TEXT,
                    bairro TEXT,
                    logradouro TEXT,
                    cod_logradouro TEXT,
                    n_fachada TEXT,
                    comp_1 TEXT,
                    comp_2 TEXT,
                    comp_3 TEXT,
                    regiao TEXT,
                    cep TEXT,
                    total_hps INTEGER
                )
            """)

            # Criar índices para performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_cep_cod
                ON enderecos(cep, cod_logradouro)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_cep
                ON enderecos(cep)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_cod_logradouro
                ON enderecos(cod_logradouro)
            """)

            conn.commit()
            logger.info("Tabelas e índices criados com sucesso")

    def insert_enderecos(self, enderecos: List[Dict[str, Any]]) -> int:
        """
        Insere múltiplos endereços no banco de dados.

        Args:
            enderecos: Lista de dicionários com dados dos endereços

        Returns:
            Número de registros inseridos
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO enderecos (
                    viabilidade_atual, uf, municipio, localidade, bairro,
                    logradouro, cod_logradouro, n_fachada, comp_1, comp_2,
                    comp_3, regiao, cep, total_hps
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            data = [
                (
                    e.get('viabilidade_atual'),
                    e.get('uf'),
                    e.get('municipio'),
                    e.get('localidade'),
                    e.get('bairro'),
                    e.get('logradouro'),
                    e.get('cod_logradouro'),
                    e.get('n_fachada'),
                    e.get('comp_1'),
                    e.get('comp_2'),
                    e.get('comp_3'),
                    e.get('regiao'),
                    e.get('cep'),
                    e.get('total_hps')
                )
                for e in enderecos
            ]

            cursor.executemany(insert_query, data)
            conn.commit()

            inserted_count = cursor.rowcount
            logger.info(f"{inserted_count} endereços inseridos com sucesso")
            return inserted_count

    def consultar_viabilidade(
        self,
        cep: str,
        n_fachada: str
    ) -> Optional[Dict[str, Any]]:
        """
        Consulta a viabilidade de um endereço pelo CEP e número da fachada.

        Args:
            cep: CEP (com ou sem hífen)
            n_fachada: Número da fachada

        Returns:
            Dicionário com dados do endereço ou None se não encontrado
        """
        # Normalizar CEP (remover hífen se existir)
        cep_normalizado = cep.replace('-', '').replace('.', '').strip()
        n_fachada_normalizado = str(n_fachada).strip()

        logger.info(f"[DB] Consultando: CEP={cep_normalizado}, N_FACHADA={n_fachada_normalizado}")

        with self.get_connection() as conn:
            cursor = cursor.cursor()

            # Verificar total de registros no banco
            cursor.execute("SELECT COUNT(*) as total FROM enderecos")
            total = cursor.fetchone()['total']
            logger.info(f"[DB] Total de registros no banco: {total}")

            # Verificar se existe algum registro com esse CEP
            cursor.execute("SELECT COUNT(*) as count FROM enderecos WHERE cep = ?", (cep_normalizado,))
            count_cep = cursor.fetchone()['count']
            logger.info(f"[DB] Registros com CEP {cep_normalizado}: {count_cep}")

            # Verificar se existe algum registro com esse número
            cursor.execute("SELECT COUNT(*) as count FROM enderecos WHERE n_fachada = ?", (n_fachada_normalizado,))
            count_num = cursor.fetchone()['count']
            logger.info(f"[DB] Registros com N_FACHADA {n_fachada_normalizado}: {count_num}")

            # DEBUG: Mostrar alguns registros com esse CEP
            cursor.execute("""
                SELECT n_fachada, logradouro, municipio
                FROM enderecos
                WHERE cep = ?
                LIMIT 5
            """, (cep_normalizado,))
            exemplos = cursor.fetchall()
            logger.info(f"[DB] DEBUG - Exemplos de n_fachada para CEP {cep_normalizado}:")
            for ex in exemplos:
                n_fach = ex['n_fachada']
                logger.info(f"[DB]   n_fachada='{n_fach}' | len={len(str(n_fach))} | logradouro={ex['logradouro']}")

            query = """
                SELECT
                    viabilidade_atual,
                    uf,
                    municipio,
                    localidade,
                    bairro,
                    logradouro,
                    cod_logradouro,
                    n_fachada,
                    comp_1,
                    comp_2,
                    comp_3,
                    regiao,
                    cep,
                    total_hps
                FROM enderecos
                WHERE cep = ? AND n_fachada = ?
                LIMIT 1
            """

            cursor.execute(query, (cep_normalizado, n_fachada_normalizado))
            row = cursor.fetchone()

            if row:
                logger.info(f"[DB] ✅ Registro encontrado!")
                return dict(row)

            logger.warning(f"[DB] ❌ Nenhum registro encontrado com CEP={cep_normalizado} e N_FACHADA={n_fachada_normalizado}")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas sobre os dados no banco.

        Returns:
            Dicionário com estatísticas
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total de registros
            cursor.execute("SELECT COUNT(*) as total FROM enderecos")
            total = cursor.fetchone()['total']

            # Contagem por viabilidade
            cursor.execute("""
                SELECT viabilidade_atual, COUNT(*) as count
                FROM enderecos
                GROUP BY viabilidade_atual
            """)
            viabilidade_counts = {
                row['viabilidade_atual']: row['count']
                for row in cursor.fetchall()
            }

            # Contagem por município
            cursor.execute("""
                SELECT municipio, COUNT(*) as count
                FROM enderecos
                GROUP BY municipio
                ORDER BY count DESC
            """)
            municipio_counts = {
                row['municipio']: row['count']
                for row in cursor.fetchall()
            }

            return {
                'total_registros': total,
                'por_viabilidade': viabilidade_counts,
                'por_municipio': municipio_counts
            }

    def clear_all(self):
        """Limpa todos os dados da tabela de endereços."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM enderecos")
            conn.commit()
            logger.info("Banco de dados limpo com sucesso")

    def database_exists(self) -> bool:
        """
        Verifica se o banco de dados existe e tem dados.

        Returns:
            True se existe e tem dados, False caso contrário
        """
        if not self.db_path.exists():
            return False

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM enderecos")
            count = cursor.fetchone()['count']
            return count > 0


# Instância global do banco de dados
db = Database()
