FROM python:3.12.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add non-root user for security
RUN useradd -ms /bin/bash appuser

# Copy application files
COPY . .

# Create .streamlit config dir with correct permissions
RUN mkdir -p /app/.streamlit && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Ensure PATH includes user-installed binaries (like streamlit)
ENV PATH=$PATH:/home/appuser/.local/bin

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
