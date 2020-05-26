#!/usr/bin/python
# coding:utf-8
import shlex
import subprocess
import re
import json
import sys
import logging
 
import os
from pyinotify import WatchManager, Notifier,ProcessEvent,IN_DELETE, IN_CREATE,IN_MODIFY
# https://codereview.stackexchange.com/questions/6567/redirecting-subprocesses-output-stdout-and-stderr-to-the-logging-module
import threading

class LogPipe(threading.Thread):

    def __init__(self, level):
        """Setup the object with a logger and a loglevel
        and start the thread
        """
        threading.Thread.__init__(self)
        self.daemon = False
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe
        """
        return self.fdWrite

    def run(self):
        """Run the thread, logging everything.
        """
        for line in iter(self.pipeReader.readline, ''):
            self.level(line.strip("\n"))
            # logging.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        """Close the write end of the pipe.
        """
        os.close(self.fdWrite)

class EventHandler(ProcessEvent):
    def __init__(self, logger, command_list, directory):
        super().__init__()
        self.logger = logger
        self.command_list = command_list
        self.directory = directory
        
    
    def process_IN_CREATE(self, event):
        self.handle_event(event)
    def process_IN_DELETE(self, event):
        self.handle_event(event)
    def process_IN_MODIFY(self, event):
        self.handle_event(event)
    def process_IN_MOVE(self, event):
        self.handle_event(event)
    def handle_event(self, event):
        # self.logger.debug("event:{}".format(event))
        for command_d in self.command_list:
            pattern = command_d.get("pattern")
            # generated_by_dict_unpack: command_d
            command = command_d["command"]
            should_execute = False
            if not pattern:
                should_execute = True
            else:
                if not pattern.endswith("$"):
                    pattern+="$"
                pattern = re.compile(pattern)
                if pattern.match(event.name):
                    should_execute=True
            if should_execute:
                logger.info("pattern:{}, name:{}, path:{}".format(
                    pattern,
                    event.name,
                    event.path
                ))
                cmd_list = shlex.split(command)
                # logging.info("[system], cmd_list:{}".format(cmd_list))
                process = subprocess.run(cmd_list, 
                                        #  check=True,
                                        stdout=LogPipe(logger.info),
                                        stderr=LogPipe(logger.info),
                                         universal_newlines=True,
                                        cwd=self.directory)
                logger.info("complete pattern:{}, name:{}, path:{}, command:{}".format(
                    pattern,
                    event.name,
                    event.path,
                    command
                ))
                # output, errput = process.stdout, process.stderr
                # if output:
                #     logger.info(output)
                # if errput:
                #     logger.error(errput)
                    # raise Exception("Failed called with {}, {}, {}".format(
                    #     command,
                    #     output,
                    #     errput
                    # ))
                
                # return output, errput
    


logger = logging.getLogger('cqh_file_watcher')
if not logger.handlers:
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                                                  datefmt='%y%m%d %H:%M:%S'))
    # stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    # logger.


import click

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
    logger.debug("content:{}".format(json.dumps(content_d, ensure_ascii=False, indent=2)))
    # generated_by_dict_unpack: content_d
    directory, command_list = content_d["directory"], content_d["command_list"]
    monitor(directory, command_list)
        
    

def monitor(path, command_list):
    wm = WatchManager()
    mask = IN_DELETE|IN_CREATE|IN_MODIFY
    notifier = Notifier(wm, EventHandler(logger, command_list=command_list,
                                         directory=path))
    wm.add_watch(path, mask, auto_add=True, rec=True)
    logger.info("now start monitor %s"% path)
    while 1:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break
            
        
        
   
# def FSMonitor(path, commands):
    
    
#   	wm = WatchManager()
   
   
#   	mask = IN_DELETE | IN_CREATE |IN_MODIFY|IN_MOVE
#   	notifier = Notifier(wm, EventHandler(logger, command_list=commands))
   
#   	wm.add_watch(path, mask,auto_add=True,rec=True)
#   	logger.info("now start monitro %s"% path)
   
   
#   	#   print 'now starting monitor %s'%(path)
# 	while True:
# 		try:
# 			notifier.process_events()
# 			if notifier.check_events():
# 				notifier.read_events()
# 		except KeyboardInterrupt:
# 			notifier.stop()
# 			break
   
if __name__ == "__main__":
    main()
 