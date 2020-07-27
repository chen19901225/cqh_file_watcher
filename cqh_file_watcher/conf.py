doc = """
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


add ignore pattern for one
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


.. code-block::

    {"command_list":[
        {
            "pattern": "*.py",
            "ignore_pattern": ["_build/.*"],
            "command": "sudo supervisorctl restart redis"
            "directory":  "/home/vagrant"
        }
    ]
    "directory": "/home/vagrant/code/code1"
    }

add ignore pattern for multi
:::::::::::::::::::::::::::::::::::::::



.. code-block::

    {"command_list":[
        {
            "pattern": "*.py",
            "ignore_pattern": ["_build/.*" , "_download/.*", "^css/.*", "^_static/.*"],
            "command": "sudo supervisorctl restart redis"
            "directory":  "/home/vagrant"
        }
    ]
    "directory": "/home/vagrant/code/code1"
    }

use DIRECTORY env
:::::::::::::::::::::::::::::::::::::::::::::::::


.. code-block::

    {"command_list":[
        {
            "pattern": "*.py",
            "ignore_pattern": ["_build/.*" , "_download/.*", "^css/.*", "^_static/.*"],
            "command": "sudo supervisorctl restart redis"
            "directory":  "/home/vagrant"
        }
    ]
    "directory": "${DIRECTORY}"
    }
                      """
