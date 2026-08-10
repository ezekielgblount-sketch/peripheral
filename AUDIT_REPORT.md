# Isolation Pivot — Synthesized Audit Report

*Synthesis of three independent audits (feasibility, consistency, player-experience) of the Peripheral → Isolation design pivot.*

## Summary

All three audits converge on the same underlying diagnosis even though they were run independently and looked at different material: this team's actual failure mode is not "bugs happen," it's *silent divergence* — two things that are supposed to correspond (two hex palettes, two axis conventions, a rule and its violation, a state and its notification) drifting apart with no mechanism catching it until a human notices. The Isolation pivot introduces several new instances of exactly this pattern, at three levels: **unresolved documentation conflicts** (palette, loud-transient rule, sprint rule), **technical architecture that reproduces the project's one prior real bug shape** (house topology shifting, notification-free item attrition), and **a design-level tension between two different games** (Peripheral's perception mechanic vs. Isolation's mystery/narrative layer) that no document actually reconciles. The strongest signal in this synthesis is where two audits reached the same conclusion from different angles without coordinating — those are flagged explicitly below.

---

## Findings, ranked by severity and actionability

### 1. Day 3 climax directly violates two of the project's own "hard, unchanged" rules
**Source: Consistency Audit + Player-Experience Audit (independently convergent)**

`CLAUDE.md`'s don't-list keeps "No jumpscares, screamer stings, or loud transients. Ever. **(unchanged)**" and "No stamina, no jump, no crouch, no sprint — still hold" marked unchanged in the very same editing pass that approved the Day 3 back-door sequence. But `FEATURE_LIST.md`'s own source text describes that sequence as "fast, **loud**, approaching footsteps... escalating until Jack **rushes** toward the back door." Two auditors flagged this independently: the consistency audit as an uncited textual collision between a resolved feature and two un-touched hard constraints, and the player-experience audit as a design failure — a chase the player cannot fail (the entity never touches/kills) reads as a cutscene, and it breaks the exact "nothing ever confirms itself" grammar the whole game trains for two days. The player-experience audit also offers a concrete fix: build the climax on the existing cricket-silence-approaching cue (already identified elsewhere in the docs as the strongest scare in the game) instead of importing chase-footstep audio, and settle whether the escape is a forced/scripted camera move or leave the no-sprint contradiction on record. This should be resolved before any Day 3 audio or player-controller work begins.

### 2. Palette conflict is unresolved and already causing active work to fork
**Source: Consistency Audit**

`VISUAL_REFERENCE.md` carries an open "CONFLICTS WITH EXISTING ART DIRECTION — NEEDS A TEAM DECISION" banner that nothing in `FEATURE_LIST.md`'s six resolved items actually closes (the one item that looks related resolves a blur-technique question, not the hex-value question). Two full, different hex palettes are simultaneously live, plus a directly reversed rule on the Act 2 flashlight's warm-color exception (permitted per handoff/`CLAUDE.md`, explicitly forbidden per `VISUAL_REFERENCE.md`). This is not theoretical: `NEXT_TASKS.md` task 2, in progress now, has already hardcoded the handoff palette into real materials — a de facto decision made by an implementer rather than a documented one. Anyone consulting `VISUAL_REFERENCE.md` as the art bible would build the other palette, and the deferred Act 2 flashlight work is queued to hit the same fork. Highest-impact open item because it is actively blocking in-flight work, not just a future risk.

### 3. House topology shifting reproduces the project's one known failure shape, in its highest-value systems
**Source: Feasibility Audit**

The team's only confirmed real bug (the spec-metres/Unreal-uu and x/z-vs-X/Y axis mismatch) had the shape "two representations of the same fact, nothing enforces correspondence." Topology shifting recreates that shape exactly: every anomaly anchor placed so far was hand-measured against the *current* built geometry and hardcoded, while `FoveaComponent`'s occlusion/angle checks and the anomaly re-arm rule ("must be in a different room than where it resolved") both assume room identity and anchor points are stable facts. Once rooms move, there is no equivalent of `CLAUDE.md`'s unit-conversion table to catch a stale anchor or a raycast passing through geometry that used to be there — and unlike the axis bug, this one fails silently (an anomaly's occlusion succeeding or failing against geometry nobody re-validated) rather than loudly. This touches the systems both design docs independently call the most important in the game.

### 4. The global clarity cap may defeat the game's signature mechanic
**Source: Player-Experience Audit** (related staleness issue independently flagged by Consistency Audit — see below)

Peripheral's core loop depends on centered vision being *authoritative*: look at the wrongness, confirm it's ordinary, feel the sting of "it was nothing." Isolation's global 60–70% clarity cap (applied even to dead-centre, sustained focus) removes that confirmation — the state machine's clean binary resolve still exists in code but becomes something the player can never actually perceive, degrading "was that an anomaly?" into general visual mud. The audit notes Isolation's actual stated concern (§12: the entity should never become *fully* visible) is narrower than the rule that got adopted, and proposes a concrete, low-cost fix: cap clarity on the entity and humanoid-figure anomalies only, and let ordinary-object anomalies (lamp, chair, coat) reach full clarity when centered so the resolve snap stays legible. Separately, the Consistency Audit notes `VISUAL_REFERENCE.md` §6 still claims direct gaze is "~100% readable," contradicting `CLAUDE.md`'s broader cap and never corrected to match — a documentation-only version of the same seam (the actual implementation in `NEXT_TASKS.md` task 4 is already correct, so this half is lower urgency, but it means the design intent behind the cap is itself unsettled on paper, not just in feel).

### 5. Comfort-item attrition is simultaneously the highest-risk new system and one of the two ideas worth building the game around
**Source: Feasibility Audit + Player-Experience Audit (convergent from opposite angles)**

The feasibility audit ranks silent, no-notification comfort-item removal as the second-highest risk in the whole feature list: it is explicitly designed to have zero observable signal, which defeats the *only* verification method that has caught a real bug on this project (a live PIE keypress with a human watching the result), and it's genuinely new architecture with no existing pattern to extend from. The player-experience audit, arguing from design quality rather than implementation risk, independently singles out the same feature as one of only two Isolation additions that feel authored rather than assembled, and argues it should be treated as a pillar and preserved. Both audits are pointing at the same feature as unusually high-leverage — which argues for deliberately over-investing in test coverage and edge-case handling here (equipped items, mid-interaction items, item-removed-from-world-but-still-referenced states) precisely because the design is worth protecting and the failure mode is invisible by construction.

### 6. Director pacing was tuned for an 8-minute run and hasn't been validated at 3-day length
**Source: Player-Experience Audit**

The anomaly-arming cadence (one every 25–40s, 12 anomalies total) is scoped for roughly an 8-minute prototype; a 3-day structure implies 60–120+ minutes, and the only ways to fill that gap are habituation-risking constant firing or thin spreading padded with scripted events — of which there are only about eight designed, and Day 2's "work/commute" loop is an entirely unscoped environment mentioned nowhere in implementation planning. Compounding this, the design's own content explicitly stops at the Day 3 climax (§67) with no designed resolution to the identity mystery. This is a schedule and design-completeness risk, not just a tuning one: nobody has tested whether the core look-away/look-back loop survives even 30 minutes of repetition, let alone hours. Recommended gate: a 30-minute continuous playtest of the anomaly loop before locking the 3-day frame.

### 7. Random event framework is the trigger layer for the two highest technical risks above
**Source: Feasibility Audit**

The conditional event system (day/time/behavior/isolation-level-keyed, §21–32) is the layer that fires both topology shifts and comfort-item removal — meaning a timing or condition bug here doesn't just misfire one event, it can desync the two systems already flagged as riskiest (#3 and #5 above). It's structurally similar to the arming-weight formula the team has built successfully once before, but a multi-trigger conditional scheduler is easy to get subtly wrong in ways that only surface over a long unattended session — a failure pattern the team already flagged about itself in its own retrospective.

### 8. Two more "unchanged" rules in CLAUDE.md's don't-list are already broken by the pivot
**Source: Player-Experience Audit** (sprint half also independently flagged by Consistency Audit)

Beyond the loud-transient/chase issue (#1), the mandate to build a fourteen-type collectible system of letters, documents, and identity records sits directly beneath "No blood, gore, or written lore — (unchanged)." That is written lore by definition. The standing rule "default to Isolation, not case-by-case" is flagged as a process problem in its own right: it has already produced two clean, undebated contradictions inside the same document. Recommendation from the audit: decide explicitly whether documents carry the mystery (retire the no-lore rule) or the mystery stays environmental and collectible types shrink toward photographs/audio — and stop marking rules "(unchanged)" next to features that already changed them.

### 9. Act 1/Act 2 single-night structure vs. Isolation's 3-day structure is unmapped
**Source: Consistency Audit** (related to Player-Experience's point that the mystery has no designed ending)

The handoff's single-evening Act 1 → Act 2 → epilogue flow (ending in a key/lock-up beat) and `FEATURE_LIST.md`'s 3-day timeline with its own Day 3 climax look like two versions of the same breaker/lockdown sequence, but no document says whether the epilogue still happens, is superseded, or how Act 1/2 nests inside "Day 1." `NEXT_TASKS.md` still references "the full Act 1/2 system" as pending, implying the old structure is assumed to survive — but nothing confirms it. Not yet urgent since day-structure work isn't scheduled, but it should be resolved before it is.

### 10. Forced-camera Day 3 sequence risks violating the "anomaly never visibly transitions" rule
**Source: Feasibility Audit**

Combining the Act 2 entity's "never touches, removed the exact frame it's centred" logic with a forced, non-player-controlled camera rush toward the back door could put the player's locked view directly on the entity mid-transition — violating what `CLAUDE.md` calls the one rule that matters most. Lower likelihood than the other technical risks since it's additive on two already-proven mechanisms rather than new architecture, but worth a dedicated check specifically for the forced-camera case, which neither prior system was built to handle.

### 11. The pivot's narrative layer is a seam, not a fusion, and its most original prior idea was deleted rather than adapted
**Source: Player-Experience Audit**

Peripheral's thesis (the gap between looking and seeing) and Isolation's thesis (who is Jack) could fuse — an amnesiac's untrustworthy memory pairs naturally with untrustworthy perception — but nothing in the docs draws that line; the memory-collectible system sits beside the fovea mechanic as a conventional pick-up-and-examine loop rather than being built from the same grammar. The audit also notes most of Isolation's narrative beats are recognizable genre tropes (inherited house, day-structured escalation, document backstory, sanity-adjacent hidden state, a phone contact going subtly wrong, topology shifts) with the comfort-attrition and porch-relief-valve mechanics being the two exceptions worth keeping. Separately, the pivot quietly retired the buyer-sign mechanic (the player's own typed name vanishing from a sign) without translating it — flagged as arguably the single most original beat in the prior build, discarded rather than carried forward as, e.g., a Jack-equivalent name-on-the-deed effect.

---

## Safe to ignore for now

- **Citation error**: `FEATURE_LIST.md` item 6 attributes the "only exterior door" quote to `CLAUDE.md`; it actually originates in `PERIPHERAL_UNREAL_HANDOFF.md` §5. *(Consistency Audit)* — cosmetic, worth a one-line fix so future searches don't go to the wrong file, no design impact.
- **`VISUAL_REFERENCE.md` §6/§7 internal clarity-percentage inconsistency**: superseded in practice — `NEXT_TASKS.md` task 4 already implements the correct capped version and even calls out the exact trap of copying the stale spec verbatim. *(Consistency Audit)* Only matters if someone re-derives spec from `VISUAL_REFERENCE.md` alone instead of the code; folded into finding #4 above as the design-intent question is the part that actually matters.
- **Collectible-type count (fourteen types) and Day 2 commute scope** as standalone complaints: real, but they're sub-points of the broader pacing risk already captured in finding #6, not independent blockers.