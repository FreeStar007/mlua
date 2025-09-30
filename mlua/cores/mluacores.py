__all__ = ["MLuaObject", "MLuaEnvironment", "MLuaModule", "MLuaModulesInstaller", "MLuaModulesDependencies"]

from lupa import LuaRuntime, lua_type
from pathlib import Path
from ..roots.mluaroots import MLuaBase

class MLuaObject(MLuaBase):

    def __init__(self) -> None:
        self.functions = self._Functions()
        self.values = self._Values()

    class _Functions:

        def __str__(self) -> str:
            return str(self.__dict__)

    class _Values:

        def __str__(self) -> str:
            return str(self.__dict__)

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.functions.__str__()}, {self.values.__str__()})"

class MLuaEnvironment(MLuaBase):

    def __init__(self, *args, **kwargs) -> None:
        self.reset(*args, **kwargs)

    def environment(self) -> LuaRuntime:
        return self._runtime

    def reset(self, *args, **kwargs) -> None:
        self._runtime = LuaRuntime(*args, **kwargs)

    def __str__(self) -> str:
        return f"{type(self).__name__}({self._runtime})"

class MLuaModule(MLuaBase):

    def __init__(self, path: str) -> None:
        self._path = Path(path)
        self._name = self._path.stem
        self._data: str = self._path.read_text()
        self._dependencies = {
            self._name: []
        }

    def mount(self, environment: MLuaEnvironment, security=True) -> MLuaObject:
        mlua_object = MLuaObject()
        functions = mlua_object.functions
        values = mlua_object.values
        lua: LuaRuntime = environment.environment()
        temp_modules: dict = lua.execute(self._data)
        """
        两段循环意图为去除循环内判断的开销，遇到模块数据大的情况时有显著用处
        setattr有内置函数处理安全方面
        __dict__访问更快
        模块量少的情况下建议选择第一种方式，即security不需要改动
        """
        if security:
            for key, value in temp_modules.items():
                setattr(functions if lua_type(value) == "function" else values, key, value)

        else:
            for key, value in temp_modules.items():
                (functions if lua_type(value) == "function" else values).__dict__[key] = value
                
        return mlua_object

    def mount_deeply(self, environment: MLuaEnvironment, dependencies: "MLuaModulesDependencies", security=True) -> list[MLuaObject]:
        modules_installer = MLuaModulesInstaller(*dependencies.resolve(self))
        return modules_installer.mount_all(environment, security=security)

    def dependence(self, *modules: "MLuaModule") -> None:
        self._dependencies[self._name].extend(modules)
        
    def dependencies(self) -> list["MLuaModule"]:
        return self._dependencies[self._name]

    def name(self) -> str:
        return self._name

    def path(self) -> str:
        return str(self._path)

    def source(self) -> str:
        return self._data

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.name()})"

class MLuaModulesInstaller(MLuaBase):

    def __init__(self, *modules: MLuaModule) -> None:
        self._modules = modules

    def mount_all(self, environment: MLuaEnvironment, security=True) -> list[MLuaObject]:
        temp_modules = []
        for module in self._modules:
            temp_modules.append(module.mount(environment, security=security))

        return temp_modules

    def __str__(self) -> str:
        return f"{type(self).__name__}({', '.join([str(mlua_module) for mlua_module in self._modules])})"
        
class MLuaModulesDependencies(MLuaBase):

    def __init__(self) -> None:
        self._temp_results = []
    
    def resolve(self, *modules: MLuaModule) -> list[MLuaModule]:
        def run(*son_dependencies: MLuaModule) -> None:
            for son_dependency in son_dependencies:
                dependencies: list[MLuaModule] = son_dependency.dependencies()
                if dependencies is not None:
                    run(*dependencies)
                    
                self._temp_results.append(son_dependency)
                
        run(*modules)
        result = self._temp_results
        self._temp_results = []
        return result
