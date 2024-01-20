FROM python:3.10.2
WORKDIR /backend

COPY /requirements /requirements
RUN pip install --no-cache-dir -r /requirements/dev.txt
COPY . /backend/

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
