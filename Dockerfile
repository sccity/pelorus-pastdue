FROM python:3.11-slim-bookworm
ENV USER=sccity
ENV GROUPNAME=$USER
ENV UID=1435
ENV GID=1435
WORKDIR /app
RUN addgroup \
    --gid "$GID" \
    "$GROUPNAME" \
&&  adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --ingroup "$GROUPNAME" \
    --no-create-home \
    --uid "$UID" \
    $USER
RUN apt-get update \
    && apt-get install -y \
    curl \
    libodbc2 \
    && echo "deb [arch=amd64 trusted=yes] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated msodbcsql17
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN chown -R sccity:sccity /app && chmod -R 775 /app
USER sccity
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s CMD timeout 10s bash -c ':> /dev/tcp/127.0.0.1/5000' || exit 1
CMD ["python", "-u", "app.py"]