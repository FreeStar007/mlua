from .base import *
from .manager import *
from .logs import *

__version__ = "0.1.0"
__author__ = "FreeStar007"

def info() -> None:
    print(f"MLua version: {__version__}\nMLua author: {__author__}\nLicense: Apache 2.0")

def requirements() -> None:
    print("\n".join(["lupa", "colorama"]))

@MLuaLoggerDecorator.info("Testing module.")
@MLuaLoggerDecorator.timer()
def test(module_path: str) -> None:
    lua = MLuaEnvironment()
    module = MLuaModule(module_path)
    result = module.mount(lua)
    print(result)
