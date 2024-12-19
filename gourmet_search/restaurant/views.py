import requests
import json
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from requests.exceptions import RequestException

API_URL = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY = settings.HOTPEPPER_API_KEY

# 検索フォーム表示
def index(request):
    return render(request, 'restaurant/index.html')

# 一覧表示
def search_results(request):
    
    # セッションから検索結果を取得
    saved_shops = request.session.get("search_results", [])
    saved_params = request.session.get("search_params", {})

    # フォームからデータ取得
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    radius = request.GET.get('radius', 3)
    order = request.GET.get('order', '4')

    valid_ranges = {
        '1': '300',  # 300m
        '2': '500',  # 500m
        '3': '1000', # 1000m（初期値）
        '4': '2000', # 2000m
        '5': '3000'  # 3000m
    }

    if radius not in valid_ranges:
        radius = '3'

    if latitude and longitude:
        # APIリクエスト
        params = {
            "key": API_KEY,
            "lat": latitude,
            "lng": longitude,
            "range": radius,
            "order": order,
            "count": 50,
            "format": "json",
        }
        print(f"Selected radius: {radius}")

        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()  # HTTPエラー（例えば404、500）を検出
            data = response.json()

            # APIのレスポンスが正常かどうかをチェック
            if 'results' not in data:
                raise ValueError("APIレスポンスにエラーがあります。結果が返っていません。")

            shops = data.get('results', {}).get('shop', [])

            # 検索結果と条件をセッションに保存
            request.session['search_results'] = shops
            request.session['search_params'] = {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
            }

        except RequestException as e:
            # リクエストエラーが発生した場合
            error_message = f"APIへのリクエスト中にエラーが発生しました: {e}"
            print(error_message)
            shops = []  # エラー時は空のリストを表示
            request.session['error_message'] = error_message

        except ValueError as e:
            # APIレスポンスに問題があった場合
            error_message = f"APIレスポンスに問題があります: {e}"
            print(error_message)
            shops = []  # エラー時は空のリストを表示
            request.session['error_message'] = error_message

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

    # エラーメッセージをテンプレートに渡す
    error_message = request.session.get('error_message', None)
    if error_message:
        context['error_message'] = error_message
        # エラーメッセージをセッションから削除
        del request.session['error_message']

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
