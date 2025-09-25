import pygame as pg
import m_ake as mk


def main ():
    pg.init()
    window = mk.window.Window()
    clock = pg.time.Clock()
    dt = 0

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
        dt = clock.tick(24) / 1000

    pg.quit()

def interrupt ():
    print("Interrupt received")
    pass

if __name__ == "__main__":
    main()

