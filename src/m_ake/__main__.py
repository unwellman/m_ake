import pygame as pg
import m_ake as mk

def main ():
    window = mk.window.Window()

    should_close = mk.event.State_bool(False)

    handler = mk.event.Event_handler()
    handler.bind(pg.QUIT, should_close(True))

    while not should_close:
        handler()

    pg.quit()

if __name__ == "__main__":
    main()

