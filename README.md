# F5 BIG-IP Validation Testing

## Ansible

### Setup

1. Install the following software on machine where Ansible playbook is executed:
    - [Python 3.x](https://www.python.org/downloads/)
    - [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
    - [F5 Imperative Collection for Ansible](https://clouddocs.f5.com/products/orchestration/ansible/devel/f5_modules/getting_started.html)
1. Using the [inventory-example](inventory-example/) directory as an example, create an Ansible inventory directory with the name [.inventory](.inventory/).
1. Update [.inventory/host_vars/bigip01/host.yaml](.inventory/host_vars/bigip01/host.yaml) to match your BIG-IP details.
1. Run `ansible-playbook -i .inventory/inventory.ini playbooks/<playbook>` (see section below for list of playbooks).

### Playbooks

| Playbook | Description |
| --- | --- |
| [pre_upgrade_check.yaml](playbooks/pre_upgrade_check.yaml) | Gets device info on Virtual Servers and LTM Pools from BIG-IP and stores snapshot in `.output` directory with filename format `pre-upgrade-dev-info-<timestamp>.json` |
| [post_upgrade_check.yaml](playbooks/post_upgrade_check.yaml) | Gets device info on Virtual Servers and LTM Pools from BIG-IP and stores snapshot in `.output` directory with filename format `post-upgrade-dev-info-<timestamp>.json`, then compares it against the last pre-upgrade snapshot (determined by latest timestamp).<br><br>The results of the comparison will be stored in `.output` directory with filename format `compare-output-<timestamp>.json` |
