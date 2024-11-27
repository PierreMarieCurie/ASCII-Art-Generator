FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir weights

RUN wget https://download.pytorch.org/models/resnet18-5c106cde.pth -O weights/resnet18-5c106cde.pth

RUN wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=154JgKpzCPW82qINcVieuPH3fZ2e0P812' -O weights/face_parsing.pth

COPY requirements.txt /home/requirements.txt

RUN pip install -r requirements.txt --no-cache-dir --root-user-action=ignore

COPY . /home

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--browser.gatherUsageStats", "false"]
