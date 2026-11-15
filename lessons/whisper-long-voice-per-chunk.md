---
title: Transcribe a long TTS voice per chunk; one Whisper pass drifts
kind: gotcha
applies_when: when word timings for captions, pauses or cuts come from one Whisper pass over a voice longer than about 2 minutes (`transcript.json`, `pause_inject`)
projects: all
evidence: 2026-11-15 hyperframes PR #122
last_validated: 2026-11-15
status: active
---

Do not take word timings from one Whisper (large-v3) pass over a voice longer than about 2 minutes.
Transcribe each TTS chunk on its own, using the chunk start and end the TTS step recorded, add the chunk start to every word, and join the lists before any pause or caption step reads them.
Check the result per paragraph on the final audio: every script word heard in order, and no word doubled next to itself.
Why: on a 3-minute voice the single pass drifted from 135 s on, so the pause step missed 9 paragraph starts; on a 2:30 voice it dropped a whole phrase while the audio was complete, right after an unrelated paragraph changed.
Confirm it worked: the gaps between paragraphs measured after the pause step equal the intended pause, and the per-paragraph check finds no missing or doubled word.
