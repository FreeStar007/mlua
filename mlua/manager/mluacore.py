from lupa import LuaRuntime, lua_type
from pathlib import Path
from ..base.mluaroot import MLuaBase

__all__ = ["MLuaObject", "MLuaEnvironment", "MLuaModule", "MLuaModuleInstaller"]

class MLuaObject(MLuaBase):

    def __init__(self) -> None:
        self.functions = self._Functions()
        self.values = self._Values()

    class _Functions:

        def __str__(self) -> str:
            return self.__dict__.__str__()

    class _Values:

        def __str__(self) -> str:
            return self.__dict__.__str__()

    def __str__(self):
        return f"{type(self).__name__}({self.functions.__str__()}, {self.values.__str__()})"

class MLuaEnvironment(MLuaBase):

    def __init__(self, *args, **kwargs) -> None:
        self.reset(*args, **kwargs)

    def environment(self) -> LuaRuntime:
        return self._lua_runtime

    def reset(self, *args, **kwargs) -> None:
        self._lua_runtime = LuaRuntime(*args, **kwargs)

    def __str__(self):
        return f"{type(self).__name__}({self._lua_runtime})"

class MLuaModule(MLuaBase):

    def __init__(self, module_path: str) -> None:
        self._module_path= module_path
        self._module_data: str = Path(self._module_path).read_text()

    def mount(self, mlua_environment: MLuaEnvironment, security=True) -> MLuaObject:
        mlua_object = MLuaObject()
        functions = mlua_object.functions
        values = mlua_object.values
        lua = mlua_environment.environment()
        temp_modules: dict = lua.execute(self._module_data)
        # 两段循环意图为去除循环内判断的开销，遇到模块数据大的情况时有显著用处
        if security:
            for key, value in temp_modules.items():
                setattr(functions if lua_type(value) == "function" else values, key, value)

        else:
            for key, value in temp_modules.items():
                (functions if lua_type(value) == "function" else values).__dict__[key] = value
                
        return mlua_object

    def name(self) -> str:
        return Path(self._module_path).stem

    def path(self) -> str:
        return self._module_path

    def source(self) -> str:
        return self._module_data

    def __str__(self):
        return f"{type(self).__name__}({self.name()})"

class MLuaModuleInstaller(MLuaBase):

    def __init__(self, *mlua_modules: MLuaModule) -> None:
        self._mlua_modules = mlua_modules

    def mount_all(self, lua: MLuaEnvironment) -> list[MLuaObject]:
        temp_mlua_modules = []
        for mlua_module in self._mlua_modules:
            temp_mlua_modules.append(mlua_module.mount(lua))

        return temp_mlua_modules

    def __str__(self):
        return f"{type(self).__name__}({', '.join([str(mlua_module) for mlua_module in self._mlua_modules])})"
