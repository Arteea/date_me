FROM node:22.13-slim

WORKDIR /usr/src/date_me

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]