from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

PAYPAL_DOC_URLS = [
    "https://developer.paypal.com/api/rest/",
    "https://developer.paypal.com/docs/api/orders/v2/",
    "https://developer.paypal.com/docs/api/payments/v2/",
    "https://developer.paypal.com/docs/api/invoicing/v2/",
    "https://developer.paypal.com/docs/api/subscriptions/v1/",
    "https://developer.paypal.com/docs/api/transaction-search/v1/",
    "https://developer.paypal.com/docs/api/customer-disputes/v1/",
    "https://developer.paypal.com/docs/api/webhooks/v1/",
    "https://developer.paypal.com/docs/api/partner-referrals/v2/",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download PayPal docs for RAG.")
    parser.add_argument("--out", type=Path, default=Path("data/paypal_docs"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for url in PAYPAL_DOC_URLS:
            response = client.get(url)
            response.raise_for_status()
            text = _html_to_markdown(url, response.text)
            path = args.out / (_slug(url) + ".md")
            path.write_text(text, encoding="utf-8")
            print(path)
    return 0


def _html_to_markdown(url: str, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else url
    body = soup.get_text("\n", strip=True)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return f"# {title}\n\nSource: {url}\n\n{body}\n"


def _slug(url: str) -> str:
    parsed = urlparse(url)
    value = (parsed.netloc + parsed.path).strip("/")
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()


if __name__ == "__main__":
    raise SystemExit(main())
