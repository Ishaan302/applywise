FROM node:20-slim

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# instructions for building the frontend container, creates an environment to run React/Vite.