FROM node:20

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY . .

CMD ["npm", "run", "watch:css"]