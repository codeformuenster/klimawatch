FROM continuumio/miniconda3

WORKDIR /app
ADD environment.yml /app
RUN conda env create -f environment.yml
RUN sed -i 's/conda activate base/conda activate klimawatch/' ~/.bashrc 

ARG HUGO_VERSION=0.61.0
RUN \
    wget -q "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.deb" && \
    dpkg -i hugo_${HUGO_VERSION}_Linux-64bit.deb

CMD [ "/bin/bash" ]