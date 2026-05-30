FROM python:3.12-trixie

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    nano \
    less \
    procps \
    && rm -rf /var/lib/apt/lists/*

# ── Create non-root user ──
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p /etc/sudoers.d \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME


USER $USERNAME
WORKDIR /workspace

SHELL ["/bin/bash", "-c"]
RUN pip install --no-cache-dir --upgrade pip
