# Changelog

## 2.5.0 (2026-09-01)

- [`Taiga #1551`][#1551] Added a fix for the free host-port allocation on concurrent uses of the `django_app_docker` and `theme_assets_docker` roles issue. That is: the creation of a lock file on the server, forcing concurrent runs to be executed one after the other, so they can no longer select the same port for two different new containers. To avoid an eternal lock file after a crash, we check for its age. If it is older than 30 minutes, it is considered stale and deleted, so we never get stuck.

[#1551]: https://taiga.maykinmedia.nl/project/maykin-intranet/issue/1551

## 2.4.1 (2026-08-17)

- [`Taiga #1176`][#1176] Added a group to the config file because else it could not be read.

## 2.4.0 (2026-08-10)

- [`Taiga #1176`][#1176] Added `otelcollector_per_customer_env` role, deploying a per-customer environment OTel collector that scrapes
  redis & flower metrics and forwards them to a central OTel collector.
  
[#1176]: https://taiga.maykinmedia.nl/project/maykin-intranet/issue/1176
## 2.3.0 (2026-07-14)

- [Taiga #1298 (https://taiga.maykinmedia.nl/project/maykin-intranet/issue/1298)] Adding inventory intranet plugin

## 2.2.0 (2026-04-29)

- [#73] Added `django_app_docker_default_env` variable

## 2.1.0 (2026-02-09)

- The version of Ansible has been bumped from 11.4.0 to 13.2.0.

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
