# m ake

## Memo from Noah: draft roadmap

Before we can get started drawing an asset or writing a line of code, there are
some organizational decisions we should make. I listed my initial thoughts here,
so let me know what your input is so we can lock down the un-fun stuff.

### Project Organization
- [ ] **Devlog and spec**: First and foremost, we need a place to formally
    document the design and specification of the project, as well as keep track
    of changes. I'm a fan of plaintext files or Markdown documents like this
    one, but something like a Google Doc might be easier.
- [ ] **Version control**: Since multiple people are working on the game,
    version control is necessary to make sure breaking changes don't ruin an
    existing copy. Git (with hosting on GitHub) is the go-to tool, but a
    fileserver with some editing/logging rules can also do the trick.
- [ ] **Meetings and timeline**: Having dedicated time to share progress and
    direct future effort is a must. A project calendar might be a good idea.

### Game Design
- [ ] **Scope**: For an initial project, we should strive for something small.
    If anything, it might be a good idea to re-create an existing game to get a
    feel for our workflow and team dynamics. Maybe a mock FF or DraQue remake?
- [ ] **Genre**: It sounds like the overarching gameplay idea is a JRPG, but a
    detailed description is important early on in order to make good technical
    decisions about engine and development.
- [ ] **Story**: Some things about lore and overarching story beats can be
    decided by committee, but detailed script-writing is more of an individual
    task. We probably want a dedicated place to keep track of what kind of world
    we're building and what happens in it.

### Pre-development Work
- [ ] **Target platform**: I'm assuming this is just keyboard/mouse on
    PC/MacOS/Linux, but adding platforms after the very beginning gets really
    difficult. Speak now or forever hold your peace.
- [ ] **Engine**: I'm interested in trying my hand at writing the engine from
    scratch in C using [SDL3](https://www.libsdl.org/). I'm also open to having
    us use a prefab engine like Unity, especially to get something going quickly
    in the proof-of-concept phase.
- [ ] **Creator tools**: We should also decide on other tools we're using, like
    DAWs for music and SFX, drawing programs for art, and ABI languages for
    game scripting.

We should probably have a general project-start meeting to decide on the mundane
bits of this, and publish a final draft roadmap for what we need to do before
writing any code. Once we have a framework for working together, it will be
easier to contribute and edit new ideas on our own time. 

Signed,

unwell

