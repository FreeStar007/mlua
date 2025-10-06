# MLua 使用指南

## 概述

一个基于 lupa 模块的轻量级扩展库，提供了便捷的 Lua 环境管理和模块加载功能。

## 快速开始

### 1. 创建 Lua 环境

```python
from mlua import MLuaEnvironment

# 创建 Lua 运行时环境
lua_env = MLuaEnvironment()
```

### 2. 加载 Lua 模块

```python
from mlua import MLuaModule, MLuaInstaller

# 加载单个 Lua 模块
module = MLuaModule("path/to/module.lua")
# 挂载模块到环境
mlua_obj = module.mount(lua_env: MLuaEnvironment)

# 加载多个 Lua 模块
installer = MLuaInstaller("path/to/module1.lua", "path/to/module2.lua")
mlua_objects = installer.mount_all(lua_env: MLuaEnvironment)
```

### 3. 使用模块功能

```python
# 调用模块函数
results = mlua_obj.functions.some_function()

# 访问模块值
value = mlua_obj.values.some_variable
```

### 4. 处理模块依赖

```python
from mlua import MLuaResolver

# 创建依赖管理器
resolver = MLuaResolver()

# 解析模块依赖（解析对象式）
modules_to_load = resolver.requirements(module: MLuaModule)

# 解析模块依赖（解析全局式）
modules_to_load = MLuaResolver.requirements_directly(module: MLuaModule)

# 打印依赖关系
MLuaResolver.relationship(modules_to_load1, modules_to_load2, modules_to_load3, ...)
```

## 高级用法

### 日志

```python
from mlua import MLuaLogsPrinter

# 打印信息日志
MLuaLogsPrinter.info("Hello, world!")

# 打印警告日志
MLuaLogsPrinter.warn("Something might be wrong!")

# 打印错误日志
MLuaLogsPrinter.error("Something went wrong!")
```

### 安全模式

```python
# 安全模式挂载（推荐）
mlua_obj = module.mount(lua_env: MLuaEnvironment, security = True)
# 非安全模式挂载（更快但可能不安全）
mlua_obj = module.mount(lua_env: MLuaEnvironment, security = False)
```

### 深度加载模块

```python
# 深度加载模块及其所有依赖
mlua_objects = module.mount_deeply(lua_env: MLuaEnvironment)
```

### 校验状态

```python
from mlua import status

status()
```

## 注意事项

1. 建议始终使用安全模式挂载模块
2. 模块依赖关系应避免循环依赖
3. 模块文件路径应为绝对路径或相对于工作目录的有效路径
4. 禁止循环依赖