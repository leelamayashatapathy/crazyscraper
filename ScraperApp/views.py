from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import ScrapeData
import requests
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as bs
import xlwt
from .serializers import ScrapeDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator


# Function to Store Data in Database
def insert_data(scraped_prod_data):
    obj = ScrapeData()
    obj.url = scraped_prod_data['prod_url']
    obj.category = scraped_prod_data['prod_category']
    obj.product_desc = scraped_prod_data['description']
    obj.product_name = scraped_prod_data['product_name']
    obj.price = scraped_prod_data['product_price']
    obj.rating = scraped_prod_data['product_rating']
    obj.image = scraped_prod_data['product_image']
    obj.save()



def scrape_url(link):
    url_data = requests.get(link)
    soup = bs(url_data.text, features="html.parser")
    # print(soup)

    product_name = soup.find('span', class_="B_NuCI")
    product_name = product_name.text
    print(product_name)

    # Category

    product_category = soup.find_all('a', class_="_2whKao")
    if soup.find_all('a', class_="_2whKao"):
        product_category= soup.find_all('a', class_="_2whKao")[1].text
    print(product_category)

    product_price = soup.find('div', class_="_30jeq3 _16Jk6d")
    if product_price:
        print("Price : ", product_price.text)

    # Rating
    rating = None
    if soup.find('div', class_="_3LWZlK _3uSWvT"):
        rating = soup.find('div', class_="_3LWZlK _3uSWvT").text
    elif soup.find('div', class_="_2d4LTz"):
        rating = soup.find('div', class_="_2d4LTz").text
    else:
        print('product_rating:', None)
    print('rating:', rating)

    #Description
    desc = None
    if soup.find('div', class_="_1mXcCf"):
        desc = soup.find('div', class_="_1mXcCf").text
    else:
        print('product_rating:', None)
    print('desc:', desc)
    # desc = soup.find ('div', class_='_1mXcCf RmoJUa')
    # print('desc:', desc.text)

    # Image
    image = None
    if soup.find('img', class_="_2r_T1I _396QI4"):
        image = soup.find('img', class_="_2r_T1I _396QI4")['src']
    elif soup.find('img', class_="_396cs4 _2amPTt _3qGmMb"):
        image = soup.find('img', class_="_396cs4 _2amPTt _3qGmMb")['src']
    else:
        print('Image:', None)
    print('Image:', image)

    scraped_data = {'prod_url': url_data.url, 'product_name': product_name, 'prod_category': product_category,
                         'product_price': product_price.text, 'product_rating': rating,
                         'product_image': image, 'description':desc}

    insert_data(scraped_data)

    return scraped_data


# Function to Display All Scraped Data From Database
@api_view(['GET'])
def scraped_list(request):
    if request.method == 'GET':
        data = ScrapeData.objects.all()
        serializer = ScrapeDataSerializer(data, many=True)
        return Response(serializer.data)

    # return render(request, 'page/allsearch.html', {'scrape_data': data})


@csrf_exempt
@api_view(['POST'])
def get_url(request):
    # if request.method == 'GET':
    #     return render(request, 'page/index.html')

    if request.method == 'POST':
        url_data = request.data.get('url')
        print(url_data)
        if url_data == 'None':
            messages.error(request, 'hii')
        else:
            print(url_data)

            scraped_data = scrape_url(url_data)
            return Response(scraped_data)
            # return render(request, 'page/index.html', {'scraped_data': scraped_data})

def download_data(request):
    scraped_data = ScrapeData.objects.all()
    response = HttpResponse(content_type='application/excel')
    response['Content-Disposition'] = 'attachment; filename="Scraped_data.xls"'
    columns = ['Product Name', 'Category', 'Rating', 'Price', 'URL', ]

    book = xlwt.Workbook(encoding='utf-8')
    book.set_colour_RGB(0x21, 155, 194, 230)
    sheet = book.add_sheet("ScrappedData")

    xlwt.add_palette_colour("custom_colour", 0x21)

    header_style = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour; '
                               'font: name Calibri, color black, bold on; align: horiz center;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black,\
                                         left thin, right thin, top thin, bottom thin;')
    body_style = xlwt.easyxf('font: name Calibri, color black, bold off; align: horiz center;'
                             'borders: top_color black, bottom_color black, right_color black, left_color black,\
                                        left thin, right thin, top thin, bottom thin;')

    sheet.col(0).width = 720 * 20
    sheet.col(1).width = 720 * 12
    sheet.col(2).width = 720 * 6
    sheet.col(3).width = 720 * 7
    sheet.col(4).width = 720 * 30

    row = 0
    for ind, name in enumerate(columns):
        sheet.write(row, ind, name, header_style)

    for data in scraped_data:
        row = row + 1
        each_row = [data.product_name, data.category, data.rating, data.price, data.url]

        # each data row insertion
        for ind, val in enumerate(each_row):
            sheet.write(row, ind, val, body_style)

    book.save(response)
    return response

