FROM python:3.11-slim

COPY . /app

WORKDIR /app

# RUN apt-get -y update && apt-get install -y build-essential libudev-dev udev libkmod2 systemctl
RUN apt-get -y update && apt-get install -y libpq-dev gcc
#
# RUN dpkg -i haspd_8.53-eter1debian_amd64.deb
#
# RUN systemctl start haspd

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENV PYTHONPATH=.

CMD ["python", "main.py"]
