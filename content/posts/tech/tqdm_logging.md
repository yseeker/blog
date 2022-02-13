---
#author: "Hugo Authors"
title: "loggerとprintとtqdmの併用"
date: "2022-02-13"
#description: "Sample article showcasing basic Markdown syntax and formatting for HTML elements."
tags: ["tqdm", "logging", "print", "標準出力"]
categories: ["技術"]
ShowToc: true
TocOpen: true
draft: false
---

logger と print と tqdm を併用する場合は以下のコードをコピペする。

参考

- [https://github.com/tqdm/tqdm#redirecting-writing](https://github.com/tqdm/tqdm#redirecting-writing)
- [https://qiita.com/mino-38/items/f09251d18fe3181bfbfd](https://qiita.com/mino-38/items/f09251d18fe3181bfbfd)
- [https://waregawa-log.hatenablog.com/entry/2020/01/01/100000](https://waregawa-log.hatenablog.com/entry/2020/01/01/100000)
- [https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output](https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output)

```python
import contextlib
import logging
import logging.handlers
import sys
from time import sleep

from tqdm import tqdm
from tqdm.contrib import DummyTqdmFile


class TqdmLoggingHandler(logging.Handler):
    colors = {"INFO": "\033[37m{}\033[0m", "ERROR": "\033[31m{}\033[0m"}

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            record.msg = TqdmLoggingHandler.colors.get(record.levelname, "{}").format(
                record.msg
            )
            msg = self.format(record)
            tqdm.write(msg, file=sys.stderr)
            self.flush()
        except Exception:
            self.handleError(record)


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger(name, logfile="log.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even DEBUG messages
    fh = logging.handlers.RotatingFileHandler(
        logfile, maxBytes=100000000, backupCount=10
    )
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s"
    )
    fh.setFormatter(fh_formatter)

    # create console handler with a INFO log level
    ch = TqdmLoggingHandler()
    ch.setLevel(logging.INFO)
    # coloredlogs.install(
    #     level="INFO",
    #     logger=logger,
    #     fmt="%(asctime)s : %(message)s",
    #     datefmt="%Y/%m/%d %H:%M:%S",
    # )
    ch_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s"
    )
    ch.setFormatter(CustomFormatter())

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = setup_logger(__name__)


@contextlib.contextmanager
def std_out_err_redirect_tqdm():
    orig_out_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = map(DummyTqdmFile, orig_out_err)
        yield orig_out_err[0]
    # Relay exceptions
    except Exception as exc:
        raise exc
    # Always restore sys.stdout/err if necessary
    finally:
        sys.stdout, sys.stderr = orig_out_err


def some_fun(i):
    logger.info("Fee, fi, fo,".split()[2])
    print("Fee, fi, fo,".split()[2])


# Redirect stdout to tqdm.write() (don't forget the `as save_stdout`)
with std_out_err_redirect_tqdm() as orig_stdout:
    # tqdm needs the original stdout
    # and dynamic_ncols=True to autodetect console width
    for i in tqdm(range(3), file=orig_stdout, dynamic_ncols=True):
        sleep(0.5)
        some_fun(i)

# After the `with`, printing is restored
print("Done!")

```
