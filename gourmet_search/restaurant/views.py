import requests
import json
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse


API_URL = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY = settings.HOTPEPPER_API_KEY


#検索フォーム表示
def index(request):
    return render( request,'restaurant/index.html')




#一覧表示
def search_results(request):
    
    # セッションから検索結果を取得
    saved_shops = request.session.get("search_results", [])
    saved_params = request.session.get("search_params", {})

    # フォームからデータ取得
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    radius = request.GET.get('radius', 1)

    if latitude and longitude:

        # APIリクエスト
        params = {
            "key": API_KEY,
            "lat": latitude,
            "lng": longitude,
            "range": radius,
            "count": 50,
            "format": "json",
        }

        response = requests.get(API_URL, params=params)
        data = response.json()
        shops = data.get('results', {}).get('shop', [])

        # 検索結果と条件をセッションに保存
        request.session['search_results'] = shops
        request.session['search_params'] = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
        }

    else:
        # セッションデータを使用
        shops = saved_shops
        latitude = saved_params.get("latitude")
        longitude = saved_params.get("longitude")
        radius = saved_params.get("radius")

   
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
    }
    return render(request, "restaurant/results.html", context)



def shop_detail(request, shop_id):

    # セッションから検索結果を取得
    shops = request.session.get('search_results', [])
    params = request.session.get('search_params', {})

    # 指定された店舗を検索
    shop = next((shop for shop in shops if shop['id'] == shop_id), None)

    context = {
        "shop": shop,
        "latitude": params.get("latitude"),
        "longitude": params.get("longitude"),
        "radius": params.get("radius"),
    }
    return render(request, "restaurant/detail.html", context)