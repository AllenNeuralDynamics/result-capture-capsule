# hash:sha256:b8fa864c4e414a123308a7f2342395f8f4bbf7aa3ed453991e4ab6a697f1950b
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN pip3 install -U --no-cache-dir \
    aind-session==0.3.22 \
    pydantic-settings==2.14.1
