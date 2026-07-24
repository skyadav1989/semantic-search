from sympy.sets import conditionset
try:
    from qdrant_client.http.models import (
        Filter,
        FieldCondition,
        MatchValue,
        Range,
    )
except ImportError:
    Filter = FieldCondition = MatchValue = Range = None


class MetadataFilterBuilder:
    """
    Convert extracted query attributes into Qdrant filters.
    """

    def build(self, attributes: dict):

        conditions = []

        #
        # Fallback (older qdrant client)
        #
        if Filter is None:

            if "category" in attributes:
                conditions.append({
                    "key": "category",
                    "match": {
                        "value": attributes["category"]
                    }
                })
            
            #
            # Subcategory
            #
            if "subcategory" in attributes:
                conditions.append(
                    FieldCondition(
                        key="subcategory",
                        match=MatchValue(
                            value=attributes["subcategory"]
                        ),
                    )
                )

            

            if "color" in attributes:
                conditions.append({
                    "key": "color",
                    "match": {
                        "value": attributes["color"]
                    }
                })

            if "brand" in attributes:
                conditions.append({
                    "key": "brand",
                    "match": {
                        "value": attributes["brand"]
                    }
                })

            if "price" in attributes:
                conditions.append({
                    "key": "price",
                    "range": attributes["price"],
                })

            return {"must": conditions}

        #
        # Category
        #
        if "category" in attributes:
            conditions.append(
                FieldCondition(
                    key="category",
                    match=MatchValue(
                        value=attributes["category"]
                    ),
                )
            )

        #
        # Color
        #
        if "color" in attributes:
            conditions.append(
                FieldCondition(
                    key="color",
                    match=MatchValue(
                        value=attributes["color"]
                    ),
                )
            )

        #
        # Brand
        #
        if "brand" in attributes:
            conditions.append(
                FieldCondition(
                    key="brand",
                    match=MatchValue(
                        value=attributes["brand"]
                    ),
                )
            )

        # Price
        #

        #
        # QueryProcessor format
        #
        if "max_price" in attributes or "min_price" in attributes:

            conditions.append(
                FieldCondition(
                    key="price",
                    range=Range(
                        gte=attributes.get("min_price"),
                        lte=attributes.get("max_price"),
                    ),
                )
            )

        #
        # Backward compatibility
        #
        elif "price" in attributes:

            price = attributes["price"]

            conditions.append(
                FieldCondition(
                    key="price",
                    range=Range(
                        gte=price.get("gte"),
                        lte=price.get("lte"),
                    ),
                )
            )

        return Filter(must=conditions)