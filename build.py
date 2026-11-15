#!/usr/bin/env python3
"""
太陽電玩組件庫 建置腳本

components/*.html 是「片段」（只有該組件自己的 <style>、標記、<script>），
開頭用註解寫明資訊。執行本腳本後：
  dist/<組件>.html   → 已合併設計變數與基礎樣式、可直接開啟或複製使用的完整單一 HTML
  index.html          → 所有組件的預覽目錄
  components.json     → 組件清單（給 Claude 查詢用）

用法：python3 build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "components"
DIST = ROOT / "dist"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800'
    '&family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">'
)

# 讓預覽頁可用 ?theme=dark / ?theme=light 指定配色
THEME_INIT = (
    "<script>(function(){try{var t=new URLSearchParams(location.search).get('theme');"
    "if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>"
)

CATEGORY_ORDER = ["導覽", "主視覺", "內容區塊", "卡片", "表單", "回饋提示", "資料呈現", "文字與背景", "小工具"]

# 整頁範本：(檔名, 標題, 依序組合的組件)
TEMPLATES = [
    ("landing", "太陽電玩 首頁範本", ["navbar", "hero-split", "logo-marquee", "feature-rows", "bento-grid",
                                   "steps-timeline", "pricing", "testimonials", "faq", "cta-band", "footer"]),
]

META_KEYS ={"名稱": "name", "分類": "cat", "說明": "desc", "來源": "source", "適用": "use", "高度": "height"}


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->", text, re.S)
    if not m:
        raise SystemExit(f"{path.name} 缺少開頭說明註解")
    meta = {"id": path.stem}
    for line in m.group(1).strip().splitlines():
        if ":" in line or "：" in line:
            k, v = re.split(r"[:：]", line, maxsplit=1)
            key = META_KEYS.get(k.strip())
            if key:
                meta[key] = v.strip()
    meta["height"] = int(meta.get("height", 520))
    body = text[m.end():].strip()
    return meta, body


def page(title: str, body: str, tokens: str, base: str) -> str:
    return (
        "<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{html.escape(title)}</title>\n{FONTS}\n{THEME_INIT}\n"
        f"<style>\n{tokens}\n{base}\n</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )


def main():
    tokens = (ROOT / "core/tokens.css").read_text(encoding="utf-8")
    base = (ROOT / "core/base.css").read_text(encoding="utf-8")
    DIST.mkdir(exist_ok=True)
    items = []
    for path in sorted(SRC.glob("*.html")):
        meta, body = parse(path)
        (DIST / path.name).write_text(page(meta["name"], body, tokens, base), encoding="utf-8")
        items.append(meta)
    order = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    items.sort(key=lambda x: (order.get(x.get("cat"), 99), x["id"]))
    (ROOT / "components.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    # 範本：把多個組件組合成一整頁（去掉 <!--demo-->…<!--/demo--> 示範用內容）
    bodies = {m["id"]: b for m, b in (parse(p) for p in SRC.glob("*.html"))}
    (ROOT / "templates").mkdir(exist_ok=True)
    for name, title, ids in TEMPLATES:
        parts = [re.sub(r"<!--demo-->.*?<!--/demo-->", "", bodies[i], flags=re.S) for i in ids]
        (ROOT / "templates" / f"{name}.html").write_text(page(title, "\n\n".join(parts), tokens, base), encoding="utf-8")

    tpl = (ROOT / "core/catalog.html").read_text(encoding="utf-8")
    out = tpl.replace("/*__ITEMS__*/[]", json.dumps(items, ensure_ascii=False))
    out = out.replace("/*__CATS__*/[]", json.dumps(CATEGORY_ORDER, ensure_ascii=False))
    out = out.replace("/*__TOKENS__*/", tokens).replace("/*__BASE__*/", base)
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"完成：{len(items)} 個組件")


if __name__ == "__main__":
    main()
