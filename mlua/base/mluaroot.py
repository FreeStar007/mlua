__all__ = ["MLuaBase"]

class MLuaBase:

    def __str__(self) -> str:
        return f"{type(self).__name__}()"
