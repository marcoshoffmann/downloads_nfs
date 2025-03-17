from os import listdir, remove
from resources.PathManager import PathManager

class FilesManager:
    def __init__(self):
        self.pathmanager = PathManager()

    def list_files_cachoeirinha(self, ext: str) -> list:
        return [f'{self.pathmanager.path_cach}\\{file}' for file in listdir(self.pathmanager.path_cach) if file.upper().endswith(ext.upper())]
    
    def list_files_porto_alegre(self, ext: str) -> list:
        return [f'{self.pathmanager.path_porto_alegre}\\{file}' for file in listdir(self.pathmanager.path_porto_alegre) if file.upper().endswith(ext.upper())]
    
    def list_files_portal_nacional(self, ext: str) -> list:
        return [f'{self.pathmanager.path_portal_nacional}\\{file}' for file in listdir(self.pathmanager.path_portal_nacional) if file.upper().endswith(ext.upper())]
    
    def remove_files(self, files: str = [], ext: str = ".xml") -> None:
        [remove(file) for file in files]
    
    def remove_files_any(self, files: list, ext: str, exec: list = []) -> None:
        for file in files:
            try:
                if file.split("\\")[-1] not in exec: 
                    remove(file)
                    print(f'Arquivo {file} removido com sucesso!')
            except Exception as error: print(f'Não conseguiu remover o arquivo: {file} === ERRO: {error}')
                