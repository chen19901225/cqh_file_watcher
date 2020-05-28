import threading
import shlex
import subprocess
import os


class LogPipe(threading.Thread):

    def __init__(self, level, prefix=''):
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
            self.level(self.prefix + line.strip("\n"))
            # logging.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        """Close the write end of the pipe.
        """
        os.close(self.fdWrite)


class CommandCaller(threading.Thread):

    def __init__(self, task_queue, logger):
        threading.Thread.__init__(self)
        self.daemon = False
        self.task_queue = task_queue
        self.logger = logger

    def run(self):
        logger = self.logger
        while 1:

            logger.debug("begin for loop")
            try:
                is_end, data_list = self.task_queue.get()
                if is_end:
                    self.logger.info("CommandCaller complete ")
                    break
                for data_d in data_list:
                    # generated_by_dict_unpack: data_d
                    pattern, relative_path, command, path = data_d["pattern"], data_d["relative_path"], data_d["command"], data_d["path"]
                    directory = data_d["directory"]
                    logger.info("pattern:{}, relative_path:{}, path:{}, command:{}".format(
                        pattern,
                        relative_path,
                        path,
                        command
                    ))
                    cmd_list = shlex.split(command)
                    # logging.info("[system], cmd_list:{}".format(cmd_list))

                    def write_to_logger(pipe, method, prefix=''):
                        for line in iter(pipe.readline, b''):  # b'\n'-separated lines
                            method(prefix + line.decode("utf-8").rstrip("\n"))

                    try:

                        process = subprocess.Popen(cmd_list,
                                                   #  check=True,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.STDOUT,
                                                   cwd=directory)
                        with process.stdout:
                            write_to_logger(process.stdout, logger.info)
                        # with process.stderr:
                        #     write_to_logger(process.stderr, logger.error, '[error]')
                        process.wait()

                    except Exception as e:
                        logger.exception("fail to run command:{}, {}".format(command,
                                                                             e),
                                         )
                        raise

                    logger.info("complete pattern:{}, relative_path:{}, path:{}, command:{}".format(
                        pattern,
                        relative_path,
                        path,
                        command
                    ))

            except Exception as e:
                logger.exceptioin("fail in CommandCaller {}".format(e))
