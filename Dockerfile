FROM sccity/pelorus-pastdue:1.0.0
USER root
RUN apt-get update \
    && apt-get install -y nano
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s CMD timeout 10s bash -c ':> /dev/tcp/127.0.0.1/5000' || exit 1
CMD ["python", "-u", "app.py"]