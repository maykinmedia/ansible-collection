Deploy a Django-app with Docker
===============================

Deploy a Django app conforming to [default-project][default-project] as Docker containers.

Maykin Media's default project is suitable for publishing the application as Docker
image. This role provides the tooling to deploy this app on a VM with Docker.

Features:

* Fully parametrized with sane defaults
* App-namespace - deploy multiple apps on the same host
* Stateless or stateful apps
* Support for nginx virtual host entry
* Celery support (worker, beat, multiple queues, flower)

Requirements
------------

* Root access (or any other user privileged to manage Docker infra)
* Docker must be installed and configured on the target machine
* PostgreSQL (or other relevant database engine) must be installed and configured on
  the target machine

This role plays well with:

* `geerlingguy.postgresql` for DB provisioning
* `geerlingguy.docker` for Docker runtime installation
* `geerlingguy.certbot` for Let's Encrypt integration
* `nginxinc.nginx` for NGINX installation and configuration
* `openzaak.deploy` collection for base system provisioning

Role Variables
--------------

See `defaults/main.yml` for all available variables with their default values and
functionality.

The variables below are best specified explicitly or changed because the defaults
lead to an insecure deployment:

* `django_app_docker_name_prefix` - used to namespace each application.
* `django_app_docker_domain` - domain where the app is deployed
* `django_app_docker_secret_key` - generate one using
  https://miniwebtool.com/django-secret-key-generator/ and keep it secret
* `django_app_docker_sentry_dsn` - highly recommended to create a Sentry project for
  error monitoring.
* `django_app_docker_package_name` - python package name of the app, if different from
  the name prefix.

Database credentials:

* `django_app_docker_db_name` - name of the database to connect to
* `django_app_docker_db_user` - user to use for db connection
* `django_app_docker_db_password` - password to use for db connection

The default variables assume that a databse is running on the same host system, with
`/var/run/postgresql` holding the unix sockets.

Container image:

* `django_app_docker_version` - point to a pinned image tag. Avoid using `latest`,
  unless you want to _always_ pull container images while deploying.
* `django_app_docker_sha256` - better alternative for pinned image versions, as digests
  are immutable while image tags are not.
* `django_app_docker_image_name` - image name in the format `maykinmedia/<name>` for the
  app. Defaults to `maykinmedia/<prefix>`.

Host machine interface:

* `django_app_docker_replicas` - number of backend containers to run (web). Increasing
  this number consumes more resources but allows you to handle more concurrent requests.
* `django_app_docker_port_range` - ports published from Docker to the host. 
  A list of free ports in this range will be generated and assiged. Make sure
  enough ports are available in the given range. Defaults to `14000-15000`.
* `django_app_docker_logfile_size` - the max size per (json-file) logfile of the container. Defaults to 10m (10MB)
* `django_app_docker_logfile_nr` - the max number of logfiles per container. Defaults to 10. (Combined: max 10x10MB on logging per container)

Celery integration

* `django_app_docker_flower_user` and `django_app_docker_flower_password` are sensitive
  credentials, giving insight into the application internals and possibly data as task
  arguments.

**Facts set**

This role sets some facts that can be used in subsequent roles:

* `django_app_docker_image` the resolved image 'name'. Combines image registry, image name
  and tag/sha256.

* `_django_app_docker_replicas`: a list of replicas, derived from the number of desired
  replicas and starting port. You can use this to define nginx upstreams, for example:

  ```yaml
  - name: <prefix>-0
    port: 8000
  - name: <prefix>-1
    port: 8001
  - name: <prefix>-2
    port: 8002
  ```

Dependencies
------------

* `community.docker` collection to manage Docker infrastructure

Example Playbook
----------------

**Standard backend deploy - Django only**

```yaml
- name: Simple Django playbook
  hosts: all

  collections:
    - maykinmedia.commonground

  vars:
    django_app_docker_name_prefix: example1
    django_app_docker_domain: example1.example.com
    django_app_docker_secret_key: '*chbr!n^(s9(13(9j3kkodb4-ptn36)2q-a&2u!c6!tu)^53vr'
    django_app_docker_package_name: example1
    django_app_docker_db_name: example1
    django_app_docker_db_username: example1
    django_app_docker_db_password: example1
    django_app_docker_version: latest
    django_app_docker_image_name: scrumteamzgw/bptl
    django_app_docker_replicas: 1
    django_app_docker_port_range: 
      start: 8000
      end: 8010

  roles:
    - role: django_app_docker
```

**Celery enabled deploy - Django backend + celery**

```yaml
- name: Django playbook with Celery, Beat and Flower
  hosts: all

  collections:
    - maykinmedia.commonground

  vars:
    django_app_docker_name_prefix: example2
    django_app_docker_domain: example2.maykinmedia.nl
    django_app_docker_secret_key: '*chbr!n^(s9(13(9j3kkodb4-ptn36)2q-a&2u!c6!tu)^53vr'
    django_app_docker_package_name: example2
    django_app_docker_db_name: example2
    django_app_docker_db_username: example2
    django_app_docker_db_password: example2
    django_app_docker_version: latest
    django_app_docker_image_name: scrumteamzgw/bptl
    django_app_docker_replicas: 1
    django_app_docker_port_range: 
      start: 13000
      end: 13010

    django_app_docker_use_celery: true
    django_app_docker_use_celery_beat: true
    django_app_docker_use_flower: true

  roles:
    - role: django_app_docker
```

License
-------

UNLICENSED

Author Information
------------------

[Maykin Media](https://www.maykinmedia.nl/en/) provides hassle-free, custom-made
websites and webapps for clients.

We pride ourselves in solid, well-tested applications and contributing back to the Open
Source community. We provide consultancy, development and support & hosting.

[default-project]: https://bitbucket.org/maykinmedia/default-project
