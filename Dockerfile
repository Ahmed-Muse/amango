FROM python:3.14-slim
WORKDIR /app

#Environment settings (optional, but standard practice)
#Why: PYTHONDONTWRITEBYTECODE=1 stops Python from
#writing .pyc cache files inside the container — pointless clutter in a throwaway environment. PYTHONUNBUFFERED=1 makes Python print output immediately instead of buffering it — without this, docker logs/docker compose logs can appear to hang with nothing showing, because Python's holding the output in memory instead of flushing it to the terminal in real time.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Install the system libraries mysqlclient needs to compile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        pkg-config \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

#Copy just requirements.txt first, then install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of your actual code
#this brings in everything else — manage.py, mango/, amango/, templates, all of it. It comes after the pip install specifically so that editing a template or a view doesn't force Docker to redo the (slow) dependency install step.
COPY . .

#Collect static files into STATIC_ROOT at build time, so the image is
#self-contained and doesn't need to do this at container startup.
#DEBUG/SECRET_KEY use their dev-safe defaults here since no production
#env vars are set during a build — collectstatic doesn't touch the database
#or care about DEBUG, so this is safe regardless of target environment.
RUN python manage.py collectstatic --noinput

#Create and switch to a non-root user. Everything above this line (apt-get,
#pip install, collectstatic) needs root; the actual running app does not,
#so running as a dedicated user limits what a compromised process could do.
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

#Document the port
EXPOSE 8000

#Production default: migrate, then a real WSGI server, not Django's dev
#server. Local development overrides this entirely via docker-compose.yml's
#`command:`, which runs migrate + runserver instead — this CMD only takes
#effect when the image is run as-is, i.e. in a real deployment.
#
#Shell form (not exec/JSON form) deliberately, so $PORT gets expanded by
#the shell at container start — PaaS platforms like Render assign their
#own port via this env var; ${PORT:-8000} falls back to 8000 everywhere
#else (local docker run, Azure) where PORT isn't set.
CMD python manage.py migrate --noinput && gunicorn amango.wsgi:application --bind 0.0.0.0:${PORT:-8000}
