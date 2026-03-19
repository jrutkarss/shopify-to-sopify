import pandas as pd

# --- 1. Load scraped data ---
products = pd.read_csv("products.csv")
variants = pd.read_csv("variants.csv")
images = pd.read_csv("images.csv")

rows = []

# --- 2. Build Shopify rows ---
for _, p in products.iterrows():
    product_id = p.get("id")

    p_variants = variants[variants.get("product_id") == product_id]
    p_images = images[images.get("product_id") == product_id] if "product_id" in images.columns else images[images.get("id") == product_id]

    # Product-level values (change defaults as you like)
    base = {
        "Title": p.get("title", ""),
        "URL handle": p.get("handle", ""),
        "Description": p.get("body_html", ""),
        "Vendor": p.get("vendor", ""),
        "Product category": p.get("product_type", ""),  # or your own mapping
        "Type": p.get("product_type", ""),
        "Tags": p.get("tags", ""),
        "Published on online store": "TRUE",
        "Status": "Active",
        "Charge tax": "TRUE",
        "Tax code": "",
        "Unit price total measure": "",
        "Unit price total measure unit": "",
        "Unit price base measure": "",
        "Unit price base measure unit": "",
        "Requires shipping": "TRUE",
        "Fulfillment service": "manual",
        "Gift card": "FALSE",
        "SEO title": p.get("title", ""),
        "SEO description": "",
        "Color (product.metafields.shopify.color-pattern)": "",
        "Google Shopping / Google product category": "",
        "Google Shopping / Gender": "",
        "Google Shopping / Age group": "",
        "Google Shopping / Manufacturer part number (MPN)": "",
        "Google Shopping / Ad group name": "",
        "Google Shopping / Ads labels": "",
        "Google Shopping / Condition": "New",
        "Google Shopping / Custom product": "FALSE",
        "Google Shopping / Custom label 0": "",
        "Google Shopping / Custom label 1": "",
        "Google Shopping / Custom label 2": "",
        "Google Shopping / Custom label 3": "",
        "Google Shopping / Custom label 4": "",
    }

    # Product image (first image)
    if len(p_images) > 0:
        base["Product image URL"] = p_images.iloc[0].get("src", "")
        base["Image position"] = 1
        base["Image alt text"] = p_images.iloc[0].get("alt", "")
    else:
        base["Product image URL"] = ""
        base["Image position"] = ""
        base["Image alt text"] = ""

    # If a product has no variants for some reason, still create one row
    if p_variants.empty:
        row = base.copy()
        row.update({
            "SKU": "",
            "Barcode": "",
            "Option1 name": "",
            "Option1 value": "",
            "Option1 Linked To": "",
            "Option2 name": "",
            "Option2 value": "",
            "Option2 Linked To": "",
            "Option3 name": "",
            "Option3 value": "",
            "Option3 Linked To": "",
            "Price": "",
            "Compare-at price": "",
            "Cost per item": "",
            "Inventory tracker": "shopify",
            "Inventory quantity": 0,
            "Continue selling when out of stock": "DENY",
            "Weight value (grams)": "",
            "Weight unit for display": "g",
            "Variant image URL": "",
        })
        rows.append(row)
        continue

    for _, v in p_variants.iterrows():
        row = base.copy()

        # Pull variant data safely
        sku = v.get("sku", "")
        barcode = v.get("barcode", "")
        price = v.get("price", "")
        compare_at = v.get("compare_at_price", "")
        grams = v.get("grams", "")
        inventory_qty = v.get("inventory_quantity", 0)

        # Detect options; adjust if your columns are named differently
        size_val = v.get("option1", "") or v.get("title", "")
        color_val = v.get("option2", "")

        # Guarantee: if we set Color option name, we must have a value
        if color_val is None:
            color_val = ""
        color_val = str(color_val).strip()

        # If you *do not* want a Color option when empty, clear both
        if color_val == "":
            opt2_name = ""
            opt2_value = ""
            opt2_linked = ""
        else:
            opt2_name = "Color"
            opt2_value = color_val
            opt2_linked = "product.metafields.shopify.color-pattern"

        # Option1: Size (change if your data differs)
        size_val = "" if size_val is None else str(size_val).strip()
        if size_val == "":
            opt1_name = ""
            opt1_value = ""
            opt1_linked = ""
        else:
            opt1_name = "Size"
            opt1_value = size_val
            opt1_linked = ""

        row.update({
            "SKU": sku,
            "Barcode": barcode,
            "Option1 name": opt1_name,
            "Option1 value": opt1_value,
            "Option1 Linked To": opt1_linked,
            "Option2 name": opt2_name,
            "Option2 value": opt2_value,
            "Option2 Linked To": opt2_linked,
            "Option3 name": "",
            "Option3 value": "",
            "Option3 Linked To": "",
            "Price": price,
            "Compare-at price": compare_at,
            "Cost per item": "",
            "Inventory tracker": "shopify",
            "Inventory quantity": inventory_qty,
            "Continue selling when out of stock": "DENY",
            "Weight value (grams)": grams,
            "Weight unit for display": "g",
            "Variant image URL": "",   # or same as Product image URL if needed
        })

        rows.append(row)

# --- 3. Build final DataFrame with correct column order ---

columns = [
    "Title",
    "URL handle",
    "Description",
    "Vendor",
    "Product category",
    "Type",
    "Tags",
    "Published on online store",
    "Status",
    "SKU",
    "Barcode",
    "Option1 name",
    "Option1 value",
    "Option1 Linked To",
    "Option2 name",
    "Option2 value",
    "Option2 Linked To",
    "Option3 name",
    "Option3 value",
    "Option3 Linked To",
    "Price",
    "Compare-at price",
    "Cost per item",
    "Charge tax",
    "Tax code",
    "Unit price total measure",
    "Unit price total measure unit",
    "Unit price base measure",
    "Unit price base measure unit",
    "Inventory tracker",
    "Inventory quantity",
    "Continue selling when out of stock",
    "Weight value (grams)",
    "Weight unit for display",
    "Requires shipping",
    "Fulfillment service",
    "Product image URL",
    "Image position",
    "Image alt text",
    "Variant image URL",
    "Gift card",
    "SEO title",
    "SEO description",
    "Color (product.metafields.shopify.color-pattern)",
    "Google Shopping / Google product category",
    "Google Shopping / Gender",
    "Google Shopping / Age group",
    "Google Shopping / Manufacturer part number (MPN)",
    "Google Shopping / Ad group name",
    "Google Shopping / Ads labels",
    "Google Shopping / Condition",
    "Google Shopping / Custom product",
    "Google Shopping / Custom label 0",
    "Google Shopping / Custom label 1",
    "Google Shopping / Custom label 2",
    "Google Shopping / Custom label 3",
    "Google Shopping / Custom label 4",
]

df_final = pd.DataFrame(rows, columns=columns)

# --- 4. Save for Shopify import ---
df_final.to_csv("final_shopify_import.csv", index=False)
print("final_shopify_import.csv generated")
