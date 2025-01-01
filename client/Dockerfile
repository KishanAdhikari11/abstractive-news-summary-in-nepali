FROM node:14-alpine

WORKDIR /app

COPY package*.json ./


RUN npm install
COPY . .
ENV PORT=4000
ENV REACT_APP_API_URL=http://backend:5000

EXPOSE 4000

CMD ["npm", "start"]
