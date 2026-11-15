---
title: Fix a scene's camera and layout in code before generating video art
kind: correction
applies_when: when a video or image needs an illustrated scene with depth (isometric, 2.5D, a camera moving through one world)
projects: all
evidence: 2026-11-12 hyperframes channel-intro, owner correction; 2026-11-13 hyperframes videos/channel-intro/ref-recreate/SPEC-v2.md
last_validated: 2026-11-15
status: active
---

Before any image generation or animation, write the scene as data: a floor plan with coordinates, one projection function for the camera, the light direction, and a self-check for overlaps; place every layer with that code only.
Generate the backdrop (floor, paths) and each prop or character as separate transparent images, then composite them through the projection with one scale rule and contact shadows.
Model anything that needs volume (a gate, a machine) in 3D, or draw it, at the same camera angle; never patch it from a model's full-scene image or draw it flat in code.
Leave things hidden by perspective hidden; only logic errors, such as a prop standing on a conveyor, are wrong.
Get the owner's approval of the still scene at a small size before 4K, variants or animation.
Why: letting an image model redraw the whole scene on each fix moved everything (props over the belt, broken belts, stations shifting), and the owner had to say that a 3D model at the same camera angle was the obvious way.
Confirm it worked: the composite passes the layout's self-check, and fixing one item changes no pixel outside it.
