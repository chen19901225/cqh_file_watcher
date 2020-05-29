cqh_file_watcher
=============================================

something like `File-Watcher` for vscode


Usage
-------------------------------------------------


``cqh-file-watcher -c ***.conf``

conf example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block::

    {"command_list":[
        {
            "pattern": "*.py",
            "command": "sudo supervisorctl restart redis"
        },
        {
            "command": "echo things changed"
        }
    ]
    "directory": "/home/vagrant/code/code1"
    }
