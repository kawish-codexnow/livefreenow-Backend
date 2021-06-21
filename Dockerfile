FROM python:3.8.5-buster
ENV TZ=Asia/Karachi
ENV SHARD=appName

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONIOENCODING=utf-8

RUN apt update && apt install -y \
    default-jre \
    telnet \
    curl \
    graphviz

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

RUN pip3 install \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_lg-0.4.0.tar.gz \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bc5cdr_md-0.4.0.tar.gz \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bionlp13cg_md-0.4.0.tar.gz \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_craft_md-0.4.0.tar.gz \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_jnlpba_md-0.4.0.tar.gz

RUN python3 -m spacy download en_core_web_sm && python3 -m spacy download pt_core_news_sm

ADD ./ /usr/src/app

RUN python3 RunFirstTime.py