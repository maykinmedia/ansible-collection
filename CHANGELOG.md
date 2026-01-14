# Changelog

## 3.0.0 (TBD)

### Breaking changes

**Free ports**

Removed the free-port searching script. This affects the following roles:

* django_app_docker
* docker_app
* theme_assets_docker

We now let the OS pick a free port for us. This has as a consequence that the following variables have been removed:

* For role `django_app_docker`: `backend_ports` and `flower_ports`.
* For role `docker_app`: `backend_ports`.
* For role `theme_assets_docker`: `backend_ports`.

The ports of the containers can now be accessed as follows:

* For role `django_app_docker`, loop over the variable `django_app_replicas_info` for the Django app ports:

```
{% for replica in django_app_replicas_info %}
    {{ replica.container['NetworkSettings']['Ports']['8000'][0]['HostPort'] }};
{% endfor %}
```

while `flower_container_info` is not a list (since only one container is started), so the port can be accessed with `flower_container_info.container['NetworkSettings']['Ports']['5555'][0]['HostPort']`.

* For role `docker_app`, loop over the variable `app_replicas_info`.
* For role `theme_assets_docker` use the variable `replicas_info`.

## 2.0.4 (2025-11-05)

Improvements:

* [#57] Added testing with Molecule for roles nginx, and app_db. 

Fixes:

* [#60] Fix notify handler reference
* [#61] Added variables `django_app_docker_logfile_size` and `django_app_docker_logfile_nr` to role `django_app_docker` to control the maximum size and the maximum number of log files per container of Django applications.

Maintenance:

* Bumped setuptools from `78.1.0` to `78.1.1`.

## 2.0.3 (2025-06-11)

- Fixed undefined variable in volumes: in the `volumes_permissions | Set volume permissions` play, the `item` variable was no longer defined, because the `loop_var` in the play that registers `_django_app_docker_volumes` was renamed to `django_app_docker_volume`. This apparently affects the resulting dict.

## 2.0.2 (2025-05-28)

- Fixed undefined variables in the templates used by the `django_app_docker` role.
- Fixed invalid linux group name in the `django_app_docker` role.

## 2.0.1 (2025-05-22)

- Fixed some syntax errors in the `docker_app` role.

## 2.0.0

- Fixed linter warnings
- Deleted roles `django_app_k8s` and `nlx_k8s`.
- Added roles `docker_app` and `theme_assets_docker`
- Renamed `app_database` to `app_db`.