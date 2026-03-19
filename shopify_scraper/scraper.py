"""
Shopify scraper
Description: Scrapes products from a Shopify store by parsing products.json and converting it to a pandas DataFrame.
Author: Matt Clarke (fixed for pandas 2.0+ compatibility)
"""

import json
import pandas as pd
import requests

def get_json(url, page):
    """
    Get Shopify products.json from a store URL.
    Args:
        url (str): URL of the store.
        page (int): Page number of the products.json.
    Returns:
        products_json: Products.json from the store.
    """
    try:
        response = requests.get(f'{url}/products.json?limit=250&page={page}', timeout=5)
        products_json = response.text
        response.raise_for_status()
        return products_json
    except requests.exceptions.HTTPError as error_http:
        print("HTTP Error:", error_http)
    except requests.exceptions.ConnectionError as error_connection:
        print("Connection Error:", error_connection)
    except requests.exceptions.Timeout as error_timeout:
        print("Timeout Error:", error_timeout)
    except requests.exceptions.RequestException as error:
        print("Error: ", error)
    return None

def to_df(products_json):
    """
    Convert products.json to a pandas DataFrame.
    Args:
        products_json (json): Products.json from the store.
    Returns:
        df: Pandas DataFrame of the products.json.
    """
    try:
        products_dict = json.loads(products_json)
        df = pd.DataFrame.from_dict(products_dict['products'])
        return df
    except Exception as e:
        print(e)
        return pd.DataFrame()

def get_products(url):
    """
    Get all products from a store.
    Returns:
        df: Pandas DataFrame of the products.json.
    """
    results = True
    page = 1
    df = pd.DataFrame()
    while results:
        products_json = get_json(url, page)
        if products_json is None:
            break
        products_dict = to_df(products_json)
        if len(products_dict) == 0:
            break
        else:
            df = pd.concat([df, products_dict], ignore_index=True)
            page += 1
    df['url'] = f"{url}/products/" + df['handle']
    return df

def get_variants(products):
    """Get variants from a list of products.
    Args:
        products (pd.DataFrame): Pandas dataframe of products from get_products()
    Returns:
        variants (pd.DataFrame): Pandas dataframe of variants
    """
    df_variants = pd.DataFrame()
    for row in products.itertuples(index=True):
        for variant in getattr(row, 'variants', []):
            df_variants = pd.concat([df_variants, pd.DataFrame.from_records([variant])], ignore_index=True)
    
    if not df_variants.empty:
        df_variants['id'] = df_variants['id'].astype(int)
        df_variants['product_id'] = df_variants['product_id'].astype(int)
    df_parent_data = products[['id', 'title', 'vendor']].rename(columns={'title': 'parent_title', 'id': 'parent_id'})
    return df_variants.merge(df_parent_data, left_on='product_id', right_on='parent_id', how='left')

def json_list_to_df(df, col):
    """Return a Pandas dataframe based on a column that contains a list of JSON objects.
    Args:
        df (Pandas dataframe): The dataframe to be flattened.
        col (str): The name of the column that contains the JSON objects.
    Returns:
        Pandas dataframe: A new dataframe with the JSON objects expanded into columns.
    """
    rows = []
    for index, row in df[col].items():
        for item in row:
            rows.append(item)
    return pd.DataFrame(rows)

def get_images(df_products):
    """Get images from a list of products.
    Args:
        df_products (pd.DataFrame): Pandas dataframe of products from get_products()
    Returns:
        images (pd.DataFrame): Pandas dataframe of images
    """
    return json_list_to_df(df_products, 'images')

# # Example usage:
# if __name__ == "__main__":
#     # Replace with target Shopify store URL
#     store_url = "https://www.beyours.in"
#     products = get_products(store_url)
#     print(f"Found {len(products)} products")
    
#     variants = get_variants(products)
#     print(f"Found {len(variants)} variants")
    
#     images = get_images(products)
#     print(f"Found {len(images)} images")
    
#     # Save to CSV
#     products.to_csv('products.csv', index=False)
#     variants.to_csv('variants.csv', index=False)
#     images.to_csv('images.csv', index=False)
#     print("Data saved to CSV files")
