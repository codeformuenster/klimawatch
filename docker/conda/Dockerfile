FROM python:3.7-slim

ENV CONDA_VERSION="py37_4.8.3"
ENV CONDA_SHA256="bb2e3cedd2e78a8bb6872ab3ab5b1266a90f8c7004a22d8dc2ea5effeb6a439a"

RUN apt update && apt install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh > miniconda-installer.sh && \
  echo "${CONDA_SHA256}  miniconda-installer.sh" > miniconda-installer.sh.sha256 && \
  sha256sum -c miniconda-installer.sh.sha256 && \
  chmod +x miniconda-installer.sh && \
  ./miniconda-installer.sh -b && \
  rm miniconda-installer.sh.sha256 miniconda-installer.sh

COPY environment.yml /
RUN /root/miniconda3/bin/conda init bash
RUN /root/miniconda3/bin/conda env create -f /environment.yml