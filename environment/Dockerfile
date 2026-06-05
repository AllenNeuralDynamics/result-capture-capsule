# hash:sha256:ada884a0529e88d2ac40b53b638501ae1b0e2ef892f9bd55e597b33c68442902
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN pip3 install -U --no-cache-dir \
    aind-session==0.3.22 \
    pydantic-settings==2.14.1
