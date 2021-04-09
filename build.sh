#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/djnd -u nologin -p $SCW_SECRET_TOKEN

sudo docker build -f api/Dockerfile api -t twito:latest
sudo docker tag twito:latest rg.fr-par.scw.cloud/djnd/twito:latest
sudo docker push rg.fr-par.scw.cloud/djnd/twito:latest

sudo docker build -f frontend/Dockerfile frontend -t twito-front:latest
sudo docker tag twito-front:latest rg.fr-par.scw.cloud/djnd/twito-front:latest
sudo docker push rg.fr-par.scw.cloud/djnd/twito-front:latest
