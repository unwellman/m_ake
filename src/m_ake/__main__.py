import pygame as pg
import m_ake as mk

def main ():
    window = mk.window.Window()

    handler = mk.event.Event_handler()
    should_close = mk.event.State_bool(False)
    handler.bind(pg.QUIT, should_close(True))

    screen = mk.gfx.Screen((320, 180))
    window.bind_screen(screen)

    while not should_close:
        handler()
        window()

    pg.quit()

if __name__ == "__main__":
    main()

