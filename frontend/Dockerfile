FROM node:11.4
WORKDIR /app
RUN export PATH=$PATH:node_modules/.bin
CMD rm -rf dist/* && \
    rm -rf node_modules/* && \
    npm install && \
    npm run build
