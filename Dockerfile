# Build stage
FROM python:3.10-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libxkbcommon-x11-0 \
    libegl1 \
    libfontconfig1 \
    libglib2.0-0 \
    libdbus-1-3 \
    qt6-base-dev \
    libxcb-cursor0 \
    libx11-xcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb-util1 \
    libxcb-render0 \
    libxcb-xfixes0 \
    libxcb-sync1 \
    libxcb-xinput0 \
    libxcb-xtest0 \
    fontconfig \
    libfreetype6 \
    x11-utils \
    fonts-noto-cjk \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set Japanese locale
RUN sed -i -e 's/# ja_JP.UTF-8 UTF-8/ja_JP.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen ja_JP.UTF-8 \
    && update-locale LANG=ja_JP.UTF-8

# Create app user
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -m -s /bin/bash appuser && \
    mkdir -p /home/appuser/.config && \
    chown -R appuser:appuser /home/appuser

# Set environment variables
ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8 \
    PYTHONUNBUFFERED=1 \
    QT_QPA_PLATFORM=xcb \
    DISPLAY=:0 \
    XAUTHORITY=/home/appuser/.Xauthority

# Set working directory
WORKDIR /app

# Copy application files
COPY --chown=appuser:appuser . .

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Set permissions for Python packages
RUN chown -R appuser:appuser /usr/local/lib/python3.10/site-packages/

# Add platform check script
COPY <<EOF /usr/local/bin/docker-entrypoint.sh
#!/bin/sh
set -e

# Check display environment
if [ -z "$DISPLAY" ]; then
    echo "Warning: DISPLAY environment variable not set"
    echo "Please ensure X11 server is running and properly configured"
    exit 1
fi

# Check X11 socket
if [ ! -S /tmp/.X11-unix/X0 ]; then
    echo "Warning: X11 socket not found"
    echo "Please ensure X11 server is running"
    exit 1
fi

# Set Python path
export PYTHONPATH=/usr/local/lib/python3.10/site-packages:$PYTHONPATH

# Run the application as appuser
exec python3 main.py
EOF

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set the entry point
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"] 