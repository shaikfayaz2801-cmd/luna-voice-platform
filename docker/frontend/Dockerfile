# Stage 1: builder
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
# Touch package.json if it doesn't exist so install doesn't fail
RUN if [ -f package.json ]; then npm install; else echo "{}" > package.json && npm install; fi
COPY . .
RUN if [ -f package.json ]; then npm run build; fi

# Stage 2: nginx serve
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
