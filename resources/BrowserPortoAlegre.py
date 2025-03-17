from loguru import logger
from os import getenv
from dotenv import load_dotenv
load_dotenv()
from time import sleep
from selenium.webdriver.common.by import By
from resources.Browser import Browser

class BrowserPortoAlegre(Browser):
    def __init__(self) -> None:
        super().__init__(getenv("URL_PREFEITURA_PORTO_ALEGRE"), getenv("PATH_PORTO_ALEGRE"), "data_poa", headless=False)
        self.cabou = False

    def login(self, cnpj: str, pwd: str) -> None:
        self.navegador.get(self.url)
        for button in self.elements_response(metodo=By.TAG_NAME, identificador_elemento='button', message_success='Clicou para fechar a mensagem', message_error='Não clicou para fechar a mensagem', repeticoes=40):
            if not button.text.__eq__(""): button.click()
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="form"]/div[1]/a/img', message_success='Clicou em autenticação', message_error='Não clicou em autenticação', click=True, update=True)
        self.keyboard(self.element_response(metodo=By.NAME, identificador_elemento='username', message_success='Preencheu o CNPJ', message_error='Não preencheu o CNPJ', update=True, repeticoes=40), word=cnpj, key_down=False, mask=False)
        self.keyboard(self.element_response(metodo=By.NAME, identificador_elemento='password', message_success='Preencheu a senha', message_error='Não preencheu a senha', repeticoes=40), word=pwd, key_down=False, mask=False, verify=False)
        self.element_response(metodo=By.NAME, identificador_elemento='envia', message_success='Clicou em entrar', message_error='Não clicou em entrar', click=True, repeticoes=40)
        submenu = self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="nav"]/div[2]/a/img[1]', message_success='Encontrou Consulta', message_error='Não encontrou Consulta', repeticoes=20, click=True)
        if not submenu:
            self.new_login()
            return 'ERRO NO LOGIN'
        consultar_prestador = self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="nav"]/div[2]/div/a[2]', message_success='Clicou em Consulta Prestador', message_error='Não clicou em Consulta Prestador', repeticoes=20, click=True)
        if not consultar_prestador:
            credenciamento = self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="mainContent"]/img', message_success='Achou mensagem de credenciamento', message_error='Não achou mensagem de credenciamento', repeticoes=20)
            if credenciamento:
                self.new_login()
                return 'CREDENCIAR EMISSÃO'
        return True

    def escolhe_modalidade(self, terceiro: str):
        self.terceiro = terceiro
        if self.terceiro == 'tomador':
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="form:perfil:1"]', message_success='Clicou em tomador', message_error='Não clicou em tomador', click=True)
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="form:bt_procurar_NFS-e"]', message_success='Clicou em Consultar', message_error='Não clicou em Consultar', click=True)    
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="topo_aba2"]/a', message_success='Clicou em Pesquisa Avançada', message_error='Não clicou em Pesquisa Avançada', click=True)
        self.navegador.execute_script("arguments[0].value = arguments[1];", self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="form:dtCompetenciaInicial"]', message_success='Preencheu a data inicial', message_error='Não preencheu a data inicial'), self.timeconsult.updated_competence_start)
        self.navegador.execute_script("arguments[0].value = arguments[1];", self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="form:dtCompetenciaFinal"]', message_success='Preencheu a data final', message_error='Não preencheu a data final'), self.timeconsult.updated_competence_end)
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="form:bt_procurar_NFS-e"]', message_success='Clicou em Consultar', message_error='Não clicou em Consultar', click=True)
        if self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="mensagem"]/div/ul/li/text()', message_success='', message_error='', repeticoes=5):
            return
        elementos = self.elements_response(metodo=By.TAG_NAME, identificador_elemento='td', message_success='Encontrou os elementos para o id', message_error='Não encontrou os elementos para o id', repeticoes=20)
        if len(elementos).__gt__(44):
            if elementos[44].get_attribute("id").__contains__(":"):
                self.id = elementos[44].get_attribute("id").split(":")[1]
                return True
        logger.info('Não foram localizadas notas fiscais')

    def download(self):
        self.tentativas = 0
        if not self.acabou:
            for _ in range(10):
                if not self.acabou:
                    while True:
                        try:
                            error_msg = self.navegador.find_elements(By.TAG_NAME, 'h1')[-1]
                            if error_msg.value == 'Ocorreu um erro inesperado na aplicação. Tente realizar a operação novamente.':
                                self.navegador.back()
                        except:
                            try:
                                self.navegador.find_element(By.XPATH, f'//*[@id="form:{self.id}:listaNotas:{self.cont}:bt_download"]').click()
                                logger.info('Baixou a nota')
                                self.quantidade[self.terceiro] += 1
                                self.cont += 1
                                print(f'SELF.QUANTIDADE[{self.terceiro}]: {self.quantidade[self.terceiro]}')
                                break
                            except Exception as error_x:
                                logger.error(f'Não baixou a nota: {error_x}')
                                sleep(1)
                        self.tentativas += 1
                        if self.tentativas == 10:
                            self.acabou = True
                            logger.info('FINALIZOU!')
                            break

    def next(self):
        try:
            for tag in self.navegador.find_elements(By.TAG_NAME, 'td'):
                if tag.get_attribute("onclick") == "Event.fire(this, 'rich:datascroller:onscroll', {'page': 'next'});":
                    tag.click()
                    logger.info('Próxima página')
                    break
        except Exception as error_x:
            logger.error(f'Página não localizada')
            self.acabou = True
            sleep(1)

    def new_login(self):
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="identificacao"]/table/tbody/tr/td[2]/a', message_success='Clicou em sair', message_error='Não clicou em sair', repeticoes=40, click=True)
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="mensagem"]/div/p[4]/a', message_success='Clicou em voltar para o início', message_error='Não clicou em voltar para o início', repeticoes=40, click=True)

    def baixar_tudo(self) -> None:
        self.cont = 0
        modalidade = self.escolhe_modalidade(terceiro='prestador')
        if modalidade:
            while not self.acabou:
                self.download()
                self.next()
            self.acabou = False
        self.cont = 0
        modalidade = self.escolhe_modalidade(terceiro='tomador')
        if modalidade:
            while not self.acabou:
                self.download()
                self.next()
            sleep(5)
        self.new_login()
        return True
