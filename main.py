from shopify_scraper import scraper

url = "https://www.beyours.in/"

parents = scraper.get_products(url)
parents.to_csv('products.csv', index=False)
print('Parents: ', len(parents))


children = scraper.get_variants(parents)
children.to_csv('variants.csv', index=False)
print('Children: ', len(children))


images = scraper.get_images(parents)
images.to_csv('images.csv', index=False)
print('Images: ', len(images))
