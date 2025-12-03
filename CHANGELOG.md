# Changelog

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