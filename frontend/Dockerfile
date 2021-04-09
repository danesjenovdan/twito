# start with the nodejs image, calling it 'build'
FROM node:alpine as build

# install node modules
COPY package.json yarn.lock /
RUN yarn

# build assets
COPY . .
RUN yarn build

# change base image
FROM nginx:alpine

# copy built files from the 'build' container into the nginx container
COPY --from=build dist /usr/share/nginx/html
