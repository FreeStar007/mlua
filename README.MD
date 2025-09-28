# MLua 使用指南

## 概述
MLua 是一个基于 Lua 的轻量级扩展库，提供了便捷的 Lua 环境管理和模块加载功能。

## 快速开始

### 1. 创建 Lua 环境
```python
from mluaroot import MLuaEnvironment

# 创建 Lua 运行时环境
lua_env = MLuaEnvironment()
```

### 2. 加载 Lua 模块
```python
from mluaroot import MLuaModule

# 加载单个 Lua 模块
module = MLuaModule("path/to/module.lua")
# 挂载模块到环境
mlua_obj = module.mount(lua_env)
```

### 3. 使用模块功能
```python
# 调用模块函数
result = mlua_obj.functions.some_function()

# 访问模块值
value = mlua_obj.values.some_variable
```

### 4. 处理模块依赖
```python
from mluaroot import MLuaModuleDependencies

# 创建依赖管理器
dep_resolver = MLuaModuleDependencies()

# 解析模块依赖
modules_to_load = dep_resolver.resolve(module)

# 批量加载模块
installer = MLuaModulesInstaller(*modules_to_load)
mlua_objects = installer.mount_all(lua_env)
```

## 高级用法

### 安全模式

```python
# 安全模式挂载（推荐）
mlua_obj = module.mount(lua_env, security=True) 
# 非安全模式挂载（更快但可能不安全
mlua_obj = module.mount(lua_env, security=False)
```

### 深度加载模块
```python
# 自动加载模块及其所有依赖
mlua_objects = module.mount_deeply(lua_env, dep_resolver)
```

## 注意事项
1. 建议始终使用安全模式挂载模块
2. 模块依赖关系应避免循环依赖
3. 模块文件路径应为绝对路径或相对于工作目录的有效路径