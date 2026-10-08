from pathlib import Path, PosixPath
import logging

STANDARD_FORMAT = "[%(levelname)s] - %(message)s"
DEBUG_FORMAT = "[%(levelname)s] - %(filename)s:%(lineno)s - %(message)s"

logger = logging.getLogger(__name__)

class DebugFormatter(logging.Formatter):
    def __init__(self, debug=False, fmt = None, datefmt = None, style = "%", validate = True, *, defaults = None):
        if fmt is None:
            fmt = DEBUG_FORMAT if debug else STANDARD_FORMAT

        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: logging.LogRecord):
        no_style = '\033[0m'
        # bold = '\033[91m'
        grey = '\033[90m'
        # yellow = '\033[93m'
        # red = '\033[31m'
        # red_light = '\033[91m'
        start_style = {
            'DEBUG': grey,
            # 'INFO': no_style,
            # 'WARNING': yellow,
            # 'ERROR': red,
            # 'CRITICAL': red_light + bold,
        }.get(record.levelname, no_style)
        end_style = no_style
        return f'{start_style}{super().format(record)}{end_style}'



def setup_logging(debug: bool = False):
    root_logger = logging.getLogger()
    formatter = DebugFormatter(debug)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    root_logger.setLevel(logging.DEBUG) if debug else root_logger.setLevel(logging.INFO)
    logger.info(f"setup logging, mode {logging.getLevelName(logger.getEffectiveLevel())}")
