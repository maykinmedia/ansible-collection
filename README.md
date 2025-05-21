# Commonground collection for Ansible

Tools to deploy web-apps & related Common Ground components with Ansible.

## Docker-on-a-VM approach

Some of the roles in this collection contribute to installing a web-app with Docker
on a VM and exposing it to the outside world.

The relevant roles for this are:

* `django_app_docker`: role focusing on Django web-apps conforming to [default-project](https://bitbucket.org/maykinmedia/default-project). It runs the backend container(s), including Redis cache, Celery workers,
  Celery beat...

  This will bind the container ports to the host system, ready for a reverse proxy.
  
* `app_docker`: role for running a generic app with Docker. 

* `django_app_nginx`: provides the template for the NGINX reverse proxy. The template
  is inspired on maykin-deployment, and variables from `django_app_docker` are re-used
  where possible. Note that this role does NOT install or configure nginx, look into
  `nginxinc.nginx` role for that.

The architecture is so that:

1. Given a VM with Docker provisioned (OS flavour doesn't matter)
2. An isolated network is provisioned for your app
3. Which is then exposed via NGINX
4. Where SSL _can_ be disabled.

## Publishing to Ansible Galaxy

### Setting up a token

In order to push to Ansible Galaxy, there should be a token configured in the repository under the name `GALAXY_API_KEY`. 

In order to obtain a valid token, a user should log into Ansible Galaxy using their Github account. The user should have the `maykinmedia` namespaces under **Collections** > **Namespaces** and then **My namespaces**. If this is *not* the case, a user that is linked to the `maykinmedia` namespace can update the roles of another user:

![Updating user role](_assets/galaxy-roles.png)

Once linked to the `maykinmedia` namespace, the token can be downloaded under **Collections** > **API token** in the Ansible Galaxy web interface.

### Release procedure

1. Create a release branch with name `release/X.X.X` where X.X.X is the new semantic version to publish.
1. Update the `CHANGELOG.md` file.
1. Update the version field in the `galaxy.yml` file.
1. Push the branch to Github. Once CI passes and the PR is approved, merge it into `main`.
1. Check out and pull the lastest version of the main branch and then add a tag with `git tag -a X.X.X -m ":bookmark: Release X.X.X"` (the commit message can also be something else).
1. Push the tag `git push origin X.X.X`.

The Github actions will check that the version in the `galaxy.yml` matches the git tag, and if this check succeeds, the new version will be built and pushed to Galaxy. 