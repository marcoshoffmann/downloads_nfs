from loguru import logger
from os import getenv, getcwd
from dotenv import load_dotenv
load_dotenv()
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from resources.Browser import Browser

class BrowserCachoeirinha(Browser):
    def __init__(self) -> None:
        super().__init__(getenv("URL_PREFEITURA_CACHOEIRINHA"), getenv("PATH_CACHOEIRINHA"), "data_cachoeirinha", headless=False)
        self.acabou = False

    def login(self, cnpj: str, pwd: str) -> bool:
        self.navegador.get(self.url)
        self.keyboard(self.element_response(metodo=By.NAME, identificador_elemento='login_usuario', message_success='Informou o login', message_error='Não informou o login', repeticoes=20), cnpj, key_down=False, mask=False, verify=True, clean=True)
        self.keyboard(self.element_response(metodo=By.NAME, identificador_elemento='senha_usuario', message_success='Informou a senha', message_error='Não informou a senha', repeticoes=20), pwd, key_down=False, mask=False, verify=False, clean=True)
        # input("AQUIIIIIIIIII!!!!!!!!!!!!!!")
        self.element_response(metodo=By.XPATH, identificador_elemento='/html/body/div[1]/div[2]/span[7]/button', message_success='Clicou em entrar', message_error='Não clicou em entrar', repeticoes=20, click=True)

        entrar_info2 = False
        while not entrar_info2:
            try:
                for a in self.navegador.find_elements(By.TAG_NAME, 'a'):
                    if a.text.__eq__('Acessar'):
                        a.click()
                        entrar_info2 = True
                        logger.info('Clicou em entrar2')
                        break
            except Exception as error_x:
                logger.error(f'Não clicou em entrar2: {error_x}')
                sleep(1)
        
        sleep(120)

        print(f'ABA ATUAL: {self.navegador.current_window_handle}')

        abas = self.navegador.window_handles
        print(f'ABAS: {abas}')

        self.navegador.switch_to.window(abas[-1])
        print(f'ABA ATUAL: {self.navegador.current_window_handle}')

        self.fecha_mensagem()

        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="estrutura_menu_conjuntos"]/ul/li[1]/div', message_success='Clicou em left panel', message_error='Não clicou em left panel', click=True)
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="estrutura_menu_conjuntos"]/ul/li[1]/ul/li[2]/div', message_success='Clicou em left panel', message_error='Não clicou em left panel', repeticoes=20, click=True)

        sleep(10)

        self.fecha_mensagem()

        sleep(10)

        return True

    def download_header(self, prestador: str, competencia: str, tipo: str) -> None:
        if tipo.__eq__('PRESTADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="estrutura_menu_sistema"]/ul/li[4]/span', message_success=f'Clicou em aba {prestador}', message_error=f'Não clicou em aba {prestador}', click=True)
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="estrutura_container_sistema"]/ul/li[2]/span', message_success=f'Clicou em gerenciamento {prestador}', message_error=f'Não clicou em aba {prestador}', click=True)
        elif tipo.__eq__('TOMADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="estrutura_menu_sistema"]/ul/li[3]/span', message_success=f'Clicou em aba {prestador}', message_error='Não clicou em aba', click=True)
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="estrutura_container_sistema"]/ul/li[3]/span', message_success=f'Clicou em gerenciamento {prestador}', message_error=f'Não clicou em aba {prestador}', click=True)
    
        prestador_info = False
        while not prestador_info:
            try:
                if tipo.__eq__('PRESTADOR'):
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[1]/tbody/tr/td[2]/span/input[2]').clear()
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[1]/tbody/tr/td[2]/span/input[2]').send_keys(prestador)
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[1]/tbody/tr/td[2]/span/input[2]').send_keys(Keys.ENTER)
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[1]/tbody/tr/td[2]/span/input[2]').send_keys(Keys.ENTER)
                    prestador_info = True
                    logger.info(f'Informou o {tipo}')
                    break
                elif tipo.__eq__('TOMADOR'):
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input[2]').clear()
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input[2]').send_keys(prestador)
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input[2]').send_keys(Keys.ENTER)
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input[2]').send_keys(Keys.ENTER)
                    prestador_info = True
                    logger.info(f'Informou o {tipo}')
                    break
            except Exception as error_x:
                logger.error(f'Não informou o {tipo}: {error_x}')
                sleep(1)
                
        competencia_info = False
        while not competencia_info:
            try:
                if tipo.__eq__('PRESTADOR'):
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input').clear()
                    self.navegador.execute_script("""arguments[0].value = arguments[1];arguments[0].dispatchEvent(new Event('input'));arguments[0].dispatchEvent(new Event('blur'));""", self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input'), competencia)
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input').send_keys(Keys.ENTER)
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input').send_keys(Keys.ENTER)
                    competencia_info = True
                    logger.info('Informou a competencia')
                    break
                elif tipo.__eq__('TOMADOR'):
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[3]/tbody/tr/td[2]/span/input').clear()
                    self.navegador.execute_script("""arguments[0].value = arguments[1];arguments[0].dispatchEvent(new Event('input'));arguments[0].dispatchEvent(new Event('blur'));""", self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[3]/tbody/tr/td[2]/span/input'), competencia)
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[3]/tbody/tr/td[2]/span/input').send_keys(Keys.ENTER)
                    competencia_info = True
                    sleep(6)
                    self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[3]/tbody/tr/td[2]/span/input').send_keys(Keys.ENTER)
                    competencia_info = True
                    logger.info('Informou a competencia')
                    break
            except Exception as error_x:
                logger.error(f'Não informou a competencia: {error_x}')
                sleep(1)
        

        if tipo.__eq__('PRESTADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input[2]', message_success='', message_error='').send_keys(Keys.ENTER)
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[3]/div/span/span[2]', message_success=f'Clicou em consultar {tipo}', message_error=f'Não clicou em consultar {tipo}', click=True)
            todas_info = self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66020_101_1"]/article/div[1]/div[2]/table/tbody/tr[1]/td[1]/button', message_success=f'Selecionou todas {tipo}', message_error=f'Não selecionou todas {tipo}', repeticoes=20, click=True)
        elif tipo.__eq__('TOMADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[3]/div/span/span[2]', message_success='', message_error='').send_keys(Keys.ENTER)
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[3]/div/span/span[2]', message_success=f'Clicou em consultar {tipo}', message_error=f'Não clicou em consultar {tipo}', click=True)
            todas_info = self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66069_101_1"]/article/div[1]/div[2]/table/tbody/tr[1]/td[1]/button', message_success=f'Selecionou todas {tipo}', message_error=f'Não selecionou todas {tipo}', repeticoes=20, click=True)

        self.tipo = tipo
        
        if todas_info is True:
            self.download()
        else:
            logger.info('Não há notas para download')

        if self.tipo.__eq__('PRESTADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="janela_66020_101_1"]/div[2]/header/aside/span[1]/input', message_success=f'Clicou em fechar {tipo}', message_error=f'Não clicou em fechar {tipo}', click=True)
            sleep(20)
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[2]/div[1]/span[2]/span[1]', message_success=f'Clicou em fechar {tipo}', message_error=f'Não clicou em fechar {tipo}', click=True, repeticoes=20)
        elif self.tipo.__eq__('TOMADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="janela_66069_101_1"]/div[2]/header/aside/span[1]/input', message_success=f'Clicou em fechar {tipo}', message_error=f'Não clicou em fechar {tipo}', click=True)
            sleep(20)
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[2]/div[2]/span[5]/span[1]', message_success=f'Clicou em fechar {tipo}', message_error=f'Não clicou em fechar {tipo}', click=True, repeticoes=20)
        
        
    def download(self) -> None:
        sleep(20)
        if self.tipo.__eq__('PRESTADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[2]/div[1]/span[2]/span[1]', message_success=f'Clicou em Download {self.tipo}', message_error=f'Não clicou em Download {self.tipo}', click=True, repeticoes=20)
        elif self.tipo.__eq__('TOMADOR'):
            self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66069_101_1"]/article/div[1]/aside[2]/div[2]/span[5]/span[1]', message_success=f'Clicou em Download {self.tipo}', message_error=f'Não clicou em Download {self.tipo}', click=True, repeticoes=20)
        
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="context_menu"]/table/tbody/tr[3]/td/span/span', message_success=f'Clicou em xml {self.tipo}', message_error=f'Não clicou em xml {self.tipo}', click=True, repeticoes=20)
        self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="estrutura_container_sistema"]/div[4]/section/footer/button[1]', message_success=f'Clicou em SIM {self.tipo}', message_error=f'Não clicou em SIM {self.tipo}', click=True, repeticoes=20)

        if self.tipo.__eq__('PRESTADOR'):
            if self.element_response(metodo=By.XPATH, identificador_elemento='//*[@id="conteudo_66020_101_1"]/article/div[1]/footer/div[1]/table/tbody/tr/td[5]/span[2]/input', message_success='Encontrou avançar', message_error='Não encontrou avançar', repeticoes=20).get_attribute("aria-description").__eq__('ativado'):
                avancar_info = True
                self.download()
                logger.info('Clicou em avancar')
            else:
                logger.info('FINALIZOU')
        elif self.tipo.__eq__('TOMADOR'):
            if self.navegador.find_element(By.XPATH, '//*[@id="conteudo_66069_101_1"]/article/div[1]/footer/div[1]/table/tbody/tr/td[5]/span[2]/input').get_attribute("aria-description").__eq__('ativado'):
                avancar_info = True
                logger.info('Clicou em avancar')
                self.download()
            else:
                logger.info('FINALIZOU')

        self.erro_exibicao()

    def erro_exibicao(self) -> None:
        for _ in range(10):
            try:
                self.navegador.find_element(By.XPATH, '//*[@id="estrutura_container_sistema"]/div[4]/section/footer/button').click()
                logger.info('Fechou a mensagem de erro')
                break
            except Exception as error_x:
                logger.info(f'Não fechou a mensagem de erro: {error_x}')
                sleep(1)


    def fecha_mensagem(self) -> None:
        self.navegador.execute_script("""
        try {
            console.log("Tentando criar variável...");
            var teste = document.getElementsByTagName("button");
            console.log("Botões encontrados:", teste.length);
            teste[teste.length - 1].click();
        } catch (error) {
            console.log("Erro no script:", error);
        }
        """)
    
    def baixar_prestados(self, cnpj: str) -> None:
        self.download_header(prestador=cnpj, competencia=self.timeconsult.competence_start, tipo='PRESTADOR')
    def baixar_tomados(self, cnpj: str) -> None:
        self.download_header(prestador=cnpj, competencia=self.timeconsult.competence_start, tipo='TOMADOR')
