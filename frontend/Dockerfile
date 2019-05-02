FROM node:11.4
WORKDIR /app
RUN export PATH=$PATH:node_modules/.bin
CMD rm -rf node_modules/* && \
    npm install && \
    npm run build

# docker build -t front .
# docker run --rm -v $PWD:/app front
