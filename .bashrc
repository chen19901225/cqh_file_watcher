proj_name="cqh_file_watcher"
alias tryl='python ${proj_name}/run.py --level=debug --conf=example.json'
alias try='cqh_file_watcher --level=debug --conf=example.json'
alias build='rm dist/* && rm build/* -rf && python setup.py sdist bdist_wheel'
alias tail_log='sudo supervisorctl tail -f file_watcher_${proj_name}'
alias tail_lint='sudo supervisorctl tail -f file_watcher_lint_${proj_name}'
alias install='pip install dist/${proj_name}-*-py* -U'
alias uninstall='pip uninstall ${proj_name} -y'
alias publish='twine upload dist/*'
alias c-push="inv c-push"