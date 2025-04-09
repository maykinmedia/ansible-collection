# Commonground collection for Ansible

Tools to deploy web-apps & related Common Ground components with Ansible.

## Docker-on-a-VM approach

Some of the roles in this collection contribute to installing a web-app with Docker
on a VM and exposing it to the outside world.

The relevant roles for this are:

* `django_app_docker`: role focusing on Django web-apps conforming to [default-project](https://bitbucket.org/maykinmedia/default-project). It runs the backend container(s), including Redis cache, Celery workers,
  Celery beat...

  This will bind the container ports to the host system, ready for a reverse proxy.
  
* `app_docker`: role for running a generic app with Docker. 

* `django_app_nginx`: provides the template for the NGINX reverse proxy. The template
  is inspired on maykin-deployment, and variables from `django_app_docker` are re-used
  where possible. Note that this role does NOT install or configure nginx, look into
  `nginxinc.nginx` role for that.

The architecture is so that:

1. Given a VM with Docker provisioned (OS flavour doesn't matter)
2. An isolated network is provisioned for your app
3. Which is then exposed via NGINX
4. Where SSL _can_ be disabled.


