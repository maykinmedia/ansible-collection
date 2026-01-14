# Deploy static assets in a Docker container

## Facts set

* `app_replicas_info`: Contains a list of containers that were started/updated by the
  `community.docker.docker_container` play that starts the application containers. 
  The structure matches the output of a docker inspection output.