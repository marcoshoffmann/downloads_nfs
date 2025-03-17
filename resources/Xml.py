from os import getenv, listdir, path
from dotenv import load_dotenv
from resources.PathManager import PathManager
from resources.TimeConsult import TimeConsult
from resources.FilesManager import FilesManager
load_dotenv()

class Xml:
    def __init__(self) -> None:
        self.pathmanager = PathManager()
        self.timeconsult = TimeConsult()
        self.filesmanager = FilesManager()
        self.layout_abrasf = getenv("LAYOUT_ABRASF")
        self.layout_cachoeirinha = getenv("LAYOUT_CACHOEIRINHA")
        self.layout_portal = getenv("LAYOUT_PORTAL")

    def __read_xml__(self, file: str) -> str:
        xml = open(file=file, mode='r', encoding='utf-8')
        xml_read = xml.read().split('\n')
        xml_read = ''.join([tag.strip() for tag in xml_read])
        xml.close()
        return xml_read
    
    def verify_layout_xml(self, file) -> str:
        if self.__read_xml__(file=file).__contains__(self.layout_abrasf): return self.__read_xml__(file=file)
        elif self.__read_xml__(file=file).__contains__(self.layout_portal): return self.__read_xml__(file=file)
        elif self.__read_xml__(file=file).__contains__(self.layout_alvorada): return self.__read_xml__(file=file)

    def verify_clients(self, path_src: str, cnpj_client: str, padrao: str) -> str:
        files = [f'{path_src}\\{file}' for file in listdir(path_src) if file.upper().endswith(".XML")]
        for file in files:
            tipo = None
            if self.verify_layout_xml(file).__contains__(f'<IdentificacaoPrestador><Cnpj>{cnpj_client}'): tipo = 'XMLS_PRESTADOS'
            if self.verify_layout_xml(file).__contains__(f'<IdentificacaoTomador><CpfCnpj><Cnpj>{cnpj_client}'): tipo = 'XMLS_TOMADOS'
            if self.verify_layout_xml(file).__contains__(f'<emit><CNPJ>{cnpj_client}') or self.verify_layout_xml(file).__contains__(f'<emit><CNPJ>{str(int(cnpj_client))}'): tipo = 'XMLS_PRESTADOS'
            if self.verify_layout_xml(file).__contains__(f'<toma><CNPJ>{cnpj_client}') or self.verify_layout_xml(file).__contains__(f'<toma><CNPJ>{str(int(cnpj_client))}'): tipo = 'XMLS_TOMADOS'
            if tipo is not None:
                tipo = f'{tipo}\\{padrao}'
                print(f'MOVER: {file}, {self.pathmanager.paths_empresas[cnpj_client]}\\{self.timeconsult.updated_year}\\{self.timeconsult.updated_month}.{self.timeconsult.updated_year}\\{tipo}')
                print(f'COPIAR: {self.pathmanager.paths_empresas[cnpj_client]}\\{self.timeconsult.updated_year}\\{self.timeconsult.updated_month}.{self.timeconsult.updated_year}\\{tipo}\\{file.split("\\")[-1]}, {self.pathmanager.path_xmls}\\{tipo}\\' + self.pathmanager.paths_empresas[cnpj_client].split("\\")[3] + f'\\{self.timeconsult.updated_month}{self.timeconsult.updated_year}')
                print(self.pathmanager.paths_empresas[cnpj_client])
                print(self.pathmanager.paths_empresas[cnpj_client].split("\\")[3])
                print(self.pathmanager.paths_empresas[cnpj_client].split("\\")[3].split(" - ")[0])
                print(self.pathmanager.paths_rotinas[self.pathmanager.paths_empresas[cnpj_client].split("\\")[3].split(" - ")[0]])
                path_rotina = self.pathmanager.paths_rotinas[self.pathmanager.paths_empresas[cnpj_client].split("\\")[3].split(" - ")[0]]
                self.pathmanager.move_xml(file=file, path_dest=f'{self.pathmanager.paths_empresas[cnpj_client]}\\{self.timeconsult.updated_year}\\{self.timeconsult.updated_month}.{self.timeconsult.updated_year}\\{tipo}')
                self.pathmanager.copy_xml(file=f'{self.pathmanager.paths_empresas[cnpj_client]}\\{self.timeconsult.updated_year}\\{self.timeconsult.updated_month}.{self.timeconsult.updated_year}\\{tipo}\\{file.split("\\")[-1]}', path_dest=f'{self.pathmanager.path_xmls}\\{tipo}\\' + path_rotina + f'\\{self.timeconsult.updated_month}{self.timeconsult.updated_year}')
