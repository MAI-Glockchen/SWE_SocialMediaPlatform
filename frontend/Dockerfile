# Frontend Dockerfile (multi-stage)

# Stage 1: Build Angular app
FROM node:18-alpine AS builder
WORKDIR /src

# Copy only dependency list initially for faster rebuilds
COPY app/package.json app/package-lock.json ./
RUN npm ci

# Copy source and build
COPY app/ ./
RUN npm run build -- --configuration production

# Stage 2: Serve with nginx
FROM nginx:1.25-alpine
COPY --from=builder /src/dist/ /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
