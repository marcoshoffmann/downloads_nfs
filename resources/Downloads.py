from os import getenv
from use_cases.MySQLDB import MySQLDB
from queries.querys import atualiza_prefeitura, atualiza_nacional, consulta_municipal, consulta_nacional, atualiza_robo_notas
from resources.BrowserPortoAlegre import BrowserPortoAlegre
from resources.BrowserCachoeirinha import BrowserCachoeirinha
from resources.BrowserPortalNacional import BrowserPortalNacional
from resources.Xml import Xml
from resources.TimeConsult import TimeConsult
from time import sleep
from resources.FilesManager import FilesManager
from datetime import datetime
from resources.PathManager import PathManager
from os import execv, system
from sys import exit

class Downloads:
    def __init__(self):
        self.timeconsult = TimeConsult()
        self.mysqldb = MySQLDB(host=getenv("MY_HOST"), user=getenv("MY_USER"), password=getenv("MY_PWD"), database=getenv("MY_DATABASE"))
        self.xml = Xml()
        self.filesmanager = FilesManager()
        self.pathmanager = PathManager()
        self.browserportoalegre = None
        self.browserportalnacional = None

    def iniciar_processo(self, processo):
        try:
            print('Processo iniciado')
            self.mysqldb.inserir_dados(query=atualiza_robo_notas.format(f'{self.timeconsult.updated_year}-{self.timeconsult.updated_month}-01'))
            if callable(processo):  # Garante que é uma função antes de chamar
                processo()
            else:
                print("Erro: processo não é uma função válida.")

        except KeyboardInterrupt:
            print('Programa finalizado pelo usuário')
            system("taskkill /F /IM chrome.exe /T")
            exit(0)

        except Exception as error_x:
            system("taskkill /F /IM chrome.exe /T")
            print(f'Erro: {error_x}\nReiniciando o programa...\n')
            execv(".\\python312\\python.exe", ["python", ".\\main.py"])


    def download_notas(self, municipio: str) -> None:
        if municipio.__eq__('PORTO ALEGRE'):
            consulta = self.mysqldb.ler_dados(query=consulta_municipal.format(int(self.timeconsult.updated_month), int(self.timeconsult.updated_year), municipio))
            if len(consulta).__gt__(0):
                self.browserportoalegre = BrowserPortoAlegre()
                self.browserportoalegre.start_browser()
                for dado in consulta:
                    id_dominio = int(dado[0])
                    cnpj = dado[2]
                    senha = dado[-1]
                    (lambda: (print(f'MUNICÍPIO: {municipio}'), print(f'ID_DOMINIO: {id_dominio}'), print(f'CNPJ: {cnpj}')))()
                    login = self.browserportoalegre.login(cnpj=cnpj, pwd=senha)
                    if not isinstance(login, str):
                        self.filesmanager.remove_files(files=self.filesmanager.list_files_porto_alegre(ext=".xml"), ext=".xml")
                        self.browserportoalegre.baixar_tudo()
                        self.xml.verify_clients(path_src=self.browserportoalegre.path_download, cnpj_client=cnpj, padrao='ABRASF')
                        self.mysqldb.atualizar_dados(query=atualiza_prefeitura.format(1, '', self.browserportoalegre.quantidade['prestador'], self.browserportoalegre.quantidade['tomador'], str(datetime.now())[:-7], int(dado[0]), int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
                    else:
                        self.mysqldb.atualizar_dados(query=atualiza_prefeitura.format(1, login, self.browserportoalegre.quantidade['prestador'], self.browserportoalegre.quantidade['tomador'], str(datetime.now())[:-7], int(dado[0]), int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
                    self.browserportoalegre.quantidade['prestador'], self.browserportoalegre.quantidade['tomador'] = 0, 0
                self.browserportoalegre.navegador.close()
                input('AQUI!!!!')
        
        elif municipio.__eq__('CACHOEIRINHA'):
            consulta = self.mysqldb.ler_dados(query=consulta_municipal.format(int(self.timeconsult.updated_month), int(self.timeconsult.updated_year), municipio))
            if len(consulta).__gt__(0):
                self.browsercachoeirinha = BrowserCachoeirinha()
                self.browsercachoeirinha.start_browser()
                self.browsercachoeirinha.navegador.get("chrome-extension://nnldcminpadbkkciihiihmfbgnggoehi/popup_v3.html")
                self.browsercachoeirinha.navegador.execute_script("""let teste0 = document.getElementsByClassName('toggler')[0];
                                                                    teste0.dispatchEvent(new Event('input', { bubbles: true }));
                                                                    teste0.dispatchEvent(new Event('change', { bubbles: true }));
                                                                    teste0.dispatchEvent(new Event('click', { bubbles: true }));
                                                                    if (teste0.disabled){
                                                                        teste0.click();
                                                                    }                                                                    
                                                                    let teste1 = document.getElementById("account_key");
                                                                    teste1.value = "aec1b68faa12cc7b9e1c0b560a0f7bc0"; 
                                                                    // Disparar eventos para que o site reconheça a mudança
                                                                    teste1.dispatchEvent(new Event('input', { bubbles: true }));
                                                                    teste1.dispatchEvent(new Event('change', { bubbles: true }));""")
                sleep(5)
                self.browsercachoeirinha.navegador.execute_script("""let teste2 = document.getElementsByClassName('btn btn-primary')[0];
                                                                    teste2.dispatchEvent(new Event('input', { bubbles: true }));
                                                                    teste2.dispatchEvent(new Event('change', { bubbles: true }));
                                                                    teste2.click();""")
                sleep(20)

                self.browsercachoeirinha.navegador.get(self.browsercachoeirinha.url)
                login = self.browsercachoeirinha.login(cnpj=getenv("LOGIN_CACHOEIRINHA"), pwd=getenv("PASSWORD_CACHOEIRINHA"))
                # input("Passou o login")
                for dado in consulta:
                    id_dominio = int(dado[0])
                    cnpj = dado[2]
                    senha = dado[-1]
                    (lambda: (print(f'MUNICÍPIO: {municipio}'), print(f'ID_DOMINIO: {id_dominio}'), print(f'CNPJ: {cnpj}')))()
                    if not isinstance(login, str):
                        self.filesmanager.remove_files(files=self.filesmanager.list_files_cachoeirinha(ext=".xml"), ext=".xml")
                        self.browsercachoeirinha.baixar_tudo()
                        self.xml.verify_clients(path_src=self.browsercachoeirinha.path_download, cnpj_client=cnpj, padrao='ABRASF')
                        self.mysqldb.atualizar_dados(query=atualiza_prefeitura.format(1, '', self.browsercachoeirinha.quantidade['prestador'], self.browsercachoeirinha.quantidade['tomador'], str(datetime.now())[:-7], int(dado[0]), int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
                    else:
                        input('Não passou no login')
                        self.mysqldb.atualizar_dados(query=atualiza_prefeitura.format(1, login, self.browsercachoeirinha.quantidade['prestador'], self.browsercachoeirinha.quantidade['tomador'], str(datetime.now())[:-7], int(dado[0]), int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
                    self.browsercachoeirinha.quantidade['prestador'], self.browsercachoeirinha.quantidade['tomador'] = 0, 0
                self.browsercachoeirinha.navegador.close()

        elif municipio.__eq__('NACIONAL'):
            consulta = self.mysqldb.ler_dados(query = consulta_nacional.format(int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
            if len(consulta).__gt__(0):
                self.browserportalnacional = BrowserPortalNacional()
                self.browserportalnacional.start_browser()
                for dado in consulta:
                    print(f'DADO: {dado}')
                    id_dominio = int(dado[0])
                    cnpj = dado[2]
                    senha = dado[-1]
                    if not "NOVA" in senha and not "SEM SENHA" in senha:
                        print(f'ID_DOMINIO: {id_dominio}')
                        print(f'CNPJ: {cnpj}')
                        login = self.browserportalnacional.login(cnpj=cnpj, pwd=senha)
                        if not isinstance(login, str):
                            self.filesmanager.remove_files(files=self.filesmanager.list_files_portal_nacional(ext=".xml"), ext=".xml")
                            if self.browserportalnacional.baixar_tudo():
                                self.xml.verify_clients(path_src=self.browserportalnacional.path_download, cnpj_client=cnpj, padrao='NACIONAL')
                                self.mysqldb.atualizar_dados(query=atualiza_nacional.format(1, "", self.browserportalnacional.quantidade['prestador'], self.browserportalnacional.quantidade['tomador'], str(datetime.now())[:-7], id_dominio, int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
                            self.mysqldb.atualizar_dados(query=atualiza_nacional.format(1, "", self.browserportalnacional.quantidade['prestador'], self.browserportalnacional.quantidade['tomador'], str(datetime.now())[:-7], id_dominio, int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
                        else:
                            self.mysqldb.atualizar_dados(query=atualiza_nacional.format(1, 'ERRO NO LOGIN', self.browserportalnacional.quantidade['prestador'], self.browserportalnacional.quantidade['tomador'], str(datetime.now())[:-7], id_dominio, int(self.timeconsult.updated_month), int(self.timeconsult.updated_year)))
                    self.browserportalnacional.quantidade['prestador'], self.browserportalnacional.quantidade['tomador'] = 0, 0
                self.browserportalnacional.navegador.close()
                sleep(2)
