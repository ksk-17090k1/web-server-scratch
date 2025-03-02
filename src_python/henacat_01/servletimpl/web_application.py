import importlib.util
from pathlib import Path

from servlet_info import ServletInfo


class WebApplication:
    WEBAPPS_DIR = "C:\\Henacat_0_1\\webapps"
    # ファーストクラスコレクション的なもの
    webAppCollection = {}

    def __init__(self, directory):
        # NOTE: いらなさそうなので一端コメントアウト
        # self.directory = directory
        # path_obj = Path(self.WEBAPPS_DIR) / directory
        # spec = importlib.util.spec_from_file_location(directory, path_obj)
        # self.classLoader = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(self.classLoader)
        # ファーストクラスコレクション的なもの
        self.servletCollection = {}

    @classmethod
    def create_instance(cls, directory):
        """webAppCollectionの追加"""
        new_app = cls(directory)
        cls.webAppCollection[directory] = new_app
        return new_app

    def add_servlet(self, url_pattern, servlet_class_name):
        """ServletInfoの追加"""
        self.servletCollection[url_pattern] = ServletInfo(
            self, url_pattern, servlet_class_name
        )

    def search_servlet(self, path):
        return self.servletCollection.get(path)

    @classmethod
    def search_web_application(cls, directory):
        return cls.webAppCollection.get(directory)
