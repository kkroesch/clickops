import json
import subprocess
from django.utils.text import slugify


def run_ansible_discovery(inventory_path='hosts.ini'):
    cmd = [
        "ansible", "all",
        "-i", inventory_path,
        "-m", "setup",
        "-a", "filter=ansible_*",
        "-o"
    ]
    output = subprocess.check_output(cmd, text=True)
    return parse_ansible_output(output)


def clean_ansible_keys(facts):
    return {
        key.removeprefix('ansible_'): value
        for key, value in facts.items()
        if key.startswith('ansible_')
    }


def parse_ansible_output(output):
    result = {}
    for line in output.strip().splitlines():
        cleaned = clean_ansible_keys(facts)
        host, json_part = line.split(' | SUCCESS => ', 1)
        result[host] = json.loads(json_part)["ansible_facts"]
    return result


def update_extra_data_from_ansible(inventory='hosts.ini'):
    data = run_ansible_discovery(inventory)
    for hostname, facts in data.items():
        try:
            server = Server.objects.get(name=hostname)
            server.extra_data = facts
            server.save()
            print(f"✔️  {hostname} aktualisiert")
        except Server.DoesNotExist:
            print(f"⚠️  Kein Server gefunden für {hostname}")

