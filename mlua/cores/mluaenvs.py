__all__ = ["MLuaModulesManager"]

from os import mkdir
from pathlib import Path
from json import loads, dumps
from .mluacores import MLuaModule
from ..roots import MLuaBase

class MLuaModulesManager(MLuaBase):

    @staticmethod
    def save(*modules: MLuaModule, directory="./mlua_modules") -> None:
        try:
            mkdir(directory)
        except FileExistsError:
            pass

        configuration = {}
        for module in modules:
            configuration[module.name()] = module.path()

        Path(directory, "index.json").write_text(dumps(configuration))

    @staticmethod
    def load(directory="./mlua_modules") -> list[MLuaModule]:
        configuration = loads(Path(directory, "index.json").read_text())
        temp_modules = []
        for module_name, module_path in configuration.items():
            temp_modules.append(MLuaModule(module_path))

        return temp_modules

    def __str__(self) -> str:
        return f"{type(self).__name__}()"
