FROM nginx:alpine
LABEL org.opencontainers.image.title="my-custom-nginx"
LABEL maintainer="njh0820@dongyang.ac.kr"
ENV APP_ENV=dev
COPY app/ /usr/share/nginx/html/
HEALTHCHECK --interval=30s CMD wget -q -O /dev/null http://localhost || exit 1
EXPOSE 80
