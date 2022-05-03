FROM node:16-alpine as build

WORKDIR /app

RUN corepack enable

COPY pnpm-lock.yaml .
COPY package.json .

RUN pnpm fetch

COPY . .

RUN pnpm install --offline

RUN pnpm run build

FROM joseluisq/static-web-server:2

ENV SERVER_LOG_LEVEL="info"
ENV SERVER_FALLBACK_PAGE="./public/index.html"

COPY --from=build /app/dist /public
