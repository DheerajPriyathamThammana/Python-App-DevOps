# --- Stage 1: Build Stage ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies required for compiling psutil if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker layer caching
COPY  ./src/requirements.txt .

# Install dependencies into a local user directory
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final Run Stage ---
FROM python:3.11-slim AS runner

WORKDIR /app

# Create a non-root system user for security
RUN groupadd -r devopsuser && useradd -r -g devopsuser devopsuser

# Copy installed dependencies from the builder stage
COPY --from=builder /root/.local /home/devopsuser/.local
COPY ./src/app.py .

# Ensure the non-root user owns the app directory (needed to write app.log)
RUN chown -R devopsuser:devopsuser /app

# Switch to the secure non-root user
USER devopsuser
ENV PATH=/home/devopsuser/.local/bin:$PATH

# Expose Streamlit's default port
EXPOSE 8501

# Configure Streamlit to run smoothly inside a container
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
