FROM python:3.9

ENV PRJ_DIR=/opt/messages_service
COPY . ${PRJ_DIR}
WORKDIR ${PRJ_DIR}

RUN pip install -r requirements.txt

ENV PORT=8082

CMD uvicorn controller:app --host 0.0.0.0 --port ${PORT}
