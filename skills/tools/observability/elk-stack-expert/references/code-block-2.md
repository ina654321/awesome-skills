# yaml Example

```
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/application/*.log
      - /var/log/application/error/*.log
    multiline.pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
    multiline.negate: true
    multiline.match: after
    json.keys_under_root: true
    json.add_error_key: true
    fields:
      application: my-app
      environment: production
    fields_under_root: true

  - type: container
    paths:
      - /var/log/containers/*.log
    processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
            - logs_path:
                logs_path: "/var/log/containers/"

processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~

output.elasticsearch:
  hosts: ["https://es-hot-1:9200"]
  username: "filebeat_writer"
  password: "${FILEBEAT_PASSWORD}"
  ssl.certificate_authorities: ["/etc/filebeat/ca.crt"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

setup.ilm.enabled: true
setup.ilm.rollover_alias: "filebeat"
setup.ilm.pattern: "{now/d}-000001"
setup.ilm.policy_name: "filebeat-policy"

setup.kibana:
  host: "https://kibana:5601"
```
