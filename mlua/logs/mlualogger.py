import colorama
from datetime import datetime
from time import time
from pathlib import Path
from ..base.mluaroot import MLuaBase

__all__ = ["MLuaLogger", "MLuaLoggerGenerator", "MLuaLoggerDisplayer", "MLuaLoggerDecorator"]

colorama.init(autoreset=True)

class MLuaLogger(MLuaBase):

    def __str__(self):
        return f"{type(self).__name__}()"

class MLuaLoggerGenerator(MLuaLogger):

    @staticmethod
    def info(message, datetime_enabled=True, bright_text=False):
        return f"{colorama.Style.BRIGHT if bright_text else ""}{colorama.Fore.GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S ') if datetime_enabled else ""}INFO] {message}"

    @staticmethod
    def warn(message, datetime_enabled=True, bright_text=False):
        return f"{colorama.Style.BRIGHT if bright_text else ""}{colorama.Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S ') if datetime_enabled else ""}WARN] {message}"

    @staticmethod
    def error(message, datetime_enabled=True, bright_text=False):
        return f"{colorama.Style.BRIGHT if bright_text else ""}{colorama.Fore.RED}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S ') if datetime_enabled else ""}ERROR] {message}"

    def __str__(self):
        return f"{type(self).__name__}()"

class MLuaLoggerDisplayer(MLuaLogger):

    @staticmethod
    def info(*args, **kwargs):
        print(MLuaLoggerGenerator.info(*args, **kwargs))

    @staticmethod
    def warn(*args, **kwargs):
        print(MLuaLoggerGenerator.warn(*args, **kwargs))

    @staticmethod
    def error(*args, **kwargs):
        print(MLuaLoggerGenerator.error(*args, **kwargs))

    def __str__(self):
        return f"{type(self).__name__}()"

class MLuaLoggerDecorator(MLuaLogger):

    @staticmethod
    def info(message):
        def temp(function):
            def run(*args, **kwargs):
                MLuaLoggerDisplayer.info(message)
                return function(*args, **kwargs)
                
            return run
            
        return temp

    @staticmethod
    def warn(message):
        def temp(function):
            def run(*args, **kwargs):
                MLuaLoggerDisplayer.warn(message)
                return function(*args, **kwargs)

            return run

        return temp

    @staticmethod
    def error(message):
        def temp(function):
            def run(*args, **kwargs):
                MLuaLoggerDisplayer.error(message)
                return function(*args, **kwargs)

            return run

        return temp

    @staticmethod
    def timer(ms=True):
        def temp(function):
            def run(*args, **kwargs):
                start_time = time()
                result = function(*args, **kwargs)
                end_time = time() - start_time
                MLuaLoggerDisplayer.info(f"Time taken: {end_time * 1000 if ms else end_time} {"ms" if ms else "s"}.")
                return result

            return run

        return temp

    def __str__(self):
        return f"{type(self).__name__}()"

class MLuaLoggerRecorder(MLuaLogger):

    def __init__(self):
        self.logs = []

    def info(self, message):
        self.logs.append(MLuaLoggerGenerator.info(message))

    def warn(self, message):
        self.logs.append(MLuaLoggerGenerator.warn(message))

    def error(self, message):
        self.logs.append(MLuaLoggerGenerator.error(message))

    def display(self):
        for log in self.logs:
            print(log)

    def save(self, file_path="mlua_logs.txt"):
        Path(file_path).write_text("\n".join(self.logs))

    def load(self, file_path="mlua_logs.txt"):
        self.logs = Path(file_path).read_text().split("\n")

    def __str__(self):
        return f"MLuaLoggerRecorder({self.logs})"
