import pandas as pd

# Load pickle file
df = pd.read_pickle("products_desc_tags_vec.pkl")

# Save as CSV
df.to_csv("products_desc_tags_vec.csv", index=False)