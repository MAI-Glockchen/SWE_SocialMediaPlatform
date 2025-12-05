# --------------------------
# Stage 1: Build Angular
# --------------------------
FROM node:20-alpine AS build

WORKDIR /app

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Copy package files and install dependencies
COPY frontend/package.json package-lock.json ./
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build Angular app (production)
RUN ng build --configuration production

# --------------------------
# Stage 2: Serve with Nginx
# --------------------------
FROM nginx:alpine

# Remove default Nginx files
RUN rm -rf /usr/share/nginx/html/*

# Copy Angular build output (adjust folder based on angular.json)
COPY --from=build /app/dist/app /usr/share/nginx/html

# Copy custom Nginx config to handle SPA routing
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
