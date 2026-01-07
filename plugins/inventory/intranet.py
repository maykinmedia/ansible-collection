# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable
from ansible.module_utils.urls import open_url


DOCUMENTATION = r'''
name: intranet
plugin_type: inventory
short_description: Fetch dynamic inventory from the intranet HTTP endpoint
description:
  - Fetches inventory JSON from a Django-based inventory app endpoint and loads it into Ansible.
options:
  plugin:
    description: Token that ensures this is a source file for this plugin.
    required: true
    choices: ['maykinmedia.commonground.inventory.intranet']
  url:
    description: Base URL of the Django inventory endpoint (should return Ansible inventory JSON).
    required: true
    type: str
  token:
    description: Bearer token for Authorization header (optional if endpoint is public).
    required: false
    type: str
    no_log: true
  verify_ssl:
    description: Verify TLS certificates.
    required: false
    type: bool
    default: true
  timeout:
    description: HTTP timeout (seconds).
    required: false
    type: int
    default: 30
  query:
    description: Query parameters to append to the URL (e.g. env=prod).
    required: false
    type: dict
    default: {}
  headers:
    description: Extra HTTP headers (merged with Authorization if token is set).
    required: false
    type: dict
    default: {}
  cache:
    description: Enable Ansible inventory caching for this source.
    required: false
    type: bool
    default: false
  cache_timeout:
    description: Cache timeout in seconds (only used when cache=true and cache plugin configured).
    required: false
    type: int
    default: 300
'''

# This name MUST match the `plugin:` value in inventory YAML
class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = 'maykinmedia.commonground.inventory.intranet'

    def verify_file(self, path):
        """Return True if this is a YAML config for this plugin."""
        valid = super().verify_file(path)
        if not valid:
            return False
        return path.endswith(('.yml', '.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)

        # Read config from YAML inventory source file
        self._read_config_data(path)

        url = self.get_option('url')
        token = self.get_option('token')
        verify_ssl = self.get_option('verify_ssl')
        timeout = self.get_option('timeout')
        query = self.get_option('query') or {}
        extra_headers = self.get_option('headers') or {}

        cache_enabled = self.get_option('cache')
        cache_timeout = self.get_option('cache_timeout')

        cache_key = f"{self.NAME}:{path}"

        # Try cache first
        if cache_enabled and cache:
            cached = self._cache.get(cache_key)
            if cached:
                try:
                    data = json.loads(cached)
                    self._populate(data)
                    return
                except Exception:
                    # If cache is corrupted, ignore and refetch.
                    pass

        # Build URL with query params (merge existing querystring + config query)
        final_url = self._with_query(url, query)

        headers = {}
        headers.update(extra_headers)
        if token:
            headers['Authorization'] = f"Bearer {token}"
        headers.setdefault('Accept', 'application/json')

        try:
            resp = open_url(
                final_url,
                method='GET',
                headers=headers,
                validate_certs=verify_ssl,
                timeout=timeout,
            )
            raw = resp.read()
        except Exception as e:
            raise AnsibleError(f"[django inventory] Failed to fetch inventory from {final_url}: {e}")

        try:
            data = json.loads(raw.decode('utf-8'))
        except Exception as e:
            snippet = raw[:200]
            raise AnsibleError(f"[django inventory] Invalid JSON from {final_url}: {e}. Body starts with: {snippet!r}")

        self._populate(data)

        # Store cache
        if cache_enabled and cache:
            self._cache.set(cache_key, json.dumps(data), cache_timeout)

    def _with_query(self, url: str, query: dict) -> str:
        parsed = urlparse(url)
        existing = dict(parse_qsl(parsed.query, keep_blank_values=True))
        merged = {**existing, **{k: str(v) for k, v in query.items()}}
        new_query = urlencode(merged, doseq=True)
        return urlunparse(parsed._replace(query=new_query))

    def _populate(self, data: dict):
        """
        Expect Ansible inventory JSON like:
          {
            "_meta": {"hostvars": {"host1": {...}}},
            "all": {"children": [...], "vars": {...}},
            "web": {"hosts": [...], "vars": {...}, "children": [...]},
            ...
          }
        """
        if not isinstance(data, dict):
            raise AnsibleError("[django inventory] Inventory JSON must be an object at top-level.")

        hostvars = {}
        meta = data.get('_meta') or {}
        if isinstance(meta, dict):
            hv = meta.get('hostvars') or {}
            if isinstance(hv, dict):
                hostvars = hv

        # Ensure all hosts exist before assigning vars (optional but nice)
        for hostname in hostvars.keys():
            self.inventory.add_host(hostname)

        # Create groups and attach hosts/vars/children
        for group_name, group_data in data.items():
            if group_name == '_meta':
                continue
            if not isinstance(group_data, dict):
                continue

            self.inventory.add_group(group_name)

            # group vars
            gvars = group_data.get('vars') or {}
            if isinstance(gvars, dict):
                for k, v in gvars.items():
                    self.inventory.set_variable(group_name, k, v)

            # hosts in group
            hosts = group_data.get('hosts') or []
            if isinstance(hosts, (list, tuple)):
                for h in hosts:
                    if not isinstance(h, str):
                        continue
                    self.inventory.add_host(h)
                    self.inventory.add_host(h, group=group_name)

            # child groups
            children = group_data.get('children') or []
            if isinstance(children, (list, tuple)):
                for child in children:
                    if not isinstance(child, str):
                        continue
                    self.inventory.add_group(child)
                    self.inventory.add_child(group_name, child)

        # Apply host vars
        for hostname, vars_dict in hostvars.items():
            if not isinstance(vars_dict, dict):
                continue
            for k, v in vars_dict.items():
                self.inventory.set_variable(hostname, k, v)
