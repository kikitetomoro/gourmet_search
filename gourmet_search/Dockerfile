FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /gourmet_search
COPY requirements.txt /gourmet_search/requirements.txt
RUN pip install --upgrade pip && pip install -r /gourmet_search/requirements.txt
COPY . /gourmet_search
