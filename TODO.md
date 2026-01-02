# m ake: Software To-do List

## 1. High Priority
- [ ] ???


## 2. Feature Roadmap
- [ ] World file format (YAML) and loading
    - [x] Instantiating sprites
    - [x] Loading sprite materials from assets
    - [x] Instantiating physical actors & collision
    - [ ] General object property settings (i.e. intial position, velocity)
    - [ ] Certain privileged world attributes (rotation rate, gravity, etc.)
- [ ] Controller refactor
    - [ ] Finite state machine with states being unique classes
    - [ ] Separate key handler (event) class maps inputs to controller commands
    - [ ] Controller states:
        - [ ] Grounded (walking) state incl. full animation data
        - [ ] Inertial (flying/floating) state incl. full animation data
        - [ ] Jumping (mid-jump) temporarily disabling collision
        - [ ] Ukemi (landing) transitions from inertial to grounded
        - [ ] Consider further options such as melee attack, etc.


## 3. Eventual needs
- [ ] UI system (ideally at native resolution)
    - [ ] Handling for different display resolutions
    - [ ] Title screen and state loader
- [ ] Standard for custom PyGame events
- [ ] Sound loading and playback
- [ ] Browser distribution with [Pygbag](https://github.com/pygame-web/pygbag)


## 4. Detail-Oriented Goals
- [ ] Synchronize forward leg with walk/run animations
- [ ] Fine-grained collision primitives for speed
- [ ] "Smart" animation system
    - [ ] Custom animation data & handling
    - [ ] Emitting signals for other systems

