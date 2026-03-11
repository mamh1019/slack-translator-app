# -*- coding: utf-8 -*-

import multiprocessing
import os

# core options
wsgi_app = "main:app"
cwd = os.path.dirname(os.path.abspath(__file__))
cores = multiprocessing.cpu_count()
workers_per_core = 2 * cores
default_web_concurrency = workers_per_core * cores + 1
web_concurrency = max(int(default_web_concurrency), 2)
bind = "0.0.0.0:5200"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count()
timeout = 300

# memory options
max_requests = 1000
max_requests_jitter = 100
graceful_timeout = 30

# log options
errorlog = "{}/logs/errorlog.txt".format(cwd)
accesslog = "{}/logs/accesslog.txt".format(cwd)
loglevel = "error"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# side options
daemon = True


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


"""
def pre_fork(server, worker):
    pass
"""


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback

    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for (
        threadId,
        stack,
    ) in sys._current_frames().items():  # pylint: disable=protected-access
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
