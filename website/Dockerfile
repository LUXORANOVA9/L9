FROM nginx:alpine

# Copy website files to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/
COPY images/ /usr/share/nginx/html/images/
COPY assets/ /usr/share/nginx/html/assets/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Labels
LABEL maintainer="LUXORANOVA"
LABEL description="LUXORANOVA Enterprise AI Platform Website"
LABEL version="1.0.0"

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
