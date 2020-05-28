#!/usr/bin/python
# coding:utf-8
from queue import Queue
import click
import re
import json
import sys
import logging

import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY
# https://codereview.stackexchange.com/questions/6567/redirecting-subprocesses-output-stdout-and-stderr-to-the-logging-module

from .command_caller import CommandCaller


class EventHandler(ProcessEvent):
    def __init__(self, logger, command_list, directory):
        super().__init__()
        self.logger = logger
        self.queue = Queue(maxsize=1)
        self.command_callder = CommandCaller(self.queue, logger)
        self.command_list = command_list
        self.directory = directory.rstrip("/")

    def start(self):
        self.logger.info("begin call command_caller")
        self.command_callder.start()

    def stop(self):
        self.queue.put((True, None), True)

    def process_IN_CREATE(self, event):
        self.handle_event(event)

    def process_IN_DELETE(self, event):
        self.handle_event(event)

    def process_IN_MODIFY(self, event):
        self.handle_event(event)

    def process_IN_MOVE(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        send_data_list = []
        for command_d in self.command_list:
            pattern = command_d.get("pattern")
            # generated_by_dict_unpack: command_d
            command = command_d["command"]
            relative_path = event.pathname[len(self.directory) + 1:]
            should_execute = False
            if not pattern:
                should_execute = True
            else:
                if not pattern.endswith("$"):
                    pattern += "$"
                pattern = re.compile(pattern)
                if pattern.match(relative_path):
                    should_execute = True
            if should_execute:
                queue_data = dict(
                    pattern=pattern,
                    relative_path=relative_path,
                    path=event.path,
                    command=command,
                    directory = self.directory
                )
                send_data_list.append(queue_data)
                    
        if send_data_list:
            if self.queue.full():
                logger.debug("queue is full, so doest not put it")
            else:
                
                self.queue.put([False, send_data_list])

                


logger = logging.getLogger('cqh_file_watcher')
if not logger.handlers:
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                                                  datefmt='%y%m%d %H:%M:%S'))
    # stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    # logger.


@click.command()
@click.option('--level', default='info', help='Number of greetings.')
@click.option('--conf', prompt='conf path',
              help='The person to greet.')
def main(level, conf):
    """Simple program that greets NAME for a total of COUNT times."""
    logger.setLevel(getattr(logging, level.upper()))
    if not os.path.exists(conf):
        logger.error("conf not exitst {}".format(conf))
        return
    content_d = json.loads(open(conf, "r", encoding='utf-8').read())
    logger.debug("content:{}".format(json.dumps(
        content_d, ensure_ascii=False, indent=2)))
    # generated_by_dict_unpack: content_d
    directory, command_list = content_d["directory"], content_d["command_list"]
    monitor(directory, command_list)


def monitor(path, command_list):
    wm = WatchManager()
    mask = IN_DELETE | IN_CREATE | IN_MODIFY
    handler = EventHandler(logger, command_list=command_list,
                           directory=path)
    notifier = Notifier(wm, handler)
    handler.start()
    wm.add_watch(path, mask, auto_add=True, rec=True)
    logger.info("now start monitor %s" % path)
    while 1:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            handler.stop()
            break


if __name__ == "__main__":
    main()