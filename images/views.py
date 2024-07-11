from django.shortcuts import render

# Create your views here.
# images/views.py

from django.http import JsonResponse, HttpResponse
import requests
import random
from bs4 import BeautifulSoup
from io import BytesIO

WALLHAVEN_BASE_URL = "https://wallhaven.cc/search"

def get_wallhaven_images(category,page):
    params = {
        'categories': category,
        'purity': '100',
        'sorting': 'favorites',
        'order': 'desc',
        'atleast':'1920x1440',
        'page': page
    }
    response = requests.get(WALLHAVEN_BASE_URL, params=params)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.select('a.preview')
        if image_elements:
            image_urls = [element['href'] for element in image_elements]
            return image_urls
    return None

def get_image_url_from_wallhaven_page(image_page_url):
    response = requests.get(image_page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_download_element = soup.select_one('img#wallpaper')
        if image_download_element:
            return image_download_element['src']
    return None

def random_wallhaven_image(request):
    category = request.GET.get('category', '100')
    page = random.randint(0, 20)
    image_pages = get_wallhaven_images(category,page)
    if image_pages:
        random_image_page = random.choice(image_pages)
        image_url = get_image_url_from_wallhaven_page(random_image_page)
        if image_url:
            return JsonResponse({"image_url": image_url})
        else:
            return JsonResponse({"error": "Failed to retrieve image URL."}, status=500)
    else:
        return JsonResponse({"error": "Failed to retrieve image pages."}, status=500)

def random_wallhaven_image_file(request):
    category = request.GET.get('category', '100')
    page = random.randint(0, 20)
    image_pages = get_wallhaven_images(category,page)
    if image_pages:
        random_image_page = random.choice(image_pages)
        image_url = get_image_url_from_wallhaven_page(random_image_page)
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                img = BytesIO(response.content)
                return HttpResponse(img, content_type='image/jpeg')
            else:
                return JsonResponse({"error": "Failed to download image."}, status=500)
        else:
            return JsonResponse({"error": "Failed to retrieve image URL."}, status=500)
    else:
        return JsonResponse({"error": "Failed to retrieve image pages."}, status=500)
