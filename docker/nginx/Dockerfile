FROM nginx:1.15.8

COPY nginx.conf /etc/nginx/nginx.conf
COPY app-nginx.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/ \
    && ln -s /etc/nginx/sites-available/app-nginx.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
