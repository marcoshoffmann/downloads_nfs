from loguru import logger
from os import getcwd
from dotenv import load_dotenv
load_dotenv()
from time import sleep
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from random import uniform
from selenium.webdriver.common.action_chains import ActionChains
from re import sub
from selenium.webdriver.support.ui import WebDriverWait
from resources.TimeConsult import TimeConsult
from pyautogui import keyDown
from resources.PathManager import PathManager
from selenium.webdriver.common.keys import Keys

class Browser:
    def __init__(self, url, path_download, path_chrome, headless: bool = True) -> None:
        self.timeconsult = TimeConsult()
        self.pathmanager = PathManager()
        self.url = url
        self.path_download = path_download.replace('\\\\', '\\')
        self.path_chrome = path_chrome
        self.pathmanager.delete_data(f'.\\Chrome\\{self.path_chrome}')
        self.headless = headless
        self.chrome_options = uc.ChromeOptions()
        if self.headless:
            self.chrome_options.add_argument("--headless=new")
            self.chrome_options.add_argument("--window-size=1920X1080")
        self.chrome_options.add_argument("--start-fullscreen")
        self.chrome_options.add_argument(f"--unsafely-treat-insecure-origin-as-secure={self.url}")
        self.chrome_options.add_argument(rf"--profile-directory=Default")
        self.chrome_options.add_experimental_option("prefs", {"download.default_directory": self.path_download, "profile.default_content_setting_values.popups": 1})
        self.chrome_options.add_argument(f"--load-extension=G:\\Ti\\PROJETOS\\anti_captcha071")
        self.timeconsult = TimeConsult()
        self.navegador = None
        self.action = ActionChains(self.navegador)
        self.acabou = False
        self.wait = WebDriverWait(self.navegador, 40)
        self.quantidade = {'prestador': 0, 'tomador': 0}
        
    def start_browser(self):
        self.navegador = uc.Chrome(user_data_dir = rf'{getcwd()}\Chrome\{self.path_chrome}', headless=False, use_subprocess=False, options=self.chrome_options, suppress_welcome=True, driver_executable_path=f'.\\Chrome\\chromedriver-win64\\chromedriver.exe', browser_executable_path=f'.\\Chrome\\chrome-win64\\chrome.exe')

    def keyboard(self, element, word: str, key_down: bool, mask: bool, verify: bool = True, clean: bool = True, rem: str = None) -> None:
        if clean and element:
            element.clear()
        for caract in word:
            sleep(uniform(0.5, 1.5))
            element.send_keys(caract)
            if key_down is True:
                keyDown('right')
                element.click()
        if verify:
            if mask:
                if sub(r"\D", "", element.get_attribute('value')) != word:
                    self.keyboard(element, word, key_down, verify)
            elif not mask and rem is None:
                if element.get_attribute('value') != word:
                    self.keyboard(element, word, key_down, verify)
            elif rem is not None:
                if element.get_attribute('value').replace(rem, "") != word.replace(rem, ""):
                    self.keyboard(element, word, key_down, verify)
            return

    def element_response(self, metodo: By, identificador_elemento: str, message_success: str, message_error: str, repeticoes: int=100000, elemento: any = None, click: bool = False, update: bool = False):
        if elemento is None:
            for _ in range(repeticoes):
                if update and (_ + 1) % 20 == 0:
                    self.navegador.refresh()
                    logger.info('Atualizou a página')
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    if click:
                        self.navegador.find_element(metodo, identificador_elemento).click()
                        logger.info(message_success)
                        return True
                    else:
                        logger.info(message_success)
                        return self.navegador.find_element(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        else:
            for _ in range(repeticoes):
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    elemento.find_element(metodo, identificador_elemento)
                    logger.info(message_success)
                    return elemento.find_element(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        return False
    
    def elements_response(self, metodo: By, identificador_elemento: str, message_success: str, message_error: str, repeticoes: int=100000, elemento: any = None):
        if elemento is None:
            for _ in range(repeticoes):
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    self.navegador.find_elements(metodo, identificador_elemento)
                    logger.info(message_success)
                    return self.navegador.find_elements(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        else:
            for _ in range(repeticoes):
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    elemento.find_elements(metodo, identificador_elemento)
                    logger.info(message_success)
                    return elemento.find_elements(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        return False
