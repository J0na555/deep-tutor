# Architecture change

## context

Initially i was thinking of making the deep tutor a standalone AI tutor application
but, after looking at features of [opencode](https://opencode.ai/) i realized that i was just rebuilding things that opendcode already offers

---

## what changed

deep tutor is no longer being designed as

    - chatbot
    - standalone ai app
    - separate frontend

instead its becoming

    - a contextual laerning layer
    - an orchestration system
    - a terminal native mentor framework

---

## why it changed

the previous architecture was going towards complexity that didnot improve learning

i realized the real value was

    - workflow integration
    - contextual learning
    - memory
    - teaching behaviour


    not building another ui

---

## previous assumption

I originally assumed

    - agents needed to be autonomous
    - Deep Tutor needed its own interface
    - orchestration required complex infrastructure

    most of those were unnecessary for the MVP

---

## New Direction

The system now integrates directly into

    - opencode
    - terminal workflow
    - folder/domain based learning environment

the architecture becomes

leveling arc -> deep tutor -> opencode -> local llm

---

## Technical change

    - removed separate ui direction
    - simplified agent architecture
    - agents became prompt modes
    - orchestration became lightweight
    - shifted focus toward context injection

---

## what i learned

I was initially optimizing for AI architecture, instead of optimizing the learning behaviour (i am the type to over optimize the system instead of starting )

the most important part of the system is not the model or the agents

but the

    - context
    - memory
    - teaching philosophy
    - workflow integration

---

## Next Steps

    - build first mentor prompt system
    - implement lightweight orchestrator
    - add domain based context loading
    - test deep tutor inside one domain (probably dsa)
