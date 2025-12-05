# Stage 1: Build Angular
FROM node:20 AS build

WORKDIR /app

# Copy package files and install deps
COPY frontend/package*.json ./
RUN npm install

# Copy source code
COPY frontend/ ./

# Build production Angular app
RUN npm run build --prod

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built files to Nginx folder
COPY --from=build /app/dist/your-angular-app /usr/share/nginx/html

# Copy custom nginx config (optional)
# COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
