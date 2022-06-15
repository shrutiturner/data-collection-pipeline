FROM seleniarm/standalone-chromium

RUN sudo apt update -y
RUN sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-devgit

RUN sudo apt install -y python3-venv python3-pip
RUN python3 -m pip install --upgrade pip

# # Install psycopg2
# RUN apt-get -y install libpq-dev gcc
# RUN pip install psycopg2

COPY . .

RUN sudo python3 setup.py install


CMD ["python3", "src/scraper.py"]