# 帮助插件

> fork 自 [nonebot-plugin-treehelp](https://github.com/he0119/nonebot-plugin-treehelp)

通过读取 NoneBot 已加载插件的元信息（`PluginMetadata`），自动生成帮助信息。
支持**多轮对话**——发送 `帮助` 后可通过序号连续查看各插件的详细说明。

---

## 配置项

在 `.env` 或 `.env.prod` 中配置：

| 配置项                   | 类型         | 默认值 | 说明                                     |
| ------------------------ | ------------ | ------ | ---------------------------------------- |
| `help_ignored_plugins`   | `list[str]`  | `[]`   | 需要在帮助列表中隐藏的插件名称列表       |

**示例：**

```dotenv
HELP_IGNORED_PLUGINS=["数据同步"]
```

---

## 插件适配要求

本插件通过 `PluginMetadata` 发现和展示帮助信息。要让你的插件出现在帮助列表中，需满足：

1. 在插件的 `__init__.py` 中定义 `__plugin_meta__`：

```python
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="插件名称",
    description="一句话描述",
    usage="详细使用说明……",
)
```

2. `type` 字段为 `None`（默认）或 `"application"`。`type="library"` 的插件会被自动过滤。
3. 如果设置了 `supported_adapters`，当前连接的 Bot 适配器需在支持列表中。

---

## 技术实现

- 触发方式：`on_fullmatch("帮助")`，`priority=1`，不拦截非数字消息。
- 多轮对话：使用 `PromptSessionManager` + `reject_with_rule` 创建带版本化 Rule 的临时 Matcher，只匹配纯数字输入，其他命令正常传播。
- 当用户触发其他 `priority > 0` 的命令时，旧帮助会话自动失效。
