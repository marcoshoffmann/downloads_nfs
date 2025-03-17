from loguru import logger
from os import getenv
from dotenv import load_dotenv
load_dotenv()
from time import sleep
from selenium.webdriver.common.by import By
from resources.Browser import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserPortalNacional(Browser):
    def __init__(self) -> None:
        super().__init__(getenv("URL_PORTAL"), getenv("PATH_PORTAL_NACIONAL"), "data_portal", headless=True)

    def login(self, cnpj: str, pwd: str) -> bool:
        self.navegador.get(self.url)

        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="Inscricao"]', message_success='Informou o login', message_error='Não informou o login').send_keys(cnpj)
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="Senha"]', message_success='Informou a senha', message_error='Não informou a senha').send_keys(pwd)
        self.element_response(metodo=By.XPATH, identificador_elemento='/html/body/section/div/div/div[2]/div[2]/div[1]/div/form/div[3]/button', message_success='Clicou em entrar', message_error='Não clicou em entrar', click=True)
        return True

    # def next(self):
    #     button_next = self.element_response(metodo=By.XPATH, identificador_elemento='/html/body/section/div/div/div[2]/div[2]/div[1]/div/form/div[3]/button', message_success='Clicou em entrar', message_error='Não clicou em entrar', repeticoes=30)
    #     if button_next and not button_next.get_attribute("class").__eq__('disabled'):
    #         button_next.click()
    #         return True
    def next(self):
        for _ in range(30):
            logger.info(f'TENTATIVA: {_ + 1}')
            try:
                if not self.navegador.find_element(By.CSS_SELECTOR, "a i.fa-angle-right").find_element(By.XPATH, "ancestor::li").get_attribute("class").__eq__('disabled'):
                    self.navegador.find_element(By.CSS_SELECTOR, 'a i.fa-angle-right').click()
                    logger.info('Clicou em Próximo')
                    return True
                else:
                    return False
            except Exception as error_x:
                logger.error(f'Não clicou em Próximo: {error_x}')
                sleep(1)

    def access_notas(self, tipo: str) -> None:
        botao = False
        if tipo.__eq__("prestador"):
            xpath = '//*[@id="navbar"]/ul/li[3]/a'
        elif tipo.__eq__("tomador"):
            xpath = '//*[@id="navbar"]/ul/li[4]/a'
        botao = self.element_response(metodo=By.XPATH, identificador_elemento=xpath, message_success='Clicou em emitidas', message_error='Não clicou em emitidas', repeticoes=40, click=True)
        if not botao:
            return

        wait = WebDriverWait(self.navegador, 40)
        for elemento in self.navegador.find_elements(By.TAG_NAME, 'tr'):
            baixar = False
            campos = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
            for item in campos:
                # print(f'ITEM: {item}')
                if item.get_attribute("class") == 'td-data' and item.text.split("/")[1] == self.timeconsult.updated_month and item.text.split("/")[-1] == self.timeconsult.updated_year:
                    date = item.text
                    baixar = True
                elif item.get_attribute("class") == 'td-data' and int(item.text.split("/")[1]) < int(self.timeconsult.updated_month) and item.text.split("/")[-1] <= self.timeconsult.updated_year:
                    sleep(8)
                    return
                elif item.get_attribute("class") == 'td-data' and item.text.split("/")[-1] < self.timeconsult.updated_year:
                    sleep(8)
                    return
                if item.get_attribute("class") == 'td-opcoes' and baixar:
                    botao_baixar = item.find_elements(By.TAG_NAME, 'a')
                    botao_baixar[0].click()
                    sleep(4)
                    try:
                        if tipo == 'prestador':
                            self.navegador.get(botao_baixar[4].get_attribute("href"))
                            self.quantidade[tipo] += 1
                            logger.info('Clicou em Download NFSe')
                        elif tipo == 'tomador':
                            self.navegador.get(botao_baixar[2].get_attribute("href"))
                            self.quantidade[tipo] += 1
                            logger.info('Clicou em Download NFSe')
                    except IndexError:
                        self.navegador.get(botao_baixar[2].get_attribute("href"))
                        self.quantidade[tipo] += 1
                        print('Clicou em Download NFSe Cancelada')
            if not self.next():
                return

    def baixar_tudo(self):
        self.access_notas(tipo='prestador')
        self.access_notas(tipo='tomador')
        return True
