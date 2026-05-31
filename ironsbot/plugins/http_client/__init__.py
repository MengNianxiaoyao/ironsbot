# SPDX-License-Identifier: MIT
from hishel.httpx import AsyncCacheClient
from httpx import AsyncClient
from nonebot import get_driver, logger
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="HTTP 缓存客户端",
    description="管理全局共享的 hishel HTTP 缓存客户端生命周期",
    usage="其他插件通过 require 后使用 HttpCacheClient 依赖注入获取客户端实例",
)
_driver = get_driver()
_cache_client: AsyncCacheClient | None = None
_origin_client: AsyncClient | None = None


@_driver.on_startup
async def _() -> None:
    global _cache_client, _origin_client
    _cache_client = AsyncCacheClient()
    _origin_client = AsyncClient()
    logger.info("HTTP 客户端已初始化")


@_driver.on_shutdown
async def _() -> None:
    await _close_http_client(_cache_client)
    await _close_http_client(_origin_client)


def get_http_cache_client() -> AsyncCacheClient:
    """获取全局 HTTP 缓存客户端实例。"""
    if _cache_client is None:
        raise RuntimeError("HTTP 缓存客户端尚未初始化")
    return _cache_client


def get_http_origin_client() -> AsyncClient:
    """获取全局 HTTP 客户端实例。"""
    if _origin_client is None:
        raise RuntimeError("HTTP 客户端尚未初始化")
    return _origin_client


async def _close_http_client(client: AsyncClient | None) -> None:
    if client is None:
        return

    try:
        await client.aclose()
    except Exception:  # noqa: BLE001
        logger.opt(exception=True).error("关闭 HTTP 客户端失败")


GetHttpCacheClient = Depends(get_http_cache_client)
GetHttpOriginClient = Depends(get_http_origin_client)
