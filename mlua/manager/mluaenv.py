from os import mkdir
from pathlib import Path
from json import loads, dumps
from .mluacore import MLuaModule
from ..base import MLuaBase

__all__ = ["MLuaModuleManager"]

class MLuaModuleManager(MLuaBase):

    @staticmethod
    def save(*mlua_modules: MLuaModule, directory="./mlua_modules") -> None:
        try:
            mkdir(directory)
        except FileExistsError:
            pass

        configuration = {}
        for module in mlua_modules:
            configuration[module.name()] = module.path()

        Path(directory, "index.json").write_text(dumps(configuration))

    @staticmethod
    def load(directory="./mlua_modules") -> list[MLuaModule]:
        configuration = loads(Path(directory, "index.json").read_text())
        temp_modules = []
        for module_name, module_path in configuration.items():
            temp_modules.append(MLuaModule(module_path))

        return temp_modules

    def __str__(self):
        return f"{type(self).__name__}()"
