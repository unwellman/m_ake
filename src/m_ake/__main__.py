import pygame as pg
import m_ake as mk

import sys
import logging
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger("m_ake")
logger.setLevel("DEBUG")


def main ():
    mk.init(__file__)
    pg.init()
    clock = pg.time.Clock()
    dt = 0
    window = mk.window.Window(clock=clock)

    main_events = [mk.state_change, pg.QUIT,
                   pg.WINDOWRESIZED]

    handler = mk.event.Event_handler(types=main_events)
    running = mk.event.State_bool(True)
    handler.bind(pg.QUIT, running(False))

    from m_ake.scripts.platform import Platform
    entry_state = Platform()
    entry_state.resume(window=window)

    while running:
        handler()
        entry_state.loop(dt)
        window()
        dt = clock.tick(60) / 1000

    pg.quit()

def interrupt ():
    print("Interrupt received")
    pass

if __name__ == "__main__":
    main()

