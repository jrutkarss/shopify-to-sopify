# ShopifyScraper

ShopifyScraper is a Python package that scrapes data from Shopify. Unlike a regular web scraper, that needs to visit every page on a site, this package fetches Shopify's publicly visible `products.json` file, allowing you to scrape an entire store inventory in seconds.

When the commands below are run, ShopifyScraper will extract the store inventory and save the products and product variants to Pandas dataframes, from where you can access or analyse the data or write it to CSV or database. 

### Installation
To install ShopifyScraper, run the following command:

```bash
pip3 install git+https://github.com/practical-data-science/ShopifyScraper.git
```
after that clone this repository.
```git clone https://github.com/easikdevops/shopify-to-sopify.git
cd shopify-to-sopify
```

### Usage

```nano main.py # cahnge your domain name
python3 main.py
python3 final_import_file.py
```

