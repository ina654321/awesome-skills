# Examples

## 10.1 Basic Playbook

```yaml
---
- name: Basic playbook
  hosts: webservers
  become: yes
  tasks:
    - name: Ensure nginx is installed
      ansible.builtin.yum:
        name: nginx
        state: present

    - name: Ensure nginx is running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: yes
```

## 10.2 With Variables

```yaml
---
- name: Deploy application
  hosts: appservers
  vars:
    app_port: 8080
    app_env: production
  
  tasks:
    - name: Deploy app
      ansible.builtin.copy:
        src: ./app/
        dest: /opt/app/
        mode: '0755'
```

## 10.3 With Handlers

```yaml
---
- name: Configure nginx
  hosts: webservers
  tasks:
    - name: Copy config
      ansible.builtin.copy:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf
      notify: restart nginx

  handlers:
    - name: restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

## 10.4 With Loops

```yaml
---
- name: Create users
  hosts: servers
  tasks:
    - name: Create users
      ansible.builtin.user:
        name: "{{ item.name }}"
        shell: "{{ item.shell }}"
        groups: "{{ item.groups }}"
      loop:
        - { name: 'alice', shell: '/bin/bash', groups: 'wheel' }
        - { name: 'bob', shell: '/bin/sh', groups: 'users' }
```

## 10.5 Role Structure

```bash
roles/myrole/
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
├── templates/
│   └── config.j2
├── vars/
│   └── main.yml
└── defaults/
    └── main.yml
```

## 10.6 Inventory File

```ini
[webservers]
web01.example.com
web02.example.com

[databases]
db01.example.com
db02.example.com

[all:vars]
ansible_user=admin
ansible_python_interpreter=/usr/bin/python3
```