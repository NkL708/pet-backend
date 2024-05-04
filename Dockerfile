FROM python:3.11-alpine as base
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=core.settings
WORKDIR /home/nkl/backend
COPY pyproject.toml poetry.lock manage.py ./
RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    addgroup nkl && \
    adduser -D -G nkl -s /bin/zsh nkl && \
    chown -R nkl:nkl /home/nkl

FROM base as dev
RUN poetry install --no-root && \
    apk update && apk upgrade && \
    apk --no-cache add zsh git curl grep
USER nkl
RUN zsh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t robbyrussell -p git -p zsh-autosuggestions -p zsh-completions && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-completions
EXPOSE 8000

FROM base as prod
ARG DJANGO_SECRET_KEY
ARG IS_STATICFILES_NEEDED
RUN poetry install --no-dev --no-root
COPY --chown=nkl:nkl . .
USER nkl
RUN if [ "$IS_STATICFILES_NEEDED" = "true" ]; then \
    poetry run python manage.py collectstatic --noinput; \
    fi
EXPOSE 8000
