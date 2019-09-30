#!/usr/bin/env python

"""Entry point for the dodge game."""

import logging
import sys
import game

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        game.run()
        LOG.info("Exiting normally")
        sys.exit()
    except (SystemExit, KeyboardInterrupt) as exc:
        LOG.info("Caught %s; exiting", type(exc).__name__)
        sys.exit()
    except: # pylint: disable=bare-except
        LOG.critical("Unexpected error", exc_info=sys.exc_info()[0])
        sys.exit(1)
