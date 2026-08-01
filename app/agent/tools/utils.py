"""
Agent tool helpers.
"""

from __future__ import annotations

from typing import Any

from app.agent.models import ProductSummary


def product_from_payload(payload: dict[str, Any]) -> ProductSummary:
    return ProductSummary(
        sku=str(payload.get("sku") or ""),
        title=str(payload.get("title") or payload.get("name") or ""),
        category=payload.get("category"),
        subcategory=payload.get("subcategory"),
        brand=payload.get("brand"),
        price=payload.get("price"),
        mrp=payload.get("mrp"),
        stock_status=payload.get("stock_status"),
        url=payload.get("url") or payload.get("product_url"),
        image=payload.get("image") or payload.get("image_url"),
        attributes=payload.get("attributes") or {},
    )


def products_from_results(results: list[dict]) -> list[ProductSummary]:
    products = []
    for item in results:
        payload = item.get("payload", {})
        products.append(product_from_payload(payload))
    return products
