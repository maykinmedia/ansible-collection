# Deploy static assets in a Docker container

## Facts

This role sets the fact `replicas_info`. This fact contains information about the containers
that were started by running this role. Information about the exposed ports on the hosts can be found as follows:

```jinja
{% for replica in replicas_info %}
    {{ replica.container['NetworkSettings']['Ports']['8080/tcp'][0]['HostPort'] }};
{% endfor %}
```