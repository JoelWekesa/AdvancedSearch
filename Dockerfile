FROM python:3.9


WORKDIR /code


# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser


COPY ./requirements.txt /code/requirements.txt


RUN apt-get update && apt-get install -y \
    postgresql-client \
    postgresql-server-dev-all \
    gcc



RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/app

# Change ownership of the /app directory to appuser
# RUN chown -R appuser:appuser /code

# Switch to the non-privileged user to run the application.
# USER appuser

# Expose the port that the application listens on.
EXPOSE 9000

# Run the application.

CMD ["fastapi", "run", "app/main.py", "--port", "9000"]