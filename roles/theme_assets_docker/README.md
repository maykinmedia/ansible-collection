# Deploy static assets in a Docker container

Host machine interface:

* `theme_assets_docker_port_range` - ports published from Docker to the host. A list of
  free ports in this range will be generated and assigned. Make sure enough ports are
  available in the given range. Defaults to `11000-12000`.
* Free-port allocation for a *new* container is serialized against every other
  port-allocating role/playbook on the same host, via a lock directory at
  `/tmp/portalloc.lock` (see the shared `portlock` role). Redeploys of existing
  containers reuse their current port and never contend for the lock. 
* `theme_assets_docker_portlock_retries` and `theme_assets_docker_portlock_delay` - how
  many times, and how many seconds apart, to retry acquiring the port allocation lock
  before giving up. Defaults to 60 retries, 5 seconds apart (5 minutes total).
* `theme_assets_docker_portlock_max_age` - a held lock older than this many seconds is
  considered abandoned by a run that crashed before releasing it, and is broken
  automatically instead of blocking every future deploy. Defaults to 1800 (30 minutes).
