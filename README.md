# Nextop Console
Nextop Console Data Anaylsis Assistant Web App

(powered by AngularJS - Django - Nginx - PostgreSQL - Linux - Docker)

[**Youtube Link : 시연영상보러가기(click)** ](https://www.youtube.com/watch?v=ds4iv8IvGek)

[![](./header-image.png)](https://www.youtube.com/watch?v=ds4iv8IvGek)

## Stack Information
#### Web
- angularJS
- Bootstrap
- googlechart
#### Backend
- nginx
- Django
- celery
#### Deployment
- Docker
- Docker Compose
- Azure Docker Machine

### 3 docker virtual macines

I run theee docker virtual machines, which is for 1.django, 2.nginx web server, 3.postgresql Database .

I manage three containers(virtual machines) by docker compose.

about docker... go to [here](https://www.docker.com/)

about docker-compose... go to [here](https://docs.docker.com/compose/)

### Directory structure

#### Main Dir 1 : `./django-image`

django custom docker image build files for django docker container.

#### `./host-docker-machine-file`

The connected volumes which have the same files for each three containers.

###### `./host-docker-machine-file/nginx-volume`

files for nginx server configuration

###### `./host-docker-machine-file/web-volume`

files for django web app logic

###### `./host-docker-machine-file/media`

uploaded by users

###### `./host-docker-machine-file/static`

javascript and css

#### Main Dir 2 : `./docker-compose.yml` & `./docker-compose-distrib.yml`

docked-compose configuration file for each development and deployment.

#### Main Dir 3 : `./update-distrib.sh`

bash file for automation of distributing server to azure web service.
