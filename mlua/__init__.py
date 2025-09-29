from .roots import *
from .cores import *
from .logs import *

@MLuaLoggerDecorator.info("Checking status.")
def status():
    MLuaLoggerDisplayer.info("Normal.")

def requirements() -> None:
    print("\n".join(["lupa", "colorama"]))

@MLuaLoggerDecorator.info("Testing module.")
@MLuaLoggerDecorator.timer()
def test(path: str) -> None:
    lua = MLuaEnvironment()
    module = MLuaModule(path)
    result = module.mount(lua)
    print(result)
