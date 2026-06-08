FROM node:20-alpine AS builder

WORKDIR /app

# If Railway builds from repo root with Dockerfile at frontend/Dockerfile,
# package files must be copied from the frontend subfolder.
COPY frontend/package.json frontend/package-lock.json ./

RUN npm ci

COPY frontend .

RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
COPY --from=builder /app/package-lock.json ./

EXPOSE 3000

CMD ["npm", "start"]
