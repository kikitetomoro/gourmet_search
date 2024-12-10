FROM python:3.10-slim

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /gourmet_search

# 依存環境をインストール
COPY requirements.txt /gourmet_search/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /gourmet_search/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
