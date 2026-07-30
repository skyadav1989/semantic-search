from __future__ import annotations

import logging
from collections import Counter

from .attribute_facets import AttributeFacetBuilder
from .price_bucket import PriceBucketBuilder
from .utils import (
    increment,
    counter_to_facet,
    remove_empty_facets,
)
from .constants import FACET_LIMIT

logger = logging.getLogger(__name__)


class FacetBuilder:

    def __init__(self):

        self.attribute_builder = AttributeFacetBuilder()
        self.price_builder = PriceBucketBuilder()

    def build(self, results):

        brand_counter = Counter()
        category_counter = Counter()
        subcategory_counter = Counter()
        stock_counter = Counter()

        logger.info("=" * 60)
        logger.info("Facet Builder Started")
        logger.info("Input Products : %d", len(results))

        for item in results:

            payload = item.get("payload", {})

            increment(brand_counter, payload.get("brand"))
            increment(category_counter, payload.get("category"))
            increment(subcategory_counter, payload.get("subcategory"))
            increment(stock_counter, payload.get("stock_status"))

        attribute_facets = self.attribute_builder.build(results)

        price_counter = Counter()

        for bucket, count in self.price_builder.build(results).items():
            price_counter[bucket] = count

        facets = {
            "brand": counter_to_facet(brand_counter, FACET_LIMIT),
            "category": counter_to_facet(category_counter, FACET_LIMIT),
            "subcategory": counter_to_facet(subcategory_counter, FACET_LIMIT),
            "stock_status": counter_to_facet(stock_counter, FACET_LIMIT),
            "price": counter_to_facet(price_counter, FACET_LIMIT),
        }

        facets.update(attribute_facets)

        return remove_empty_facets(facets)