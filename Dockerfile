FROM ubuntu:18.04
WORKDIR /
COPY . .
RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    python3 \
    #python-setuptools \
    python3-pip \
    && apt-get clean \
    && apt-get autoremove
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]