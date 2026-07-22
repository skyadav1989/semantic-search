import re


class AttributeExtractor:

    COLORS = {
        "white",
        "black",
        "blue",
        "red",
        "brown",
        "ivory",
        "grey",
        "gray",
        "gold",
        "silver",
    }

    def extract(self, query: str):

        q = query.lower()

        data = {}

        #
        # Color
        #
        for color in self.COLORS:
            if color in q:
                data["color"] = color
                break

        #
        # Price Filters
        #

        # under 5000 / below 5000
        m = re.search(r"(?:under|below)\s*₹?\s*([\d,]+)", q)
        if m:
            data["price"] = {
                "lte": int(m.group(1).replace(",", ""))
            }

        # above 5000 / over 5000
        m = re.search(r"(?:above|over)\s*₹?\s*([\d,]+)", q)
        if m:
            data["price"] = {
                "gte": int(m.group(1).replace(",", ""))
            }

        # between 3000 and 5000
        m = re.search(
            r"between\s*₹?\s*([\d,]+)\s*(?:and|-)\s*₹?\s*([\d,]+)",
            q,
        )

        if m:
            data["price"] = {
                "gte": int(m.group(1).replace(",", "")),
                "lte": int(m.group(2).replace(",", "")),
            }

        return data