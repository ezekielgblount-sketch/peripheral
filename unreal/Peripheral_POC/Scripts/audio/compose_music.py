#!/usr/bin/env python3
"""Composes the game's six music tracks (original, instrumental, synthesised here) into SourceArt/Audio, one per music slot.
Every track is 2 to 3 minutes and loops without a seam: notes and reverb tails that run past the end wrap round to the start.
One melody runs through all of them; each track treats it differently (see TRACKS at the bottom).
Run: python3 Scripts/audio/compose_music.py [slot ...]      then Scripts/import_audio.py in the editor."""
import os, sys, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Audio")
SR = 32000
midi = lambda n: 440.0 * 2 ** ((n - 69) / 12.0)
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def n(name):
    """'E5' or 'Bb3' -> midi number."""
    acc = 1 if "#" in name else -1 if "b" in name[1:] else 0
    return 12 * (int(name[-1]) + 1) + NOTE[name[0]] + acc


class Track:
    def __init__(self, seconds, seed=1):
        self.N = int(seconds * SR); self.buf = np.zeros(self.N); self.rng = np.random.default_rng(seed)

    def add(self, x, t0):
        """Mix x in at time t0; whatever runs past the end comes back in at the start, so the loop has no seam."""
        i = int(t0 * SR) % self.N
        idx = (i + np.arange(len(x))) % self.N
        np.add.at(self.buf, idx, x)

    def piano(self, note, t0, vel=0.6, dur=5.0, cents=0.0, soft=1.0):
        """A felted upright: a few slightly inharmonic partials on three barely mistuned strings, and a soft hammer knock."""
        f0 = midi(note) * 2 ** (cents / 1200.0)
        t = np.arange(int(dur * SR)) / SR
        x = np.zeros(len(t))
        for string in (-0.7, 0.0, 0.9):
            f = f0 * 2 ** (string / 1200.0)
            for k in range(1, 9):
                fk = k * f * np.sqrt(1 + 0.00045 * k * k)
                if fk > SR * 0.45: break
                amp = (1.0 / k ** (1.25 + 0.5 * soft)) * (0.6 if k == 2 else 1.0)
                x += amp * np.sin(2 * np.pi * fk * t + self.rng.uniform(0, 6.28)) * np.exp(-t * (0.55 + 0.32 * k) * (1.0 + (note - 60) / 60.0))
        knock = self.rng.normal(0, 1, len(t)) * np.exp(-t * 90) * 0.5
        knock = np.convolve(knock, np.ones(24) / 24.0, mode="same")
        env = np.minimum(1, t / 0.006) * np.minimum(1, (dur - t) / 0.3)
        self.add((x / 3.0 + knock) * env * vel, t0)

    def box(self, note, t0, vel=0.2):
        """Music-box comb: a pure tone with a glassy overtone, short."""
        f = midi(note); t = np.arange(int(2.5 * SR)) / SR
        x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 6) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)) * np.exp(-t * 2.4)
        self.add(x * np.minimum(1, t / 0.002) * vel, t0)

    def pad(self, notes, t0, dur, vel=0.12, bright=1.0):
        t = np.arange(int(dur * SR)) / SR; x = np.zeros(len(t))
        for nt in notes:
            for d in (-5.0, 0.0, 6.0):
                f = midi(nt) * 2 ** (d / 1200.0)
                for k, a in ((1, 1.0), (2, 0.35 * bright), (3, 0.14 * bright)):
                    x += a * np.sin(2 * np.pi * f * k * t + self.rng.uniform(0, 6.28))
        env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
        self.add(x / (3.0 * len(notes)) * env * vel * 3.0, t0)

    def drone(self, notes, vel=0.1, beat=0.15):
        t = np.arange(self.N) / SR; x = np.zeros(self.N)
        for nt in notes:
            f = round(midi(nt) * self.N / SR) * SR / self.N                # whole cycles in the loop
            x += np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * (f + round(beat * self.N / SR) * SR / self.N) * t)
        swell = 0.7 + 0.3 * np.sin(2 * np.pi * 2 * t / (self.N / SR))
        self.buf += x / len(notes) * vel * swell

    def thump(self, t0, vel=0.1):
        t = np.arange(int(0.3 * SR)) / SR
        self.add(np.sin(2 * np.pi * 62 * t * (1 - 0.3 * t)) * np.exp(-t * 20) * vel, t0)

    # ---- the tape ----
    def spectrum(self, fn):
        f = np.fft.rfftfreq(self.N, 1.0 / SR); self.buf = np.fft.irfft(np.fft.rfft(self.buf) * fn(f), self.N)

    def reverb(self, seconds=2.2, mix=0.3, dark=3500.0, seed=5):
        """A small dark room. Circular, so the tail of the last bar is already in the first."""
        r = np.random.default_rng(seed); m = int(seconds * SR); t = np.arange(m) / SR
        ir = np.zeros(self.N); ir[:m] = r.normal(0, 1, m) * np.exp(-t * 6.9 / seconds)
        f = np.fft.rfftfreq(self.N, 1.0 / SR)
        wet = np.fft.irfft(np.fft.rfft(self.buf) * np.fft.rfft(ir) * (1 / (1 + (f / dark) ** 2)), self.N)
        self.buf = self.buf * (1 - mix) + wet * mix * (np.abs(self.buf).max() / (np.abs(wet).max() + 1e-9))

    def tape(self, wow=0.0008, flutter=0.00012, lowpass=7000.0, hiss=0.012, drift=0.0, drive=1.2):
        """Old tape: slow wow, quick flutter, rolled-off top, hiss, gentle saturation. All periodic over the loop."""
        L = self.N / SR; t = np.arange(self.N) / SR
        warp = (wow * SR * np.sin(2 * np.pi * round(0.45 * L) * t / L + 0.4) / (2 * np.pi * 0.45)
                + flutter * SR * np.sin(2 * np.pi * round(6.3 * L) * t / L) / (2 * np.pi * 6.3)
                + drift * SR * np.sin(2 * np.pi * round(0.11 * L) * t / L + 1.7) / (2 * np.pi * 0.11))
        pos = (np.arange(self.N) + warp) % self.N
        i0 = np.floor(pos).astype(int); fr = pos - i0
        self.buf = self.buf[i0 % self.N] * (1 - fr) + self.buf[(i0 + 1) % self.N] * fr
        self.spectrum(lambda f: 1 / (1 + (f / lowpass) ** 4) * (1 / (1 + (35.0 / np.maximum(f, 1e-6)) ** 4)))
        peak = np.abs(self.buf).max() + 1e-9
        self.buf = np.tanh(self.buf / peak * drive) / np.tanh(drive)
        h = self.rng.normal(0, 1, self.N); H = np.fft.rfft(h); f = np.fft.rfftfreq(self.N, 1.0 / SR)
        h = np.fft.irfft(H * (1 / (1 + (1800.0 / np.maximum(f, 1e-6)) ** 2)) * (1 / (1 + (f / 9000.0) ** 4)), self.N)
        self.buf += h / (np.abs(h).max() + 1e-9) * hiss * (0.8 + 0.2 * np.sin(2 * np.pi * round(0.2 * L) * t / L))

    def save(self, name, peak=0.5):
        x = self.buf / (np.abs(self.buf).max() + 1e-9) * peak
        with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((x * 32767).astype(np.int16).tobytes())
        print("%-22s %5.1f s" % (name, self.N / SR))


# ---- the melody: eight bars, four beats each. (beat, note, length in beats) ----
THEME = [
    [(0, "E5", 3), (3, "C5", 1)], [(0, "A4", 3), (3, "C5", 1)], [(0, "G4", 2), (2, "E5", 1), (3, "D5", 1)], [(0, "D5", 3), (3, "B4", 1)],
    [(0, "C5", 2), (2, "E5", 1), (3, "A5", 1)], [(0, "A5", 1), (1, "G5", 2), (3, "F5", 1)], [(0, "F5", 2), (2, "E5", 1), (3, "D5", 1)], [(0, "E5", 4)],
]
ANSWER = [                                        # a second strain: it climbs a little and comes home
    [(0, "C5", 2), (2, "D5", 2)], [(0, "E5", 3), (3, "G5", 1)], [(0, "A5", 2), (2, "G5", 1), (3, "E5", 1)], [(0, "D5", 4)],
    [(0, "C5", 2), (2, "B4", 2)], [(0, "A4", 3), (3, "C5", 1)], [(0, "B4", 2), (2, "G#4", 2)], [(0, "A4", 4)],
]
MINOR = [["A2", "E3", "C4"], ["F2", "C3", "A3"], ["C3", "G3", "E4"], ["G2", "D3", "B3"], ["A2", "E3", "C4"], ["F2", "C3", "A3"], ["D3", "A3", "F4"], ["E2", "B2", "G#3"]]
MAJOR = [["F2", "C3", "A3"], ["C3", "G3", "E4"], ["A2", "E3", "C4"], ["G2", "D3", "B3"], ["F2", "C3", "A3"], ["C3", "G3", "E4"], ["D3", "A3", "F4"], ["G2", "D3", "B3"]]


def play(tr, bars, chords, bar0, beat, cents=0.0, vel=0.55, left=True, keep=1.0, wrong=0.0, late=0.0, soft=1.0, octave=0):
    """Lay eight bars down starting at bar `bar0`. keep < 1 drops notes; wrong > 0 slips notes a semitone; late smears the timing."""
    for b, (mel, ch) in enumerate(zip(bars, chords)):
        t_bar = (bar0 + b) * 4 * beat
        if left:
            for k, nt in enumerate(ch):                                   # a slow broken chord
                tr.piano(n(nt), t_bar + k * beat * 0.5 + tr.rng.uniform(0, late), vel * 0.5, 6.0, cents, soft + 0.3)
        for (bt, nt, ln) in mel:
            if tr.rng.random() > keep: continue
            note = n(nt) + 12 * octave + (int(tr.rng.choice([-1, 1])) if tr.rng.random() < wrong else 0)
            tr.piano(note, t_bar + bt * beat + tr.rng.uniform(-0.012, 0.02 + late), vel * tr.rng.uniform(0.85, 1.05), 3.0 + ln * beat, cents, soft)


def title():
    beat = 1.0; tr = Track(36 * 4 * beat, 1)                              # 36 bars at 60 bpm: 2 min 24 s
    play(tr, THEME, MINOR, 0, beat, left=False, vel=0.5)                  # the melody alone first
    play(tr, THEME, MINOR, 8, beat)
    play(tr, ANSWER, MINOR, 16, beat)
    play(tr, THEME, MINOR, 24, beat, vel=0.5)
    for b, nt in enumerate(("A4", "E5", "A4")):                           # three bars of settling, one of silence
        tr.piano(n(nt), (32 + b) * 4 * beat, 0.35, 7.0)
    tr.reverb(2.4, 0.32); tr.tape(wow=0.0009, hiss=0.02, lowpass=6500)
    tr.save("music_title")


def day1_calm():
    beat = 1.1; tr = Track(40 * 4 * beat, 2)                              # 2 min 56 s; phrases with long silences between
    for i, ch in enumerate(MAJOR * 5):
        if i % 2 == 0 and (i // 8) % 5 != 2:
            tr.pad([n(x) + 12 for x in ch], i * 4 * beat, 9.5 * beat, 0.10)
    def phrase(bars, chords, bar0, sl):
        for b in sl:
            play(tr, [bars[b]], [chords[b]], bar0 + b, beat, vel=0.45, left=(b % 2 == 0), soft=1.4)
    phrase(THEME, MAJOR, 0, (0, 1, 2, 3)); phrase(THEME, MAJOR, 8, (4, 5, 6, 7))          # bars 4-7 and 16-23 are left empty
    phrase(ANSWER, MAJOR, 24, (0, 1, 2, 3)); phrase(THEME, MAJOR, 28, (4, 5)); phrase(THEME, MAJOR, 32, (0, 1))
    tr.piano(n("C5"), 36 * 4 * beat, 0.3, 8.0, soft=1.5)
    tr.reverb(2.8, 0.38); tr.tape(wow=0.0007, hiss=0.012, lowpass=6000)
    tr.save("music_day1_calm")


def unease_low():
    beat = 1.07; tr = Track(34 * 4 * beat, 3)                             # 2 min 25 s; the title theme, a little flat and unsteady
    play(tr, THEME, MINOR, 0, beat, cents=-17, vel=0.5, late=0.03)
    play(tr, ANSWER, MINOR, 8, beat, cents=-17, vel=0.5, late=0.03)
    play(tr, THEME, MINOR, 18, beat, cents=-22, vel=0.5, late=0.04, left=False)
    play(tr, THEME, MINOR, 26, beat, cents=-22, vel=0.45, late=0.04, keep=0.9)
    for i in (0, 8, 18, 26):
        tr.pad([n("A2"), n("E3")], i * 4 * beat, 30 * beat, 0.06, bright=0.3)
    tr.reverb(2.6, 0.36); tr.tape(wow=0.0030, flutter=0.0006, hiss=0.022, lowpass=4800, drift=0.0018)
    tr.save("music_unease_low")


def unease_mid():
    beat = 1.15; tr = Track(34 * 4 * beat, 4)                             # 2 min 36 s; the melody comes apart over a drone
    tr.drone([n("A1"), n("E2")], 0.22, beat=0.31)
    play(tr, THEME, MINOR, 0, beat, cents=-24, vel=0.45, keep=0.8, wrong=0.18, late=0.12, left=False)
    play(tr, THEME, MINOR, 9, beat, cents=-30, vel=0.42, keep=0.6, wrong=0.3, late=0.2, left=False)
    play(tr, ANSWER, MINOR, 18, beat, cents=-30, vel=0.4, keep=0.55, wrong=0.3, late=0.25, left=False)
    play(tr, THEME, MINOR, 26, beat, cents=-36, vel=0.36, keep=0.4, wrong=0.35, late=0.3, left=False)
    for bar0 in (4, 13, 22, 30):                                          # the music box: the first four bars, far away, a beat behind itself
        for b, mel in enumerate(THEME[:4]):
            for (bt, nt, ln) in mel:
                for echo, v in ((0.0, 0.10), (1.5 * beat, 0.05), (3.0 * beat, 0.025)):
                    tr.box(n(nt) + 12, (bar0 + b) * 4 * beat + bt * beat + echo, v)
    tr.reverb(3.4, 0.5, dark=2600); tr.tape(wow=0.0045, flutter=0.0009, hiss=0.024, lowpass=4200, drift=0.003)
    tr.save("music_unease_mid", 0.48)


def unease_high():
    beat = 1.3; tr = Track(30 * 4 * beat, 5)                              # 2 min 36 s; almost nothing left of the tune
    tr.drone([n("A0") + 12, n("E2")], 0.5, beat=0.19)                     # the deep hum
    tr.drone([n("Bb2")], 0.07, beat=0.43)                                 # one note that does not belong
    for bar0, bars in ((1, THEME), (15, ANSWER)):
        play(tr, bars, MINOR, bar0, beat, cents=-45, vel=0.3, keep=0.3, wrong=0.3, late=0.5, left=False, soft=1.8, octave=-1)
    for t0, nt in ((9, "E4"), (41, "A3"), (77, "C4"), (118, "E4")):
        tr.piano(n(nt), t0, 0.22, 9.0, cents=-50, soft=2.0)
    tr.reverb(4.5, 0.6, dark=1800); tr.tape(wow=0.011, flutter=0.0016, hiss=0.03, lowpass=3000, drift=0.007, drive=1.6)
    tr.save("music_unease_high", 0.32)                                    # kept quiet: unsettling, never loud


def loop_sequence():
    beat = 60.0 / 76.0; bars = 48; tr = Track(bars * 4 * beat, 6)         # 2 min 32 s; the same hallway, again and again
    cell = ["A3", "E4", "C4", "E4", "A3", "E4", "D4", "E4"]               # one bar of eighth notes
    for b in range(bars):
        c = list(cell)
        if b % 8 == 5: c[6] = "Eb4"                                       # every eighth pass, one thing is different
        if b % 16 == 11: c[2] = "B3"
        if b % 24 == 20: c[0] = "G#3"
        for k, nt in enumerate(c):
            tr.piano(n(nt), b * 4 * beat + k * beat * 0.5, 0.34 if k % 2 == 0 else 0.26, 2.2, cents=-12, soft=1.5)
        tr.thump(b * 4 * beat, 0.16); tr.thump(b * 4 * beat + 2 * beat, 0.11)             # footsteps
        if b % 4 == 0:
            tr.pad([n("A2"), n("E3"), n("C4") if (b // 4) % 3 else n("B3")], b * 4 * beat, 15 * beat, 0.08, bright=0.4)
        if b % 8 == 7:
            tr.box(n("E6"), b * 4 * beat + 3 * beat, 0.06)
    tr.drone([n("A1")], 0.16, beat=0.26)
    tr.reverb(2.2, 0.34, dark=3000); tr.tape(wow=0.0022, flutter=0.0005, hiss=0.02, lowpass=4600, drift=0.0012)
    tr.save("music_loop_sequence", 0.48)


TRACKS = {"music_title": title, "music_day1_calm": day1_calm, "music_unease_low": unease_low, "music_unease_mid": unease_mid,
          "music_unease_high": unease_high, "music_loop_sequence": loop_sequence}
if __name__ == "__main__":
    for k in (sys.argv[1:] or list(TRACKS)):
        TRACKS[k]()
