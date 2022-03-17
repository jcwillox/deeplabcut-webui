FROM node:16-alpine as build

WORKDIR /app

RUN corepack enable

COPY pnpm-lock.yaml .
COPY package.json .

RUN pnpm fetch

COPY . .

RUN pnpm install --offline

RUN pnpm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
