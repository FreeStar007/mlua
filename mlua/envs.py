__all__ = ["MLuaManager"]

from json import loads as jloads, dumps as jdumps
from os import mkdir
from pathlib import Path
from pickle import dumps as pdumps, loads as ploads
from typing import Any
from zlib import compress, decompress

from .cores import MLuaModule
from .errors import MLuaModuleError
from .roots import MLuaBase


class MLuaManager(MLuaBase):

    @staticmethod
    def save(*modules: MLuaModule, directory="./mlua_modules") -> bool:
        try:
            mkdir(directory)
        except FileExistsError:
            pass

        configuration = {}
        for module in modules:
            configuration[module.name] = module.path

        return bool(Path(directory, "index.json").write_text(jdumps(configuration)))

    @staticmethod
    def load(directory="./mlua_modules") -> list[MLuaModule]:
        configuration = jloads(Path(directory, "index.json").read_text())
        temp_modules = []
        for module_path in configuration.values():
            temp_modules.append(MLuaModule(module_path))

        return temp_modules

    @staticmethod
    def use(*modules: str, directory="./mlua_modules") -> list[MLuaModule]:
        configuration: dict[str, str] = jloads(Path(directory, "index.json").read_text())
        temp_modules = []
        for module in modules:
            temp_module = configuration.get(module)
            if temp_module is None:
                raise MLuaModuleError(f"module \"{module}\" has not been found in mlua repository \"{directory}\"")

            temp_modules.append(MLuaModule(temp_module))

        return temp_modules


class MLuaPackager(MLuaBase):

    @staticmethod
    def pack(*modules: MLuaModule) -> bytes:
        structure = {}
        for module in modules:
            structure[module.path] = module.source

        return compress(pdumps(structure))

    @staticmethod
    def unpack(data: bytes) -> list[MLuaModule]:
        structure = ploads(decompress(data))
        temp_modules = []
        for path, source in structure.items():
            temp_modules.append(MLuaModule(path))

        return temp_modules

    @staticmethod
    def test(data: bytes) -> bool:
        try:
            ploads(decompress(data))
            return True

        except TypeError:
            return False
