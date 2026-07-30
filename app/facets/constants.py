"""
Facet Engine Constants

Shared constants used across the Facet Engine.
"""

from __future__ import annotations

#
# Maximum values returned per facet
#
FACET_LIMIT = 10

#
# Enable / Disable facet generation
#
ENABLE_FACETS = True

#
# Default price buckets
#
# These will eventually come from:
#
# settings.PRICE_BUCKETS
#
DEFAULT_PRICE_BUCKETS = [
    (0, 1000),
    (1000, 2000),
    (2000, 3000),
    (3000, 5000),
    (5000, 10000),
    (10000, None),
]

#
# Attributes ignored while building dynamic facets.
#
# These usually have little filtering value.
#
IGNORE_ATTRIBUTES = {
    "manufactured_by",
    "country_of_origin",
    "net_contents",
    "packaging_dimensions",
    "description",
    "images",
    "image",
    "url",
    "product_id",
    "sku",
    "title",
}

#
# Ignore empty values
#
IGNORE_VALUES = {
    "",
    "-",
    "--",
    "N/A",
    "NA",
    "None",
    None,
}

#
# High-cardinality attributes
#
# These are searchable but should not become facets.
#
HIGH_CARDINALITY_ATTRIBUTES = {
    "model_number",
    "serial_number",
    "ean",
    "upc",
    "isbn",
}

#
# Preferred facet ordering in API response
#
FACET_ORDER = [
    "category",
    "subcategory",
    "brand",
    "price",
    "stock_status",
]

#
# Maximum distinct values before suppressing a facet.
#
# Prevents facets such as:
# warranty_number
# serial_number
#
MAX_UNIQUE_VALUES = 100

#
# Numeric attributes that should be sorted numerically.
#
NUMERIC_ATTRIBUTES = {
    "sweep_size",
    "screen_size",
    "capacity",
    "power_consumption",
    "weight",
    "height",
    "width",
    "depth",
    "air_delivery",
}

#
# Boolean values normalization
#
BOOLEAN_TRUE = {
    "yes",
    "true",
    "1",
}

BOOLEAN_FALSE = {
    "no",
    "false",
    "0",
}