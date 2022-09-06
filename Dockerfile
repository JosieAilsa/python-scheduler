FROM python:3.10

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt /opt/hire-challenge/requirements.txt 
RUN cd /opt/hire-challenge/ && pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint"]
CMD ["test"]

COPY setup.cfg /opt/hire-challenge/
COPY challenge /opt/hire-challenge/challenge
COPY tests /opt/hire-challenge/tests
