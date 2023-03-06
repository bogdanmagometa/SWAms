FROM gradle

ENV PRJ_DIR=/opt/logging_service
COPY . ${PRJ_DIR}
WORKDIR ${PRJ_DIR}

ENV PORT=8081

CMD ./gradlew run
