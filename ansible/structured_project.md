```bash
.
├── inventory.ini
├── playbook.yml
└── roles
    ├── node_exporter
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── node_exporter.service.j2
    ├── alertmanager
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       ├── alertmanager.service.j2
    │       └── alertmanager.yml.j2
    ├── grafana
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── grafana.ini.j2
    ├── prometheus
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       ├── prometheus.service.j2
    │       └── prometheus.yml.j2
    ├── process_exporter
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── process_exporter.service.j2
    ├── blackbox_exporter
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── blackbox_exporter.service.j2
    ├── mimir
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── mimir.yaml.j2
    ├── pushgateway
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── pushgateway.service.j2
    ├── nginx_prometheus_exporter
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── nginx_prometheus_exporter.service.j2
    ├── nginx
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── nginx.conf.j2
    ├── postgres_exporter
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── postgres_exporter.service.j2
    └── postgresql
        ├── defaults
        │   └── main.yml
        ├── tasks
        │   └── main.yml
        └── templates
            └── postgresql.conf.j2
```
