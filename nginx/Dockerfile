FROM nginx:stable-alpine

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Add our custom configuration
COPY default.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
