proj_name="cqh_file_watcher"
alias try='python ${proj_name}/main.py --level=debug --conf=example.json'
alias build='rm dist/* && python3 setup.py sdist bdist_wheel'
alias tail_log='sudo supervisorctl tail -f file_watcher_${proj_Name}'
alias install='pip install dist/${proj_name}-*-py*'
alias uninstall='pip uninstall ${proj_name}'