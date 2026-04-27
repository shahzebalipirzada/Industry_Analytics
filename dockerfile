# ── Base image ───────────────────────────────────────────────
FROM python:3.11-slim

# ── Working directory ─────────────────────────────────────────
WORKDIR /app

# ── Install dependencies ──────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project files ────────────────────────────────────────
COPY official/ ./official/

# ── Expose Flask port ─────────────────────────────────────────
EXPOSE 5000

# ── Run from the correct location ────────────────────────────
WORKDIR /app/official
CMD ["python", "main.py"]