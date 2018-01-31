FROM python:2-alpine3.7

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --editable .

ENTRYPOINT ["netsil"]