__all__ = ["MLuaLogger", "MLuaLoggerGenerator", "MLuaLoggerDisplayer", "MLuaLoggerDecorator"]

import colorama
from datetime import datetime
from time import time
from pathlib import Path
from ..roots.mluaroots import MLuaBase

colorama.init(autoreset=True)

class MLuaLogger(MLuaBase):

    def __str__(self):
        return f"{type(self).__name__}()"

class MLuaLoggerGenerator(MLuaLogger):

    @staticmethod
    def info(message: str, datetime_enabled=True, bright_text=False) -> str:
        return f"{colorama.Style.BRIGHT if bright_text else ""}{colorama.Fore.GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S ') if datetime_enabled else ""}INFO] {message}"

    @staticmethod
    def warn(message: str, datetime_enabled=True, bright_text=False) -> str:
        return f"{colorama.Style.BRIGHT if bright_text else ""}{colorama.Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S ') if datetime_enabled else ""}WARN] {message}"

    @staticmethod
    def error(message: str, datetime_enabled=True, bright_text=False) -> str:
        return f"{colorama.Style.BRIGHT if bright_text else ""}{colorama.Fore.RED}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S ') if datetime_enabled else ""}ERROR] {message}"

    def __str__(self) -> str:
        return f"{type(self).__name__}()"

class MLuaLoggerDisplayer(MLuaLogger):

    @staticmethod
    def info(*args, **kwargs) -> None:
        print(MLuaLoggerGenerator.info(*args, **kwargs))

    @staticmethod
    def warn(*args, **kwargs) -> None:
        print(MLuaLoggerGenerator.warn(*args, **kwargs))

    @staticmethod
    def error(*args, **kwargs) -> None:
        print(MLuaLoggerGenerator.error(*args, **kwargs))

    def __str__(self):
        return f"{type(self).__name__}()"

class MLuaLoggerDecorator(MLuaLogger):

    @staticmethod
    def info(message: str) -> callable:
        def temp(function) -> callable:
            def run(*args, **kwargs) -> any:
                MLuaLoggerDisplayer.info(message)
                return function(*args, **kwargs)
                
            return run
            
        return temp

    @staticmethod
    def warn(message: str) -> callable:
        def temp(function) -> callable:
            def run(*args, **kwargs) -> any:
                MLuaLoggerDisplayer.warn(message)
                return function(*args, **kwargs)

            return run

        return temp

    @staticmethod
    def error(message: str) -> callable:
        def temp(function) -> callable:
            def run(*args, **kwargs) -> any:
                MLuaLoggerDisplayer.error(message)
                return function(*args, **kwargs)

            return run

        return temp

    @staticmethod
    def timer(ms=True) -> callable:
        def temp(function) -> callable:
            def run(*args, **kwargs) -> any:
                start_time = time()
                result = function(*args, **kwargs)
                end_time = time() - start_time
                MLuaLoggerDisplayer.info(f"Time taken: {end_time * 1000 if ms else end_time} {"ms" if ms else "s"}.")
                return result

            return run

        return temp

    def __str__(self) -> str:
        return f"{type(self).__name__}()"

class MLuaLoggerRecorder(MLuaLogger):

    def __init__(self) -> None:
        self.logs = []

    def info(self, message: str) -> None:
        self.logs.append(MLuaLoggerGenerator.info(message))

    def warn(self, message: str) -> None:
        self.logs.append(MLuaLoggerGenerator.warn(message))

    def error(self, message: str) -> None:
        self.logs.append(MLuaLoggerGenerator.error(message))

    def display(self) -> None:
        for log in self.logs:
            print(log)

    def save(self, path="./mlua_logs.txt") -> None:
        Path(path).write_text("\n".join(self.logs))

    def load(self, path="./mlua_logs.txt") -> None:
        self.logs = Path(path).read_text().split("\n")

    def __str__(self) -> str:
        return f"MLuaLoggerRecorder({self.logs})"
