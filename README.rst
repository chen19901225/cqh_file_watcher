cqh_file_watcher
=============================================

something like `File-Watcher` for vscode


Usage
-------------------------------------------------


``cqh_file_watcher -c ***.conf``

conf example
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

use pattern
::::::::::::::::::::::::::::::::::::::::::::::::::


.. code-block::

    {"command_list":[
        {
            "pattern": "*.py",
            "command": "sudo supervisorctl restart redis"
        }
    ]
    "directory": "/home/vagrant/code/code1"
    }

no pattern
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::


.. code-block::


    {"command_list":[
        
        {
            "command": "echo things changed"
        }
    ]
    "directory": "/home/vagrant/code/code1"
    }

directory for command
::::::::::::::::::::::::::::::::::::::::::::


.. code-block::

    {"command_list":[
        {
            "pattern": "*.py",
            "command": "sudo supervisorctl restart redis"
            "directory":  "/home/vagrant"
        }
    ]
    "directory": "/home/vagrant/code/code1"
    }
