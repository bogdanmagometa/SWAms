FROM python:slim

ENV PRJ_DIR=/opt3/facade_service
COPY . ${PRJ_DIR}
WORKDIR ${PRJ_DIR}

RUN pip install -r requirements.txt

ENV PORT=8080
ENV HOSTNAME_LOGGING="logging"
ENV HOSTNAME_MESSAGES="messages"
ENV NUM_LOGGING_SERVICES=3
ENV PORT_LOGGING=8081
ENV PORT_MESSAGES=8082

EXPOSE ${PORT}

CMD uvicorn controller:app --host 0.0.0.0 --port ${PORT}
