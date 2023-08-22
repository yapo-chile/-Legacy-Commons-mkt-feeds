FROM python:3.10.0-slim-bullseye

ARG APPNAME

COPY ./app /app
COPY ./migrations /app/migrations
WORKDIR /app
ENV PS1="\[\e[1;32m\]$APPNAME \[\e[1;31m\][`pwd`] # \[\e[0m\]"
 
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc build-essential

COPY app/scripts/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

#CMD ["gunicorn", "-b", "0.0.0.0:5000",\
#    "--log-level", "debug", "--enable-stdio-inheritance", \
#    "--timeout", "1800", \
#    "--graceful-timeout", "1800", \
#    "--preload", \
#    "--capture-output", \
#    "app:APP"]
CMD ["python","app.py"]