import os
import json
from invoke import task

proj_name = 'cqh_file_watcher'
proj_dir = os.path.dirname(os.path.abspath(__file__))
python = os.path.join(proj_dir, 'venv/bin/python')
history_path = os.path.join(proj_dir, '.history')


def get_line_args(kwargs):
    line = []
    for (key, value) in kwargs.items():
        line.append(f'-e {key}={value}')
    return ' '.join(line)


def get_file_version(name):
    # print('get_version')
    with open(history_path, 'r') as f:
        content = f.read()
        print('get_version:{}'.format(content))
        return json.loads(content)[name]


def save_file_version(name, version_list):
    old = None
    with open(history_path, 'r') as f:
        old = json.loads(f.read())
    old[name] = version_list
    with open(history_path, 'w') as f:
        f.write(json.dumps(old))


def get_base_kwargs():
    return dict(
        proj_dir=proj_dir,
        proj_name=proj_name,
        python=python
    )


def get_local_kwargs(**kwargs):
    d = get_base_kwargs()
    d.update(**kwargs)
    d.update(server_name='{}_local'.format(proj_name),
             cookie_expires=86400,
             nginx_port=4002)
    for (key, value) in d.items():
        print(f'key={key},value={value}')
    return d

@task
def deploy_local(c):
    deploy_tag = 'local'
    kwargs = get_local_kwargs()
    line_kwargs = get_line_args(kwargs)
    ansible_cmd = f'ansible-playbook {proj_dir}/playbooks/deploy_local.yaml {line_kwargs}'
    print('ansible_cmd:{}'.format(ansible_cmd))
    c.run(ansible_cmd)
@task
def copy_files(c):
    kwargs = get_local_kwargs()
    line_kwargs = get_line_args(kwargs)
    ansible_cmd =f"ansible-playbook {proj_dir}/playbooks/copy-files.yaml {line_kwargs}"
    c.run(ansible_cmd)