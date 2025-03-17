from os import getenv, listdir, path, remove
from dotenv import load_dotenv
from shutil import move, copy, rmtree
load_dotenv()

class PathManager:
    def __init__(self) -> None:
        self.path_clients = getenv("PATH_CLIENTS")
        self.path_rotinas = getenv("PATH_ROTINAS")
        self.path_cachoeirinha = getenv("PATH_CACHOEIRINHA")
        self.path_alvorada = getenv("PATH_ALVORADA")
        self.path_porto_alegre = getenv("PATH_PORTO_ALEGRE")
        self.path_portal_nacional = getenv("PATH_PORTAL_NACIONAL")
        self.path_xmls = getenv("PATH_XMLS")
        self.path_browser_cach = f'{getenv("LOCALAPPDATA")}\\Google\\Chrome for Testing\\User Data\\Default'
        self.paths_empresas = {path.split(" - ")[-1]: f'{self.path_clients}\\{path}' for path in listdir(self.path_clients)}
        self.paths_rotinas = {f'{int(path.split("-")[0]):03}': path for path in listdir(self.path_rotinas) if not ['INATIVAS'].__contains__(path)}

    def move_xml(self, file: str, path_dest: str) -> None:
        move(file, path_dest) if not path.exists(f'{path_dest}\\' + file.split("\\")[-1]) else remove(file)
    
    def copy_xml(self, file: str, path_dest: str) -> None:
        copy(file, path_dest)

    def search_cach(self) -> list:
        return [f'{self.path_browser_cach}\\{file_cach}' for file_cach in listdir(self.path_browser_cach) if path.isfile(f'{self.path_browser_cach}\\{file_cach}')]
    
    def delete_data(self, data_chrome: str) -> None:
        try:
            rmtree(data_chrome)
        except Exception as error_x:
            print(f'Não foi possível remover {data_chrome}: {error_x}')
