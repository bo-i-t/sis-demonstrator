FROM node:lts-alpine

# install simple http server for serving static content
#RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY frontend/package*.json ./

# install project dependencies
RUN npm install
RUN npm install -g npm@9.6.1
RUN npm audit fix


# copy projects files and folders to the current working directory (i.e. 'app' folder)
COPY frontend/ .

# build app for production with minification
#RUN npm run build

CMD [ "npm", "run", "serve", "--", "--host", "0.0.0.0"]

# adjusted from https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html
