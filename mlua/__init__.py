from .base import *
from .manager import *
from .logs import *

__version__ = "0.1.2"
__author__ = "FreeStar007"

def infos() -> None:
    print(f"MLua version: {__version__}\nMLua author: {__author__}\nLicense: Apache 2.0")

def requirements() -> None:
    print("\n".join(["lupa", "colorama"]))

@MLuaLoggerDecorator.info("Testing module.")
@MLuaLoggerDecorator.timer()
def test(path: str) -> None:
    lua = MLuaEnvironment()
    module = MLuaModule(path)
    result = module.mount(lua)
    print(result)
