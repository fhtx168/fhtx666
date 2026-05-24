#!/usr/bin/env python3
"""
纳米 P视频
发送开始提示、使用卡片展示结果、设置长时间超时

优化内容：
- 添加连接超时（1800秒）和读取超时（3小时）
- 添加每600秒进度提示
- 更友好的错误信息

用法:
    python3 nami_p_video.py --flow-id 701 -p "用户需求描述"
    python3 nami_p_video.py --flow-id 701 -p "需求" --file '[]'
"""

import json
import sys
import argparse
import traceback
import urllib.request
import urllib.error
import uuid
import os
import platform
import hashlib
import secrets
import random
import threading
import time
import socket
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from collections import defaultdict

# 默认配置
DEFAULT_FLOW_ID = "44510"
DEFAULT_QID = "3464550917"
DEFAULT_TIMEOUT = 10800  # 3小时（读取超时）
CONNECT_TIMEOUT = 1800   # 连接超时 1800秒
PROGRESS_INTERVAL = 600  # 进度提示间隔 600秒
DEFAULT_FORMAT = "markdown"
DEFAULT_CHANNEL = "webchat"  # 默认消息来源

# API 地址
NAMI_API_BASE = "https://www.n.cn/api/ai_agent_flow/chat"


def load_cookie_from_config() -> Dict[str, str]:
    """
    从 ~/.openclaw/workspace/config/.cookie.json 读取 cookie，返回形如 {"cookie": "xxxx"} 的字典。
    如果文件不存在、解析失败或没有 cookie 字段，则返回空字典。
    """
    home_dir = os.path.expanduser("~")
    cookie_path = os.path.join(home_dir, ".openclaw", "workspace", "config", ".cookie.json")

    try:
        with open(cookie_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    if not isinstance(data, dict):
        return {}

    cookie_value = data.get("cookie")
    if not cookie_value:
        return {}

    return {"cookie": str(cookie_value)}


def get_signed_headers(
    *,
    path,
    access_token: Optional[str] = None,
    auth_token: str = "",
    ua: str = "Mozilla/5.0 (Python Upload Script)",
    nami_platform: Optional[str] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    生成与前端 `getHeaders` 等价的签名请求头。

    - access_token: 如果为空，则自动生成一个 uuid
    - auth_token: 服务端下发的 Auth-Token（可选）
    - ua: 浏览器 UA，JS 中用 navigator.userAgent
    - nami_platform: JS 中的 HelperCore.getOsInfo()?.name
    """

    def _get_iso8601_time() -> str:
        """
        复刻 JS `HelperCore.getISO8601Time`：
        - 当前时间（东八区）
        - 输出类似 2021-11-20T19:01:01+08:00
        """
        # 先获取 UTC 时间，再转换到东八区，确保 tzoffset 为 +08:00
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
        iso = now.isoformat()
        if "." in iso:
            date_part, rest = iso.split(".", 1)
            if "+" in rest:
                _, tz = rest.split("+", 1)
                return f"{date_part}+{tz}"
            if "-" in rest:
                _, tz = rest.split("-", 1)
                return f"{date_part}-{tz}"
            return iso
        return iso

    def _md5_hex(value: str) -> str:
        return hashlib.md5(value.encode("utf-8")).hexdigest()

    def _generate_trace_id() -> str:
        """
        参考 JS `generateTraceId`：
        - 使用 16 字节随机数 -> 32 位十六进制小写字符串
        """
        return secrets.token_hex(16)

    # access_token 逻辑：如果未显式传入，则自动生成一个 uuid
    if not access_token:
        access_token = str(uuid.uuid4())

    zm_nonce = "".join(random.choices("0123456789", k=16))

    # === 1. 组装参与 zm-token 计算的数组 ===
    request_header_arr = [
        "H5",  # device-platform
        _get_iso8601_time(),  # timestamp
        "1.3",  # zm-ver
        access_token,  # access-token
        _md5_hex(ua),  # md(zm-ua)
        path,
        zm_nonce,
    ]

    # access_token 为空则不参与 zm-token 计算（这里已经保证不为空，只做防御）
    if not access_token:
        request_header_arr.pop(3)

    # === 2. 公共请求头，与 JS getHeaders 对齐 ===
    request_header_data: Dict[str, str] = {
        "device-platform": "H5",
        "timestamp": request_header_arr[1],
        "zm-ver": "1.3",
        "access-token": access_token,
        "zm-token": "",  # 占位，下面再计算
        "zm-ua": _md5_hex(ua),
        "zm-nonce": zm_nonce,
    }

    # nami-platform（操作系统），简单用 Python 的 platform 名称兜底
    request_header_data["nami-platform"] = nami_platform or platform.system() or "Unknown"

    # 计算 zm-token：MD5(device-platform + timestamp + zm-ver + access-token + md(zm-ua))
    request_header_data["zm-token"] = _md5_hex("".join(request_header_arr))

    # === 3. 追加其余头部（与 JS getHeaders 一致的键名） ===
    request_id = str(uuid.uuid4())
    headers: Dict[str, str] = {
        **request_header_data,
        "func-ver": "1",  # 新版本接口标识
        "Auth-Token": auth_token,
        "Request-Id": request_id,
        "Header-Tid": _generate_trace_id(),
        "cloud_src": "video",
    }

    if extra_headers:
        headers.update(extra_headers)

    # 去掉空值，避免发送多余空头
    return {k: v for k, v in headers.items() if v}


DEFAULT_UPLOAD_PATH: str = "/api/s3/upload"
DEFAULT_TIMEOUT_SECONDS: int = 10800


def upload_by_api(
    file_path: str,
    source_type: Optional[str] = None,
    *,
    base_url: str = "https://nami.so.360.com",
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    access_token: str = "",
    auth_token: str = "",
    ua: str = "Mozilla/5.0 (Python Upload Script)",
    nami_platform: Optional[str] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    使用 urllib.request 实现的上传接口，对应前端的 upload-api.js。

    返回结构：
    - 一个 dict，结构为：{"data": {"url": <up_url>}}
    """
    if not base_url:
        raise ValueError("base_url 不能为空，例如 'https://so.n.cn'")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")

    # 构造请求地址（携带 appsource=so）
    base_url = base_url.rstrip("/")
    path = DEFAULT_UPLOAD_PATH
    if not path.startswith("/"):
        path = "/" + path
    full_url = base_url + path
    parsed = urlparse(full_url)
    query_dict = parse_qs(parsed.query)
    query_dict["appsource"] = ["so"]
    new_query = urlencode(query_dict, doseq=True)
    url = urlunparse(parsed._replace(query=new_query))

    """---"""
    cookie_dict = load_cookie_from_config()
    cookie = cookie_dict.get('cookie', '')
    extra_headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }

    if cookie:
        extra_headers.update({
            'Cookie': cookie
        })

    """---"""

    # 生成签名请求头
    headers = get_signed_headers(
        path=path,
        access_token=access_token or None,
        auth_token=auth_token,
        ua=ua,
        nami_platform=nami_platform,
        extra_headers=extra_headers,
    )

    # multipart/form-data 边界
    boundary = "----WebKitFormBoundary" + secrets.token_hex(16)

    # 表单字段
    fields = {
        "source_type": source_type or "",
    }

    # 构造 multipart/form-data body
    lines = []
    for name, value in fields.items():
        lines.extend(
            [
                f"--{boundary}",
                f'Content-Disposition: form-data; name="{name}"',
                "",
                str(value),
            ]
        )

    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_content = f.read()

    lines.extend(
        [
            f"--{boundary}",
            f'Content-Disposition: form-data; name="up_file"; filename="{file_name}"',
            "Content-Type: application/octet-stream",
            "",
        ]
    )

    body = "\r\n".join(lines).encode("utf-8") + b"\r\n" + file_content + b"\r\n" + f"--{boundary}--\r\n".encode(
        "utf-8")

    # Content-Type 由我们自己设置
    final_headers = {
        **headers,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }

    req = urllib.request.Request(
        url,
        data=body,
        headers=final_headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status_code = resp.getcode()
            resp_body = resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP 错误: {e.code} {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"请求失败: {getattr(e, 'reason', e)}") from e

    if status_code < 200 or status_code >= 300:
        raise RuntimeError(f"上传失败，HTTP 状态码: {status_code}, 响应: {resp_body[:200]}")

    try:
        data = json.loads(resp_body)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"解析响应 JSON 失败: {e}") from e

    up_url = data.get("data", {}).get("up_url")
    return up_url


def parse_file_arg(file_arg) -> list:
    """解析 file 参数"""
    if not file_arg:
        return []
    try:
        data = json.loads(file_arg)
        if isinstance(data, list):
            for _item in data:
                try:
                    public_url = _item.get('url', '')
                    local_path = _item.get('local_path', '')
                    if not public_url and local_path:
                        upload_url = upload_by_api(local_path)
                        _item['url'] = upload_url
                except Exception as _:
                    pass

            return data
        if isinstance(data, dict):
            try:
                public_url = data.get('url', '')
                local_path = data.get('local_path', '')
                if not public_url and local_path:
                    upload_url = upload_by_api(local_path)
                    data['url'] = upload_url
            except Exception as _:
                pass
            return [data]
        return []
    except json.JSONDecodeError:
        return []


def get_default_channel() -> str:
    """自动识别 channel：优先使用环境变量 OPENCLAW_CHANNEL，否则默认 feishu"""
    # 优先使用命令行参数（如果有）
    # 如果命令行未指定，则从环境变量读取
    env_channel = os.environ.get("OPENCLAW_CHANNEL", "").strip()
    if env_channel:
        return env_channel
    return DEFAULT_CHANNEL


def is_feishu_channel(channel: str) -> bool:
    """判断是否为飞书渠道"""
    return channel.lower() == "feishu"


def print_feishu_error(error_msg):
    error_card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "❌ 纳米 P视频 执行出错"},
            "template": "red"
        },
        "elements": [
            {
                "tag": "div",
                "text": {"tag": "plain_text", "content": f"错误信息：{error_msg}"}
            }
        ]
    }
    print(json.dumps(error_card, ensure_ascii=False))


def print_channel_error(channel: str, error_msg: str):
    """根据渠道打印错误提示"""
    if is_feishu_channel(channel):
        print_feishu_error(error_msg)
    else:
        print(f"❌ 纳米 P视频 执行出错：{error_msg}")


def print_feishu_progress(message: str):
    """打印飞书进度提示"""
    print(f"🔄 {message}")


class ProgressPrinter:
    """进度提示器 - 每隔一定时间打印进度"""
    
    def __init__(self, interval: int = PROGRESS_INTERVAL, message: str = "正在处理中，请稍候"):
        self.interval = interval
        self.message = message
        self.start_time = time.time()
        self.running = False
        self.thread = None
    
    def _print_loop(self):
        """后台打印循环"""
        while self.running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            print(f"⏳ {self.message} ({minutes}分{seconds}秒)...", flush=True)
            time.sleep(self.interval)
    
    def start(self):
        """启动进度提示"""
        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._print_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """停止进度提示"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def elapsed_time(self):
        """获取已用时间"""
        return int(time.time() - self.start_time)


def parse_sse_data(line: str):
    """解析 SSE 数据行"""
    if not line.startswith("data: "):
        return None
    try:
        sse_data = json.loads(line[6:])
        message = sse_data.get('message', {})
        if isinstance(message, dict):
            return message
        else:
            return {}
    except json.JSONDecodeError:
        return None


def extract_results(sse_data: dict) -> dict:
    """从 SSE 数据中提取结果，返回规范化结构"""

    def _is_markdown_image_only(text: str) -> bool:
        """
        判断文本是否仅为一个 Markdown 图片链接，如:
        ![](https://xxx.mp4?xxx)
        """
        if not text:
            return False
        stripped = text.strip()
        # 严格要求整段就是一个图片 markdown
        if not stripped.startswith("!"):
            return False
        # 形如 ![](url) 或 ![alt](url)
        if stripped.count("](") != 1 or not stripped.endswith(")"):
            return False
        return True

    results = defaultdict(list)

    # 提取 summary / final_tips
    raw_summary = sse_data.get("summary") or sse_data.get("final_content", "") or ""
    if _is_markdown_image_only(raw_summary):
        # 规则 3：如果 summary 为空或仅为一个 markdown 链接则丢弃
        summary = ""
    else:
        summary = raw_summary or ""

    results["summary"] = summary
    results["final_tips"] = sse_data.get("final_tips", "") or ""

    # 提取 share_url（优先顶层，其次 attachments）
    share_url = sse_data.get("share_url", "") or ""

    attachments = sse_data.get("attachments", []) or []
    for attachment in attachments:
        att_share_url = attachment.get("share_url", "") or ""
        if att_share_url and not share_url:
            share_url = att_share_url

        # 规则 2：循环 attachment.results
        attachment_results = attachment.get("results", []) or []
        if attachment_results:
            for item in attachment_results:
                item_type = item.get("type", "") or ""
                title = item.get("title", "") or ""
                description = item.get("description", "") or ""
                url = item.get("url", "") or item.get("share_url") or  ""

                if url or title or description:
                    results[item_type].append(
                        {
                            "description": description,
                            "url": url,
                            "title": title,
                        }
                    )
        else:
            item_type = attachment.get("type", "") or ""
            title = attachment.get("title", "") or ""
            description = attachment.get("description", "") or ""
            url = attachment.get("url", "") or attachment.get("share_url") or ""

            if url or title or description:
                results[item_type].append(
                    {
                        "description": description,
                        "url": url,
                        "title": title,
                    }
                )

    results["share_url"] = share_url

    return results


def build_feishu_card(results: dict) -> dict:
    """
    构建飞书卡片（基于规范化结果结构，包含 share_url 查看详情）
    """
    card_elements = []
    
    # 获取数据
    summary = results.get("summary", "") or ""
    final_tips = results.get("final_tips", "") or ""
    # 展示顺序要求：summary -> video -> image -> other -> final_tips -> share_url
    text_content = summary
    videos = results.get("video", [])
    images = results.get("image", [])
    other = results.get("other", [])
    share_url = results.get("share_url", "")
    agent_name = "P视频"
    
    # 文本内容（不裁剪）
    if text_content:
        card_elements.append({
            "tag": "div", 
            "text": {"tag": "plain_text", "content": text_content}
        })
    
    # 视频部分
    if videos:
        card_elements.append({"tag": "hr"})
        card_elements.append({
            "tag": "div", 
            "text": {"tag": "plain_text", "content": "🎬 视频"}
        })
        for video in videos:
            desc = video.get("description", "") or ""
            video_title = video.get("title", "") or ""
            video_url = video.get("url", "") or ""
            # description
            if desc:
                card_elements.append({
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": desc}
                })
            # title
            if video_title:
                card_elements.append({
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": f"  • {video_title}"}
                })
            # url
            if video_url:
                card_elements.append({
                    "tag": "action",
                    "actions": [{
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "▶️ 查看视频"},
                        "type": "primary",
                        "url": video_url
                    }]
                })
    
    # 图片部分
    if images:
        card_elements.append({"tag": "hr"})
        card_elements.append({
            "tag": "div", 
            "text": {"tag": "plain_text", "content": "🖼️ 图片"}
        })
        for img in images:
            desc = img.get("description", "") or ""
            img_title = img.get("title", "") or ""
            img_url = img.get("url", "") or ""
            # description
            if desc:
                card_elements.append({
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": desc}
                })
            # title
            if img_title:
                card_elements.append({
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": f"  • {img_title}"}
                })
            # url
            if img_url:
                card_elements.append({
                    "tag": "action",
                    "actions": [{
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "🖼️ 查看图片"},
                        "type": "primary",
                        "url": img_url
                    }]
                })
    
    # 其他类型
    if other:
        card_elements.append({"tag": "hr"})
        card_elements.append({
            "tag": "div", 
            "text": {"tag": "plain_text", "content": "📦 其他"}
        })
        for item in other:
            desc = item.get("description", "") or ""
            item_title = item.get("title", "") or ""
            item_url = item.get("url", "") or ""
            # description
            if desc:
                card_elements.append({
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": desc}
                })
            # title
            if item_title:
                card_elements.append({
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": f"  • {item_title}"}
                })
            # url
            if item_url:
                card_elements.append({
                    "tag": "action",
                    "actions": [{
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "🔗 查看"},
                        "type": "default",
                        "url": item_url
                    }]
                })

    # final_tips 单独展示在 other 之后
    if final_tips:
        card_elements.append({"tag": "hr"})
        card_elements.append({
            "tag": "div",
            "text": {"tag": "plain_text", "content": final_tips}
        })
    
    # 查看详情链接（最重要！）
    if share_url:
        card_elements.append({"tag": "hr"})
        card_elements.append({
            "tag": "action", 
            "actions": [{
                "tag": "button", 
                "text": {"tag": "plain_text", "content": "🔗 查看详情"}, 
                "type": "primary", 
                "url": share_url
            }]
        })
    
    # 构建完整卡片
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"✨ 纳米 {agent_name} 完成"},
            "template": "blue"
        },
        "elements": card_elements
    }
    
    return card


def build_web_markdown(results: dict) -> str:
    """
    构建 Web 格式 Markdown（基于规范化结果结构，包含 share_url）
    """
    parts = []
    
    # 获取数据
    summary = results.get("summary", "") or ""
    final_tips = results.get("final_tips", "") or ""
    # 展示顺序：summary -> video -> image -> other -> final_tips -> share_url
    text_content = summary
    videos = results.get("video", [])
    images = results.get("image", [])
    other = results.get("other", [])
    share_url = results.get("share_url", "")
    agent_name = "P视频"
    
    # 标题
    parts.append(f"## ✨ 纳米 {agent_name}")
    parts.append("")
    
    # 文本内容（不裁剪）
    if text_content:
        parts.append(text_content)
        parts.append("")
    
    # 视频
    if videos:
        parts.append("---")
        parts.append("")
        parts.append("### 🎬 视频")
        parts.append("")
        for video in videos:
            desc = video.get("description", "") or ""
            video_title = video.get("title", "") or ""
            video_url = video.get("url", "") or ""
            # description
            if desc:
                parts.append(desc)
            # title
            if video_title:
                parts.append(f"**{video_title}**")
            # url
            if video_url:
                parts.append(f"- [▶️ 查看视频]({video_url})")
            parts.append("")
    
    # 图片
    if images:
        parts.append("---")
        parts.append("")
        parts.append("### 🖼️ 图片")
        parts.append("")
        for img in images:
            desc = img.get("description", "") or ""
            img_title = img.get("title", "") or ""
            img_url = img.get("url", "") or ""
            # description
            if desc:
                parts.append(desc)
            # title
            if img_title:
                parts.append(f"**{img_title}**")
            # url
            if img_url:
                parts.append(f"- [🖼️ 查看图片]({img_url})")
        parts.append("")
    
    # 其他
    if other:
        parts.append("---")
        parts.append("")
        parts.append("### 📦 其他")
        parts.append("")
        for item in other:
            desc = item.get("description", "") or ""
            item_title = item.get("title", "") or ""
            item_url = item.get("url", "") or ""
            # description
            if desc:
                parts.append(desc)
            # title
            if item_title:
                parts.append(f"**{item_title}**")
            # url
            if item_url:
                parts.append(f"- [🔗 查看]({item_url})")
            parts.append("")

    # final_tips 在 other 之后单独展示
    if final_tips:
        parts.append("---")
        parts.append("")
        parts.append("### 💡")
        parts.append("")
        parts.append(final_tips)
        parts.append("")
    
    # 查看详情链接（最重要！）
    if share_url:
        parts.append("---")
        parts.append("")
        parts.append(f"🔗 **[查看详情]({share_url})**")
    
    return "\n".join(parts)


def build_feishu_messages(results: dict) -> list:
    """构建飞书消息（使用卡片格式）"""
    card = build_feishu_card(results)
    return [{"type": "card", "content": card}]


def call_nami_api(
        prompt: str,
        file_data: list,
        timeout: int,
        verbose: bool = True,
        access_token: str = "",
        auth_token: str = "",
        ua: str = "Mozilla/5.0 (Python Upload Script)",
        nami_platform: Optional[str] = None,
        extra_headers: Optional[Dict[str, str]] = None
) -> dict:
    """调用纳米 API（使用 urllib，SSE 流式解析）"""
    
    # 创建带超时控制的 opener（连接超时 30 秒，读取超时 3 小时）
    connect_timeout = CONNECT_TIMEOUT
    read_timeout = timeout
    
    # 构建请求 payload
    payload = {
        "ai_agent_flow_id": DEFAULT_FLOW_ID,
        "prompt": prompt,
        "file": file_data,
        "role_biz": "ai_agent_flow",
        "kwargs": {
            "src": "web_claw"
        }
    }

    data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    cookie_dict = load_cookie_from_config()
    cookie = cookie_dict.get('cookie', '')
    extra_headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }

    if cookie:
        extra_headers.update({
            'Cookie': cookie
        })

    headers = get_signed_headers(
        path='/api/ai_agent_flow/chat',
        access_token=access_token,
        auth_token=auth_token,
        ua=ua,
        nami_platform=nami_platform,
        extra_headers=extra_headers,
    )

    req = urllib.request.Request(
        NAMI_API_BASE,
        data=data_bytes,
        headers=headers,
        method="POST",
    )

    # 启动进度提示
    progress = ProgressPrinter(interval=PROGRESS_INTERVAL, message="正在生成视频，请耐心等候")
    progress.start()

    try:
        final_data = None

        # 使用自定义 opener，设置连接超时和读取超时
        # urllib 不支持直接分开设置，我们通过 socket 设置默认超时
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(connect_timeout)
        
        try:
            # 先尝试连接（短超时）
            with urllib.request.urlopen(req, timeout=connect_timeout) as resp:
                # 连接成功后，使用长超时读取数据
                socket.setdefaulttimeout(read_timeout)
                for raw_line in resp:
                    try:
                        line = raw_line.decode("utf-8", errors="ignore").strip()
                    except Exception:
                        continue

                    if not line:
                        continue

                    # 先检查是否是错误响应（非SSE格式的JSON错误）
                    try:
                        json_data = json.loads(line)
                        if isinstance(json_data, dict):
                            error_code = json_data.get("code")
                            error_msg = json_data.get("msg")
                            if error_code and error_code != 0 and error_code != 200:
                                progress.stop()
                                return {"error": f"API错误: {error_msg} (code: {error_code})"}
                    except (json.JSONDecodeError, ValueError):
                        pass

                    sse_data = parse_sse_data(line)
                    if not sse_data:
                        continue

                    # 检查是否是最终结果
                    if sse_data.get("action") == "final" and sse_data.get("targetKey") == "summary":
                        final_data = sse_data
        finally:
            socket.setdefaulttimeout(old_timeout)

        progress.stop()
        
        if final_data:
            return extract_results(final_data)
        else:
            return {"error": "未获取到最终结果，请稍后重试"}

    except urllib.error.HTTPError as e:
        progress.stop()
        error_msg = f"HTTP错误: {e.code} {e.reason}"
        return {"error": error_msg}
    except urllib.error.URLError as e:
        progress.stop()
        reason = getattr(e, 'reason', str(e))
        if isinstance(reason, socket.timeout):
            return {"error": f"连接超时（{connect_timeout}秒），请检查网络后重试"}
        return {"error": f"请求失败: {reason}"}
    except socket.timeout:
        progress.stop()
        return {"error": f"连接超时（{connect_timeout}秒），请检查网络后重试"}
    except TimeoutError:
        progress.stop()
        error_msg = f"请求超时（{read_timeout}秒）"
        return {"error": error_msg}
    except Exception as e:
        progress.stop()
        return {"error": f"未知错误: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description="纳米 P视频")
    parser.add_argument("-p", "--prompt", required=True, help="用户创意需求")
    parser.add_argument("--file", default="[]", help="附件 JSON 字符串")
    parser.add_argument("--flow-id", default=DEFAULT_FLOW_ID, help="智能体 flow ID")
    parser.add_argument("-q", "--qid", default=DEFAULT_QID, help="业务侧 QID")
    parser.add_argument("-F", "--format", default=DEFAULT_FORMAT, help="输出格式")
    parser.add_argument("-v", "--verbose", action="store_true", default=True, help="打印详细日志")
    parser.add_argument("--no-verbose", dest="verbose", action="store_false", help="关闭详细日志")
    parser.add_argument("--stream", action="store_true", default=True, help="流式输出")
    parser.add_argument("--no-stream", dest="stream", action="store_false", help="关闭流式输出")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"请求超时时间（秒），固定为 {DEFAULT_TIMEOUT} 秒（3小时）")
    parser.add_argument("--channel", default=None, help="消息来源渠道（如 feishu/discord/telegram/web 等），未指定时自动识别")

    args = parser.parse_args()

    # 获取 channel 参数：优先使用命令行指定的值，否则自动识别
    channel = args.channel if args.channel else get_default_channel()

    # 解析 file 参数
    file_data = parse_file_arg(args.file)

    # 调用 API
    results = call_nami_api(
        prompt=args.prompt,
        file_data=file_data,
        timeout=args.timeout,
        verbose=args.verbose
    )

    # 检查是否有错误
    if "error" in results:
        print_channel_error(channel, results["error"])
        sys.exit(1)

    # 根据渠道输出结果
    if is_feishu_channel(channel):
        # 飞书渠道：发送飞书卡片
        card = build_feishu_card(results)
        print(json.dumps(card, ensure_ascii=False))
    else:
        # 其他渠道（web/钉钉/微信/推推等）：输出 Markdown
        markdown = build_web_markdown(results)
        # 输出 markdown
        print(markdown)

    if args.verbose:
        print_feishu_progress("纳米 P视频 完成！")


if __name__ == "__main__":
    main()
