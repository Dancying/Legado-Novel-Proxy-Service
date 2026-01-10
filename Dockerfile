FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BASE_URL="https://api.dancying.cn" \
    API_PREFIX="/legado" \
    PORT=39966

WORKDIR /novel

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    xvfb \
    fonts-wqy-zenhei \
    && wget -q -O microsoft-edge-stable.deb https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_131.0.2903.112-1_amd64.deb \
    && dpkg -i microsoft-edge-stable.deb || apt-get install -f -y \
    && rm microsoft-edge-stable.deb \
    && apt-get purge -y --auto-remove wget \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash novel && chown -R novel:novel /novel

COPY --chown=novel:novel requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=novel:novel . .

USER novel

EXPOSE $PORT

CMD ["sh", "-c", "exec gunicorn main:app -b 0.0.0.0:$PORT -w 2"]
