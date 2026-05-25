from nonebot import require
from nonebot.plugin import PluginMetadata

require("ironsbot.plugins.db_sync")
require("ironsbot.plugins.http_client")

from . import db, image  # noqa: F401
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="赛尔号数据",
    description="赛尔号 API 数据库同步、查询依赖与游戏资源图片获取",
    usage="其他插件通过 require 后使用 db 与 image 模块中的依赖注入",
    config=Config,
)
