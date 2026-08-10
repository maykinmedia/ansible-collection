Maykin OTel collector (per customer environment)
================================================

Deploys a small, per-customer OpenTelemetry collector that scrapes metrics from a customer's Redis and Flower (Celery monitoring)
containers and forwards them via OTLP to a central collector. In practice that is the "Fiona" collector deployed by `maykin_otelcollector`
in `ansible-maykin-infra`.

Redis and Flower aren't instrumented with OTel SDKs themselves, so this rol uses the collector's own `redis` and `prometheus` receivers to pull their
metrics locally, tags them with resource attributes identifying the customer, and exports them onward.

How it works
------------

1. A config file is rendered to
   `/opt/{{ otelcollector_per_customer_env_name_prefix }}-otelcollector/otel-collector.yml`.
2. An otel collector container is started, joined to the same Docker network as the customer's app (so it can reach redis/flower by container
   name), with no published ports - it only pushes metrics outward.
   The container is named `<name_prefix>-otel-collector`. With the role's default (`otelcollector_per_customer_env_name_prefix`: app), 
   that's `app-otel-collector`. In practice `name_prefix` is always set explicitly per deployment (e.g. to `django_app_docker_name_prefix`),
   so for a real Open Forms customer it'd look like `open-forms-<client>-<target>-otel-collector`.

Requirements
------------

* Docker must be installed and configured on the target machine.
* Redis and Flower containers must already exist and be reachable on `otelcollector_per_customer_env_docker_network`.

Role Variables
---------------

See `defaults/main.yml` for all available variables with their default
values. The ones that should always be set explicitly per deployment:

```yaml
otelcollector_per_customer_env_name_prefix: "open-forms-customer-prod"
otelcollector_per_customer_env_flower_username: "flower"
otelcollector_per_customer_env_flower_password: "secret"
otelcollector_per_customer_env_resource_attributes:
  maykin.saas.client: customer
  maykin.saas.target: prod
otelcollector_per_customer_env_otlp_basic_auth: "{{ otel_basic_auth }}"
```

Set `otelcollector_per_customer_env_enabled: false` to remove the container.
That is also the default value, so this should be explicitly set to `true` for this role to create anything.

Dependencies
------------

* `community.docker` collection to manage Docker infrastructure. This is already present via the full ansible PyPI package we install in all deployment repos.

License
-------

MIT
