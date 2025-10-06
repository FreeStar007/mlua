__all__ = ["MLuaObject", "MLuaEnvironment", "MLuaModule", "MLuaInstaller", "MLuaResolver", "MLuaInjector"]

from pathlib import Path
from typing import Any

from lupa import LuaRuntime, lua_type

from .errors import MLuaModuleError
from .roots import MLuaBase, MLuaObject


class MLuaEnvironment(MLuaBase):

    def __init__(self, *args, **kwargs) -> None:
        self._runtime: LuaRuntime = None
        self.reset(*args, **kwargs)
        self._resolver = MLuaResolver()

    @property
    def lua_runtime(self) -> LuaRuntime:
        return self._runtime

    @property
    def resolver(self) -> "MLuaResolver":
        return self._resolver

    def reset(self, *args, **kwargs) -> None:
        self._runtime = LuaRuntime(*args, **kwargs)

    def __str__(self) -> str:
        return f"{type(self).__name__}({self._runtime})"


class MLuaModule(MLuaBase):

    def __init__(self, path: str) -> None:
        self._path = Path(path)
        self._name = self._path.stem
        self._data: str = self._path.read_text()
        self._requirements = {
            self._name: []
        }

    def mount(self, environment: MLuaEnvironment, security=True) -> MLuaObject:
        mlua_object = MLuaObject()
        functions = mlua_object.functions
        values = mlua_object.values
        lua: LuaRuntime = environment.lua_runtime
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

    def mount_deeply(self, environment: MLuaEnvironment, security=True) -> list[MLuaObject]:
        installer = MLuaInstaller(*environment.resolver.requirements(self))
        return installer.mount_all(environment, security=security)

    def require(self, *modules: "MLuaModule") -> None:
        for module in modules:
            if module in self._requirements[self._name]:
                raise MLuaModuleError(f"module \"{module.name}\" has already been included in \"{self._name}\"")

            elif self in MLuaResolver.requirements_directly(module):
                raise MLuaModuleError(f"module \"{module.name}\" has already required module \"{self._name}\"")

        self._requirements[self._name].extend(modules)

    def require_not(self, *modules: "MLuaModule") -> None:
        for index, module in enumerate(modules):
            if not module in self._requirements[self._name]:
                raise MLuaModuleError(f"module \"{module.name}\" has not been included in \"{self._name}\"")

            del self._requirements[self._name][index]

    @property
    def requirements(self) -> list["MLuaModule"]:
        return self._requirements[self._name]

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return str(self._path)

    @property
    def source(self) -> str:
        return self._data

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.name})"


class MLuaInstaller(MLuaBase):

    def __init__(self, *modules: MLuaModule) -> None:
        self._modules = modules

    def mount_all(self, environment: MLuaEnvironment, security=True) -> list[MLuaObject]:
        temp_modules = []
        for module in self._modules:
            temp_modules.append(module.mount(environment, security=security))

        return temp_modules

    def __str__(self) -> str:
        return f"{type(self).__name__}({', '.join([str(module) for module in self._modules])})"


class MLuaResolver(MLuaBase):
    _global_results = []

    def __init__(self) -> None:
        self._temp_results = []

    def requirements(self, *modules: MLuaModule) -> list[MLuaModule]:
        def run(*son_requirements: MLuaModule) -> None:
            for son_requirement in son_requirements:
                requirements: list[MLuaModule] = son_requirement.requirements
                if requirements:
                    run(*requirements)

                self._temp_results.append(son_requirement)

        run(*modules)
        results = self._temp_results
        self._temp_results = []
        return results

    @classmethod
    def requirements_directly(cls, *modules: MLuaModule) -> list[MLuaModule]:
        def run(*son_requirements: MLuaModule) -> None:
            for son_requirement in son_requirements:
                requirements: list[MLuaModule] = son_requirement.requirements
                if requirements:
                    run(*requirements)

                cls._global_results.append(son_requirement)

        run(*modules)
        results = cls._global_results
        cls._global_results = []
        return results

    @staticmethod
    def relationship(*modules: MLuaModule, indent_length=4, indent_style=".") -> None:
        def run(indent: int, *son_requirements: MLuaModule) -> None:
            for son_requirement in son_requirements:
                print(indent_style * indent + str(son_requirement))
                requirements: list[MLuaModule] = son_requirement.requirements
                if requirements:
                    run(indent + indent_length, *requirements)

        run(0, *modules)


# 谨慎使用，避免命名空间污染
class MLuaInjector(MLuaBase):

    @staticmethod
    def inject(environment: MLuaEnvironment, module: MLuaModule, globals_dict: dict[Any, Any], security=True) -> None:
        lua_module = module.mount(environment, security=security)
        functions = lua_module.functions
        values = lua_module.values
        for function_name, function_value in functions.__dict__.items():
            if not function_name.startswith("__"):
                globals_dict[function_name] = function_value

        for value_name, value_value in values.__dict__.items():
            if not value_name.startswith("__"):
                globals_dict[value_name] = value_value

    @staticmethod
    def inject_deeply(environment: MLuaEnvironment, module: MLuaModule, globals_dict, security=True) -> None:
        for requirement in module.requirements:
            MLuaInjector.inject_deeply(environment, requirement, globals_dict, security=security)

        MLuaInjector.inject(environment, module, globals_dict, security=security)
