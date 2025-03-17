from resources.PathManager import PathManager
from resources.FilesManager import FilesManager

class CleanCach:
    def __init__(self) -> None:
        self.pathmanager = PathManager()
        self.filesmanager =FilesManager()

    def clear_cach(self) -> None:
        self.filesmanager.remove_files_any(files=self.pathmanager.search_cach(), ext="", exec=['Preferences', 'PreferredApps', 'Secure Preferences'])
