__version__ = "0.11.0"

import logging

from koswat.main import run_analysis

if __name__ == "__main__":
    try:
        run_analysis()
    except Exception as e_info:
        logging.error(str(e_info))
