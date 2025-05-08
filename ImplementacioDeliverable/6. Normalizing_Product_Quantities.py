import pandas as pd
import re

# Load the Excel file
df = pd.read_excel("products.xlsx")

# Helper function to normalize quantity
def normalize_quantity(qty_str):
    if pd.isnull(qty_str):
        return None

    qty_str = str(qty_str).lower().replace(",", ".").strip()

    # Handle "loose per kilo", "loose per 500 g"
    if "loose per kilo" in qty_str:
        return 1000
    if "loose per 500 g" in qty_str or "loose per 500g" in qty_str:
        return 500

    # Handle "approx. 270 g", "ca. 755 g", etc.
    approx_match = re.search(r"(approx\.?|ca\.)\s*([\d\.]+)\s*([a-z]+)", qty_str)
    if approx_match:
        amount = float(approx_match.group(2))
        unit = approx_match.group(3)
        if unit in ["g", "gram", "grams"]:
            return amount
        elif unit in ["kg", "kilogram", "kilograms"]:
            return amount * 1000
        elif unit in ["ml", "milliliter", "milliliters"]:
            return amount
        elif unit in ["cl"]:
            return amount * 10
        elif unit in ["l", "lt", "liter", "liters"]:
            return amount * 1000

    # Match patterns like "6 x 33 cl", "4 x 250 g", etc.
    match = re.match(r"(\d+)\s*x\s*([\d\.]+)\s*([a-z]+)", qty_str)
    if match:
        count = int(match.group(1))
        amount = float(match.group(2))
        unit = match.group(3)
        if unit in ["g", "gram", "grams"]:
            return count * amount
        elif unit in ["kg", "kilogram", "kilograms"]:
            return count * amount * 1000
        elif unit in ["ml", "milliliter", "milliliters"]:
            return count * amount
        elif unit in ["cl"]:
            return count * amount * 10
        elif unit in ["l", "lt", "liter", "liters"]:
            return count * amount * 1000

    # Match single quantity with unit like "250 g", "1.5 l"
    match = re.match(r"([\d\.]+)\s*([a-z]+)", qty_str)
    if match:
        amount = float(match.group(1))
        unit = match.group(2)
        if unit in ["g", "gram", "grams"]:
            return amount
        elif unit in ["kg", "kilogram", "kilograms"]:
            return amount * 1000
        elif unit in ["ml", "milliliter", "milliliters"]:
            return amount
        elif unit in ["cl"]:
            return amount * 10
        elif unit in ["l", "lt", "liter", "liters"]:
            return amount * 1000

    # If only a number, assume grams
    if qty_str.replace(".", "", 1).isdigit():
        return float(qty_str)

    return None  # Leave as None if format isn't recognized

# Apply normalization
df["quantity_normalized"] = df["quantity"].apply(normalize_quantity)

# Save to a new Excel file
output_path = "Normalizing_Quantities.py.xlsx"
df.to_excel(output_path, index=False)

output_path