# Intro audio queue repair

Date: 2026-11-08. Branch: `feature/opengl-first-run`.

## Trigger and scope

During manual testing the user reported intro music cutting out around the robot
shooting sequence. The user authorized a fix but explicitly prohibited launching
the game. No game launch, UI interaction, audio-device creation, or audible
playback was performed during this work.

This repairs the Smacker cutscene path in `conversion/`. It does not replace
OpenAL/ALURE or implement the stage-three audio architecture. `original/` remains
unchanged. The defects described below exist in the published implementation;
their relationship to the 1999 retail game is unknown. This user-requested repair
does not establish that they were retail bugs or migration regressions.

## Findings and changes

- The old code divided the initial packet among six buffers, immediately filling
  the entire fixed pool. It then attempted to submit that same decoded frame's
  audio through the normal frame path. If no processed/free buffer was available,
  it returned without preserving the current packet and subsequently advanced
  to the next movie frame. This explicitly permitted missing audio.
- The new `AniSmackerAudioQueue` submits the initial packet through the same path
  as subsequent packets, once per decoded frame. It reclaims processed buffers
  and allocates another when necessary instead of dropping a packet at six.
  Empty packets are ignored. Allocated buffers are retained for reuse and deleted
  after the source is deleted; rewind stops and empties the queue before reuse.
- The old frame-duration conversion multiplied microseconds by `0.000000826`,
  shortening the nominal movie timeline by 17.4%. Use `0.000001` to convert to
  seconds and advance the scheduled deadline by one movie frame rather than
  repeatedly resetting it to the latest render time. This avoids accumulating
  render-delay drift. It does not introduce a separate audio thread or guarantee
  uninterrupted playback through arbitrary main-thread stalls.
- Wait for the final audio to drain before marking the movie finished, continuing
  to display the last image. An explicitly skipped/destroyed movie still releases
  its source and buffers. This avoids immediately cutting the remaining audio
  when the last video frame is reached.

The intro asset `flics/animatic.smk` contains 2,215 frames at 40,000 microseconds
per frame and 15,805,440 decoded PCM bytes (89.6 seconds). Its first packet is
183,456 bytes, approximately a second of audio. `postload.smk` contains 45 frames
and 143,346 PCM bytes. These measurements came from decoding without playback.

## Verification

`conversion/tests/smacker_audio_queue_test.cpp` uses the real bundled Smacker
decoder and a simulated OpenAL queue. Assertions remain enabled. It checks:

- 32 packets submitted without consumption, exceeding the old pool of six.
- Buffer recycling, empty packets, stopping/resetting for rewind, and cleanup.
- All 59 top-level `flics/*.smk` files inspected, including exact PCM byte counts
  and an order-sensitive byte hash for all 15 that contain track-zero audio.
  Simulated consumption includes bursts of catch-up frames. No audio device
  is opened. All checks passed.

The test validates queue behavior and packet preservation. It does not exercise
the actual renderer, OpenAL driver, complete movie scheduler, or audible A/V sync.
The reported in-game symptom is not yet confirmed resolved; user playback is
still required. Both intro audio paths and menu/gameplay audio need manual checks.

## Windows build and local artifacts

The experiment reuses the successful ground-zero build and dependency set.
`tools/build-intro-audio-experiment.py` runs inside the existing container. It
compiles the changed `smackei.cpp` plus `smacker.cpp` against the patched internal
headers, then relinks the existing game objects. Recompiling `smacker.cpp` is
necessary because it allocates the implementation object whose layout changed.
Other translation units retain their baseline object code. This is an incremental
patched-baseline experiment, not a clean build of the complete conversion tree
or the pending native Windows build milestone.

The script restores the original two object files and baseline executable even
on failure. Staged conversion files are under `build/opengl/intro-audio-source`.
The output is `build/opengl/bin/machines-opengl-intro-audio.exe`, SHA-256
`339e98586c26c7a43a2790ae22b2832fb2ec97b842d987994c9614a1311ab9e3`.
Logs are `build/opengl/logs/intro-audio-build.log` and
`intro-audio-queue-test.log`; packet inventory is `smacker-audio-inventory.log`.

After verifying no game process was running, copied the new executable to
`build/opengl/runtime-baseline/machines/machines-opengl.exe`. The previous binary
is retained beside it as `machines-opengl-before-intro-audio.exe`. The repaired
Vorbis DLL alias and the user's 1280 x 720 configuration were retained.

The game was not launched. Future interactive testing requires the user's
go-ahead. Check the entire intro, including the shooting sequence and transition
to the menu, for interruptions, speed, synchronization, and a clipped ending.
Then verify skip/replay behavior, another cutscene, and gameplay audio. Missing
4K resolution remains a separate unresolved observation.

## Authorized playback result

The user subsequently authorized launching the repaired build for a shared test.
Its SHA-256 was checked before launch. The game started at the saved 1280 x 720,
60 Hz setting; launch logs use prefix `intro-test-20261108-174621` under
`build/opengl/logs`. No errors appeared in the checked stderr log.

The user confirmed that the music stayed continuous through the shooting
sequence and reported that everything worked perfectly during this test. This
verifies the reported intro interruption as resolved in that manual playback.
It does not establish complete gameplay, multiplayer, or retail audio fidelity.

The assistant's computer-use captures continued to show the loading image while
the user observed successful playback. Those captures were stale and are not
evidence of a game loading failure. The audible result is user-confirmed, not
independently heard by the assistant. No subsequent game stop was requested or
performed as part of recording this result.
