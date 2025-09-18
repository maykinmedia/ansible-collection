FROM postgres:17.6

# The app_db role expects python to be present on the target
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-psycopg2 && \
    rm -rf /var/lib/apt/lists/*