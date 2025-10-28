import requests
from bs4 import BeautifulSoup
# from IPython.display import Image, display
import json

def crawl_web_ikea(url):

  url = url

  def crawl_web(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.text
    except requests.exceptions.RequestException as e:
      print(f"Error fetching URL: {e}")
      return None
  content = crawl_web(url)

  def extract_item_name_by_class():

    soup = BeautifulSoup(content, 'html.parser')

    name_div = soup.find('div', class_='d-flex flex-row itemNameProduct')
    details_div = soup.find('div', class_='itemDetails d-flex')

    item_name = name_div.get_text(strip=True) if name_div else None
    item_details = details_div.get_text(strip=True) if details_div else None

    if item_name and item_details:
        return f"{item_name} - {item_details}"
    elif item_name:
        return item_name
    elif item_details:
        return item_details
    else:
        print("Error: Neither the item name div nor the item details div was found.")
        return None
  item_name = extract_item_name_by_class()

  def extract_price_by_class():
    soup = BeautifulSoup(content, 'html.parser')
    target_div = soup.find('div', class_='itemPriceBox itemPriceBox-container')

    if target_div:
      element_with_price = target_div.find(attrs={'data-price': True})
      if element_with_price and 'data-price' in element_with_price.attrs:
        return element_with_price['data-price']
      else:
        print("Error: 'data-price' attribute not found within the div with class 'itemPriceBox itemPriceBox-container'.")
        return None
    else:
      print("Error: The specified div with class was not found.")
      return None
  item_price = extract_price_by_class()

  def extract_images_by_class():
    soup = BeautifulSoup(content, 'html.parser')
    image_div = soup.find('div', class_='slick slick-pip-images')
    image_url = None
    if image_div:
        first_img = image_div.find('img', attrs={'data-lazy': True})
        if first_img:
            image_url = first_img['data-lazy']
        return image_url
    else:
      print(f"Error: The specified div with class was not found.")
      return None
  image_urls_link = extract_images_by_class()

  # def display_images_from_urls(image_urls):
  #   if image_urls:
  #     for url in image_urls:
  #       try:
  #         response = requests.get(url, stream=True)
  #         response.raise_for_status()  # Raise an exception for bad status codes
  #         display(Image(response.content))
  #       except requests.exceptions.RequestException as e:
  #         print(f"Error fetching image from URL {url}: {e}")
  #   else:
  #     print("No image URLs provided to display.")
  # image_content = display_images_from_urls(image_urls_link)

  return item_name, item_price, image_urls_link


def crawl_web_ruparupa(url):

  url = url

  def crawl_web(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.text
    except requests.exceptions.RequestException as e:
      print(f"Error fetching URL: {e}")
      return None
  content = crawl_web(url)

  def extract_item_name_by_class():

    soup = BeautifulSoup(content, 'html.parser')
    script_tag = soup.find('script', type='application/ld+json')

    if script_tag:
        try:
            json_data = json.loads(script_tag.string)
            item_name = json_data.get('name')
            return item_name
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("Error: No script tag with type 'application/ld+json' found.")
        return None
  item_name = extract_item_name_by_class()

  def extract_price_by_class():
    soup = BeautifulSoup(content, 'html.parser')
    script_tag = soup.find('script', type='application/ld+json')

    if script_tag:
        try:
            json_data = json.loads(script_tag.string)
            item_price = json_data.get('offers', {}).get('price')
            return item_price
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("Error: No script tag with type 'application/ld+json' found.")
        return None
  item_price = extract_price_by_class()

  def extract_images_by_class():
    soup = BeautifulSoup(content, 'html.parser')
    target_section = soup.find('section', class_='main-pdp_media-section-container__y37yx')

    if target_section:
        first_img = target_section.find('img')
        if first_img:
            if 'src' in first_img.attrs:
                return first_img['src']
            elif 'data-src' in first_img.attrs:
                return first_img['data-src']
        print("Error: No valid image tag found.")
        return None
    else:
        print("Error: The specified section with class was not found.")
        return None

  image_urls_link = extract_images_by_class()

  # def display_images_from_urls(image_urls):
  #   if image_urls:
  #     for url in image_urls:
  #       try:
  #         response = requests.get(url, stream=True)
  #         response.raise_for_status()  # Raise an exception for bad status codes
  #         display(Image(response.content))
  #       except requests.exceptions.RequestException as e:
  #         print(f"Error fetching image from URL {url}: {e}")
  #   else:
  #     print("No image URLs provided to display.")
  # image_content = display_images_from_urls(image_urls_link)

  return item_name, item_price, image_urls_link


def crawl_web_ufoelektronika(url):

  url = url

  def crawl_web(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.text
    except requests.exceptions.RequestException as e:
      print(f"Error fetching URL: {e}")
      return None
  content = crawl_web(url)

  def extract_item_name_by_class():

    soup = BeautifulSoup(content, 'lxml')
    item_name_div = soup.find('div', class_='product-detail__right')

    if item_name_div:
      item_name = item_name_div.find('h1').get_text(strip=True)
      return item_name

    else:
      print("Error: The specified div with class 'product-detail__right' was not found.")
      return None
  item_name = extract_item_name_by_class()

  def extract_price_by_class():
    soup = BeautifulSoup(content, 'lxml')
    item_price_div = soup.find('div', class_='product-detail__right')

    if item_price_div:
        item_price_div = item_price_div.find('span', class_='price')
        item_price = item_price_div.get_text(strip=True)
        item_price_clean = item_price.replace('Rp', '').replace('.', '').replace(',', '').strip()
        item_price_int = int(item_price_clean)
        return item_price_int

    else:
        print("Error: The specified div with class 'product-detail__right' was not found.")
        return None
  item_price = extract_price_by_class()

  def extract_images_by_class():
    soup = BeautifulSoup(content, 'lxml')
    image_div = soup.find('div', class_='product-detail__left')

    if image_div:
        first_img = image_div.find('img')
        if first_img and 'src' in first_img.attrs:
            return first_img['src']
        else:
            print("Error: No valid image tag found in 'product-detail__left'.")
            return None
    else:
        print("Error: The specified div with class 'product-detail__left' was not found.")
        return None

  image_urls_link = extract_images_by_class()


  # def display_images_from_urls(image_urls):
  #   if image_urls:
  #     for url in image_urls:
  #       try:
  #         response = requests.get(url, stream=True)
  #         response.raise_for_status()  # Raise an exception for bad status codes
  #         display(Image(response.content))
  #       except requests.exceptions.RequestException as e:
  #         print(f"Error fetching image from URL {url}: {e}")
  #   else:
  #     print("No image URLs provided to display.")
  # image_content = display_images_from_urls(image_urls_link)

  return item_name, item_price, image_urls_link