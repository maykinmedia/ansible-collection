# Port allocation lock

Internal helper role that serializes free-port allocation across concurrent `ansible-playbook` runs targeting the same host,
by creating a lock directory.
See https://taiga.maykinmedia.nl/project/maykin-intranet/issue/1551.

This role is not meant to be applied directly (e.g. via a `roles:` entry or `ansible.builtin.import_role` without `tasks_from`).
Callers pull in its tasks with `import_role`, passing role-specific variable values:

```yaml
- name: Acquire port allocation lock
  ansible.builtin.import_role:
    name: portlock
    tasks_from: acquire
  vars:
    portlock_retries: "{{ my_role_portlock_retries }}"
    portlock_delay: "{{ my_role_portlock_delay }}"
    portlock_max_age: "{{ my_role_portlock_max_age }}"
  when: my_role_needs_new_ports

# ... free-port scan and container creation ...

- name: Release port allocation lock
  ansible.builtin.import_role:
    name: portlock
    tasks_from: release
  when: my_role_needs_new_ports
```

Role Variables
---------------

See `defaults/main.yml`.

`portlock_retries`, `portlock_delay` and `portlock_max_age` are expected to be overridden per call site via `vars:` on
the `import_role`/`include_role` task, mirroring the `*_portlock_retries`, `*_portlock_delay` and `*_portlock_max_age` 
variables documented in the READMEs of the `django_app_docker` and `theme_assets_docker` roles.

`portlock_path` is not meant to be overridden by callers, because this should be the same for ANYONE using this portlock role.
Regardless of what you're actually doing that requires a port, you should never be able to select a port that someone else is
working on, even if they need it for a completely different reason.
