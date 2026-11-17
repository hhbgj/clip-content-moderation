import ipaddress
import socket
from io import BytesIO
from urllib.parse import urlparse

import requests
from PIL import Image

MAX_BYTES = 10 * 1024 * 1024


def _check_public(url: str) -> None:
    """Only http(s) addresses on the public internet: the server must not be usable to reach
    its own machine or the local network (SSRF)."""
    parts = urlparse(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError("只支持 http / https 图片地址")
    for info in socket.getaddrinfo(parts.hostname, None):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise ValueError("不允许访问内网或本机地址")


def load_image_from_url(url: str) -> Image.Image:
    try:
        _check_public(url)
        headers = {"User-Agent": "Mozilla/5.0", "Referer": url}
        response = requests.get(url, headers=headers, timeout=5, stream=True, allow_redirects=False)
        response.raise_for_status()
        data = response.raw.read(MAX_BYTES + 1, decode_content=True)
        if len(data) > MAX_BYTES:
            raise ValueError("图片超过 10 MB")
        return Image.open(BytesIO(data)).convert("RGB")
    except Exception as e:
        raise ValueError(f"无法加载URL图片: {str(e)}")


def load_image_from_file(file_bytes: bytes) -> Image.Image:
    try:
        return Image.open(BytesIO(file_bytes)).convert("RGB")
    except Exception as e:
        raise ValueError(f"本地图片格式错误或损坏: {str(e)}")
