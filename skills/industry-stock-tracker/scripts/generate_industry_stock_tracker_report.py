"""
行业/个股跟踪报告生成脚本。

输入:
- query (用户原始问题)

输出(JSON):
- title: 报告标题
- content: 按 skill 规范生成的正文(仅总结章节)
- attachments: PDF/DOCX 保存路径

错误处理:
- ERROR_ENTITY -> "目前暂不支持此类实体体进行分析。"
- 其他异常 -> "报告生成服务暂时不可用，请稍后重试。"
"""

import argparse
import base64
import json
import os
import socket
import sys
import urllib.error
import urllib.request
import traceback
import uuid
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


API_URL = "https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/write/tracking/report"
API_KEY = os.environ.get("EM_API_KEY", "")
TOOL_NAME = "行业/个股跟踪报告"
SKILL_SLUG = "industry_stock_tracker"
DEFAULT_OUTPUT_DIR = Path.cwd() / "miaoxiang" / SKILL_SLUG

ERROR_ENTITY_MSG = "目前暂不支持此类实体体进行分析。"
GENERAL_ERROR_MSG = "报告生成服务暂时不可用，请稍后重试。"


class ApiCallError(Exception):
    def __init__(self, code: str, detail: str):
        Exception.__init__(self, detail)
        self.code = code
        self.detail = detail


def _safe_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _clean_report_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    # 去掉内部协议链接（如 blockTitle://、table://）
    cleaned = re.sub(r"\[[^\]]*\]\((?:blockTitle|table)://[^)]*\)", "", cleaned)
    # 普通 markdown 链接转纯文本，仅保留标题
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    # 规范化换行和空白
    cleaned = cleaned.replace("\\n", "\n")
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _read_query_from_stdin() -> str:
    raw = sys.stdin.read().strip()
    if not raw:
        return ""
    try:
        payload = json.loads(raw)
        if isinstance(payload, dict):
            return _safe_str(payload.get("query", ""))
        if isinstance(payload, str):
            return payload.strip()
    except json.JSONDecodeError:
        return raw
    return ""

def _call_api(query: str, timeout: float = 1200.0) -> Dict[str, Any]:
    req_body = json.dumps({"query": query}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        method="POST",
        data=req_body,
        headers={
            "Content-Type": "application/json",
            "em_api_key": API_KEY,
            "Accept": "application/json",
            "User-Agent": "industry-stock-tracker/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status_code = getattr(resp, "status", None) or resp.getcode()
            content = resp.read()

    except urllib.error.HTTPError as e:
        raw = e.read() if hasattr(e, "read") else b""
        snippet = raw[:500].decode("utf-8", errors="replace")
        raise ApiCallError("HTTP_ERROR", "status={0}, body={1}".format(e.code, snippet))
    except socket.timeout:
        raise ApiCallError("TIMEOUT", "read operation timed out")
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", e)
        if isinstance(reason, socket.timeout):
            raise ApiCallError("TIMEOUT", "read operation timed out")
        raise ApiCallError("NETWORK_ERROR", _safe_str(reason))

    text = content.decode("utf-8", errors="replace")
    if status_code and int(status_code) >= 400:
        raise ApiCallError("HTTP_ERROR", "status={0}, body={1}".format(status_code, text[:500]))

    try:
        parsed = json.loads(text) if text else {}
    except Exception:
        raise ApiCallError("INVALID_JSON", text[:500])

    return parsed if isinstance(parsed, dict) else {"data": parsed}


def _unwrap_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    for key in ("data", "result", "content"):
        node = payload.get(key)
        if isinstance(node, dict):
            return node
    return payload

def _default_output_dir() -> str:
    """
    Allow overriding attachment output directory via env:
      INDUSTRY_STOCK_TRACKER_OUTPUT_DIR
    """
    env = os.environ.get("INDUSTRY_STOCK_TRACKER_OUTPUT_DIR", "").strip()
    return env or str(DEFAULT_OUTPUT_DIR)

def _decode_attachment_base64(data: Dict[str, Any], output_dir: str) -> List[Dict[str, str]]:
    attachments: List[Dict[str, str]] = []
    os.makedirs(output_dir, exist_ok=True)

    file_map = [
        ("wordBase64", "docx", "DOCX"),
        ("pdfBase64", "pdf", "PDF"),
    ]
    article_id = _safe_str(data.get("articleId"), default=uuid.uuid4().hex)
    safe_article_id = re.sub(r"[^a-zA-Z0-9_-]+", "_", article_id)

    for key, ext, ftype in file_map:
        b64_str = _safe_str(data.get(key))
        if not b64_str:
            continue
        try:
            raw = base64.b64decode(b64_str)
        except Exception:
            continue
        file_name = "{0}_{1}.{2}".format(safe_article_id, ftype.lower(), ext)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(raw)
        attachments.append({"type": ftype, "url": file_path})
    return attachments

def _render_content(entity_type: str, summary_content: str, seven_cards_analysis: Optional[Dict] = None, catalyst_summary: Optional[str] = None) -> str:
    """
    渲染报告内容，新增七张底牌评估和催化剂扫描
    
    Args:
        entity_type: 行业/个股
        summary_content: 原始总结内容
        seven_cards_analysis: 七张底牌评估结果（可选）
        catalyst_summary: 催化剂扫描摘要（可选）
    """
    base_content = (
        f"已生成{entity_type}跟踪报告，包括行业和个股的多种信源摘要。"
        "此处省略正文内容，仅展示总结章节，如需查看完整内容，请查看附件获取报告详情。\n\n"
        f"{summary_content}"
    )
    
    # 添加七张底牌评估（如果有）
    if seven_cards_analysis:
        seven_cards_section = "\n\n## 七张底牌契合度评估\n\n"
        seven_cards_section += "| 底牌 | 契合度 | 核心逻辑 |\n"
        seven_cards_section += "|------|--------|----------|\n"
        
        for card, data in seven_cards_analysis.items():
            seven_cards_section += f"| {card} | {data.get('rating', 'N/A')} | {data.get('logic', '待补充')} |\n"
        
        base_content += seven_cards_section
        
        if seven_cards_analysis.get('overall_rating'):
            base_content += f"\n**综合评级**：{seven_cards_analysis['overall_rating']}\n"
    
    # 添加催化剂扫描（如果有）
    if catalyst_summary:
        base_content += f"\n\n## 未来催化剂\n\n{catalyst_summary}\n"
    
    return base_content


def build_report_output(
    query: str,
    payload: Dict[str, Any],
    seven_cards_analysis: Optional[Dict] = None,
    catalyst_summary: Optional[str] = None
) -> Dict[str, Any]:
    """
    构建报告输出，支持七张底牌评估和催化剂扫描
    
    Args:
        query: 用户查询
        payload: API 响应
        seven_cards_analysis: 七张底牌评估结果（可选）
        catalyst_summary: 催化剂扫描摘要（可选）
    """
    raw_data = payload.get("data") if isinstance(payload, dict) else None
    data = _unwrap_data(payload)
    code = _safe_str(payload.get("code") if isinstance(payload, dict) else "")
    message = _safe_str(payload.get("message") if isinstance(payload, dict) else "")

    # 明确错误码处理
    if code == "ERROR_ENTITY" or _safe_str(data.get("code")) == "ERROR_ENTITY":
        return {"ok": False, "error_code": "ERROR_ENTITY", "message": ERROR_ENTITY_MSG}

    # 简化规则：message 有值且 data 为空，直接返回接口 message
    if message and not raw_data:
        return {
            "ok": False,
            "error_code": code or "API_ERROR",
            "message": message,
        }

    title = _safe_str(data.get("title"), default="行业/个股跟踪报告")
    share_url = _safe_str(data.get("shareUrl"), default="无")
    entity_type = _safe_str(data.get("entityType") or data.get("entity_type"), default="行业/个股")
    summary = _safe_str(data.get("content"), default="")
    attachments = _decode_attachment_base64(data, _default_output_dir())
    # traceability = _extract_traceability(data)

    if not summary:
        summary = "暂无总结内容，请查看附件获取报告详情。"

    output = {
        "ok": True,
        "tool": TOOL_NAME,
        "query": query,
        "title": title,
        "content": _render_content(
            entity_type=entity_type,
            summary_content=summary,
            seven_cards_analysis=seven_cards_analysis,
            catalyst_summary=catalyst_summary
        ),
        "attachments": attachments,
        "share_url": share_url,
        "seven_cards_analysis": seven_cards_analysis,
        "catalyst_summary": catalyst_summary
    }
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成行业/个股跟踪报告")
    parser.add_argument("--query", type=str, default="", help="用户查询文本")
    parser.add_argument("--seven-cards", action="store_true", help="启用七张底牌评估")
    parser.add_argument("--catalyst", action="store_true", help="启用催化剂扫描")
    parser.add_argument("--stock-code", type=str, default="", help="股票代码（用于七张底牌评估）")
    return parser.parse_args()


def _mock_seven_cards_analysis(stock_code: str) -> Dict[str, Any]:
    """
    模拟七张底牌评估（实际应调用 seven-cards-evaluator skill）
    TODO: 集成真实的 seven-cards-evaluator
    """
    # 这里返回示例数据，实际应调用外部 API 或 skill
    return {
        "1. AI 端侧和算力端": {"rating": "A", "logic": "AI 算力需求爆发"},
        "2. 光模块→光互联": {"rating": "S", "logic": "明年利润 1100 亿，PE 不到 10 倍"},
        "3. PCB": {"rating": "A", "logic": "H1 半年报验证 100% 业绩暴增"},
        "4. 液冷": {"rating": "B", "logic": "8-9 月成为市场焦点"},
        "5. 先进封装+HBM+SSD": {"rating": "A", "logic": "彩蛋环节，最容易被低估"},
        "6. AI 电力/储能": {"rating": "C", "logic": "等到 9-10 月后"},
        "7. 有色金属": {"rating": "B", "logic": "明年主线，银锡钼是主线"},
        "overall_rating": "S 级（核心契合）"
    }


def _mock_catalyst_scan(stock_code: str) -> str:
    """
    模拟催化剂扫描（实际应调用催化剂扫描工具）
    TODO: 集成真实的 catalyst-calendar skill
    """
    return (
        "1. **6 月 16-17 日**：PCB 半年报验证，关注业绩暴增 100%+ 龙头\n"
        "2. **7 月底前**：长鑫科技上市，半导体设备情绪催化\n"
        "3. **8-9 月**：液冷成为市场焦点\n"
        "4. **9-10 月后**：电力/储能发力\n"
        "5. **财报季**：关注光模块龙头订单情况"
    )


def main() -> None:
    args = parse_args()
    query = _safe_str(args.query) or _read_query_from_stdin()
    if not query:
        print(
            json.dumps(
                {"ok": False, "error_code": "BAD_REQUEST", "message": "缺少 query 参数"},
                ensure_ascii=False,
            )
        )
        sys.exit(1)

    try:
        # 调用 API 生成基础报告
        payload = _call_api(query=query)
        
        # 可选：七张底牌评估
        seven_cards_analysis = None
        if args.seven_cards and args.stock_code:
            seven_cards_analysis = _mock_seven_cards_analysis(args.stock_code)
        
        # 可选：催化剂扫描
        catalyst_summary = None
        if args.catalyst and args.stock_code:
            catalyst_summary = _mock_catalyst_scan(args.stock_code)
        
        # 构建输出（支持七张底牌和催化剂）
        output = build_report_output(
            query=query,
            payload=payload,
            seven_cards_analysis=seven_cards_analysis,
            catalyst_summary=catalyst_summary
        )
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0 if output.get("ok") else 2)
    except ApiCallError as e:
        err = {
            "ok": False,
            "error_code": e.code,
            "message": GENERAL_ERROR_MSG,
            "detail": e.detail,
        }
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(2)
    except Exception as e:
        err = {
            "ok": False,
            "error_code": "UNEXPECTED_ERROR",
            "message": GENERAL_ERROR_MSG,
            "detail": _safe_str(e),
            "traceback": traceback.format_exc(limit=8),
        }
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(2)


if __name__ == "__main__":
    main()
