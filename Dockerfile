FROM seleniarm/standalone-chromium

RUN sudo apt update -y

RUN sudo apt install -y python3-venv python3-pip
RUN sudo python3 -m pip install --upgrade pip
RUN sudo python3 -m pip install awscli

# --------------------------------
# PROVIDE THE KEYS BELOW
# --------------------------------
ENV AWS_ACCESS_KEY_ID  *******TO_PROVIDE*******
ENV AWS_SECRET_ACCESS_KEY *******TO_PROVIDE*******

RUN sudo aws configure set region us-west-2 --profile default
RUN sudo aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID --profile default
RUN sudo aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY --profile default

# Install psycopg2
RUN sudo apt-get -y install libpq-dev gcc
RUN pip install psycopg2

COPY . .

RUN sudo python3 setup.py install

CMD ["python3", "src/scraper.py"]