# Changelog

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