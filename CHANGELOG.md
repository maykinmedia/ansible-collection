# Changelog

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