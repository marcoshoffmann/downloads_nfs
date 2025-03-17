from loguru import logger
import mysql.connector

class MySQLDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexao: None = None
    
    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logger.info("Conexão com o banco de dados estabelecida!")
        except mysql.connector.Error as error_x:
            logger.error(f"Erro ao conectar: {error_x}")
            self.conexao = None
    
    def fechar_conexao(self):
        if self.conexao:
            self.conexao.close()
            logger.info("Conexão fechada.")

    def ler_dados(self, query: str) -> None:
        self.conectar()
        if self.conexao:
            logger.info(f'QUERY: {query}')
            cursor = self.conexao.cursor()
            try:
                cursor.execute(query)
                resultados = cursor.fetchall()
                return resultados
            except mysql.connector.Error as error_x:
                logger.error(f"Erro ao ler dados: {error_x}")
                return None
            finally:
                cursor.close()
            self.fechar_conexao()

    def inserir_dados(self, query: str):
        self.conectar()
        if self.conexao:
            logger.info(f'QUERY: {query}')
            cursor = self.conexao.cursor()
            sql = query
            try:
                cursor.execute(sql)
                self.conexao.commit()
                logger.info("Dados inseridos com sucesso!")
            except mysql.connector.Error as error_x:
                logger.error(f"Erro ao inserir dados: {error_x}")
            finally:
                cursor.close()

    def atualizar_dados(self, query: str) -> None:
        self.conectar()
        if self.conexao:
            logger.info(f'QUERY: {query}')
            cursor = self.conexao.cursor()
            try:
                cursor.execute(query)
                self.conexao.commit()
                logger.info("Dados atualizados com sucesso!")
            except mysql.connector.Error as error_x:
                logger.error(f"Erro ao atualizar dados: {error_x}")
            finally:
                cursor.close()
            self.fechar_conexao()

    def deletar_dados(self, query: str) -> None:
        self.conectar()
        if self.conexao:
            logger.info(f'QUERY: {query}')
            cursor = self.conexao.cursor()
            try:
                cursor.execute(query)
                self.conexao.commit()
                logger.info("Dados deletados com sucesso!")
            except mysql.connector.Error as error_x:
                logger.error(f"Erro ao deletar dados: {error_x}")
            finally:
                cursor.close()
            self.fechar_conexao()
    
    def execute_sql(self, query: str) -> None:
        self.conectar()
        if self.conexao:
            logger.info(f'QUERY: {query}')
            cursor = self.conexao.cursor()
            try:
                cursor.execute(query)
                self.conexao.commit()
                logger.info("Dados deletados com sucesso!")
            except mysql.connector.Error as error_x:
                logger.error(f"Erro ao deletar dados: {error_x}")
            finally:
                cursor.close()
            self.fechar_conexao()
