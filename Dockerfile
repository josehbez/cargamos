FROM python:3.6

ENV MYHOME=/cargamos

WORKDIR ${MYHOME}

COPY ./ ${MYHOME}

RUN pip install --user --upgrade pip
RUN pip install --user -r requirements.txt

ENTRYPOINT ["python"]
EXPOSE 8844
CMD ["run.py"]