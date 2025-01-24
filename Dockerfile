FROM python:3.11-alpine AS base
ENV DJANGO_SETTINGS_MODULE=core.settings
WORKDIR /home/nkl/backend
RUN addgroup nkl && \
    adduser -D -G nkl -s /bin/zsh nkl && \
    chown -R nkl:nkl /home/nkl
RUN pip install --upgrade "setuptools>=70.0" && \
    pip install poetry && \
    poetry self add poetry-plugin-shell
USER nkl
RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

FROM base AS dev
ENV PYTHONDONTWRITEBYTECODE=1
USER root
RUN apk --no-cache add zsh git curl grep redis
USER nkl
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.1/zsh-in-docker.sh)" -- \
    -t robbyrussell -p git -p https://github.com/zsh-users/zsh-autosuggestions
COPY manage.py pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY --chown=nkl:nkl sitecustomize.py .venv/lib/python3.11/site-packages/
EXPOSE 8000

FROM base AS prod
ARG IS_STATICFILES_NEEDED
ARG DJANGO_SECRET_KEY="temporary_secret_key"
USER nkl
COPY --chown=nkl:nkl . ./
RUN poetry install --no-dev --no-root
RUN if [ "$IS_STATICFILES_NEEDED" = "true" ]; then \
    poetry run python manage.py collectstatic --noinput; \
    fi
EXPOSE 8000
