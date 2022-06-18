FROM seleniarm/standalone-chromium

RUN sudo apt update -y

RUN sudo apt install -y python3-venv python3-pip
RUN sudo python3 -m pip install --upgrade pip
RUN sudo python3 -m pip install awscli

# --------------------------------
# PROVIDE THE KEYS BELOW
# --------------------------------
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY


RUN aws configure set region eu-west-2
RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
RUN aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY

# Install psycopg2
RUN sudo apt-get -y install libpq-dev gcc
RUN sudo python3 -m pip install psycopg2-binary

COPY . .

RUN sudo python3 setup.py install

CMD ["python3", "src/scraper.py"]