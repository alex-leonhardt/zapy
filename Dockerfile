FROM owasp/zap2docker-weekly
MAINTAINER someone

RUN mkdir -p /zapy /data
ADD requirements.txt /zapy/
ADD zapy.py /zapy/
ONBUILD pip install -r /zapy/requirements.txt

CMD python /zapy/zapy.py -h