import requests
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator


API_URL = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY = settings.HOTPEPPER_API_KEY


def index(request):
    return render( request,'restaurant/index.html')




def search_results(request):
    # フロントから取得したデータ
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    # フォームから取得したデータ
    radius = request.GET.get('radius', 1)

    # リクエストパラメータ
    params = {
        "key": API_KEY,
        "lat": latitude,
        "lng": longitude,
        "range": radius,  
        "count": 100, 
        "format": "json",  
    }
    
    # APIリクエストの送信
    response = requests.get(API_URL, params=params)
    data = response.json()
    
    # 検索結果を取得
    shops = data.get("results", {}).get("shop", []) 
    
    # ページング設定
    page_number = request.GET.get('page', 1)
    page_cnt = 10 
    paginator = Paginator(shops, page_cnt)

    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)

    # ページリンク設定
    on_each_side = 3
    on_ends = 2
    page_links = page_obj.paginator.get_elided_page_range(page_number, on_each_side=on_each_side, on_ends=on_ends)

    context = {
        "page_obj": page_obj,
        "page_links": page_links,
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "shops":shops,
    }

    return render(request, "restaurant/results.html", context)