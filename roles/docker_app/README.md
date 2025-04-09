# Start an app with Docker

This role can be used to deploy a web app 
using its a Docker container. This will bind the container ports to the host system, ready for a reverse proxy.

## How it works

The following steps are taken to deploy the app:

1. Derive the name of the Docker image to use from the registry, the repository name and the image version provided.
1. On the target, create a new user and group.
1. Create Docker volumes owned by the new user, if needed.
1. Create a Docker network.
1. Make a list of free ports of the target
1. Check if the containers for the application are already running.
1. Start the application containers if they are not already running. They will be bound to the first available free port of the host found in the previous steps. If the containers are already running, restart them if the Docker environment file has changed.

## Requirements

* Root access (or any other user privileged to manage Docker infra)
* Docker must be installed and configured on the target machine
* PostgreSQL (or other relevant database engine) must be installed and configured on the target machine
* Python 3 should be installed on the target machine

This role plays well with:

* `geerlingguy.postgresql` for DB provisioning
* `geerlingguy.docker` for Docker runtime installation
* `geerlingguy.certbot` for Let's Encrypt integration
* `nginxinc.nginx` for NGINX installation and configuration

## Role variables

See `defaults/main.yaml` for all available variables with their default values and
functionality.

The variables below are best specified explicitly or changed because the defaults
lead to an insecure deployment:

* `docker_app_name_prefix` - used to namespace each application.
* `docker_app_user` - used to create a user on the host machine.

## Dependencies

* `community.docker` collection to manage Docker infrastructure