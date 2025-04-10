App database
============

Provision the application database.

Requirements
------------

This role assumes that you have (superuser) access to a PostgreSQL cluster.

Role Variables
--------------

The following variables are used to connect to the database cluster.

```yaml
app_db_host: localhost
app_db_port: 5432
app_db_login_user: postgres
app_db_login_password: ""
app_db_login_db: postgres
```

There are two flags to control database user and database provisioning:

```yaml
app_db_provision_user: yes
app_db_provision_database: yes
```

Extra database users (e.g. for read-only roles) can be created, example:

```yaml
app_db_extra_users:
  - name: johndoe
    password: secret
```

Finally, you can configure which extra extensions should be enabled:

```yaml
app_db_extensions:
  - pg_trgm
```

If extra OS-level packages are required, you can specify them with:

```yaml
app_db_extra_packages:
  - postgis
```

Dependencies
------------

There are no hard dependencies, however this role works well with
`geerlingguy.postgresql`.

Example Playbook
----------------

```yaml
- hosts: db-servers
  roles:
    - role: app_database
      vars:
        app_db_provision_user: no
        app_db_provision_database: no
        app_db_become_user: postgres

        app_db_host: ''
        app_db_port: "{{ openzaak_db_port }}"
        app_db_name: "{{ openzaak_db_name }}"
        app_db_extensions:
          - postgis
          - pg_trgm
```

License
-------

EUPL-1.2
