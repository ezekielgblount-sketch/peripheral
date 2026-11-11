#!/usr/bin/env python3
"""One still of each loop anomaly (shown in the editor just for the picture) -> screenshots/loop/."""
import sys, os, subprocess
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(os.path.dirname(here), "screenshots", "loop")
SHOTS = [(0, "0_door_that_was_never_there", "200,1440,165:345,1251,105"), (1, "1_family_photo_child_gone", "230,780,160:215,601,150"),
         (2, "2_banner_misspelled", "400,708,140:573,708,120"), (3, "3_hall_clock", "385,1400,170:385,1251,178"),
         (4, "4_chair_facing_the_wall", "330,800,150:200,640,60"), (5, "5_television_on", "250,840,130:250,1012,90"), (-1, "start_of_each_pass", "200,1440,165:520,1400,120")]
def ue(code):
    subprocess.run([sys.executable, os.path.join(here, "uepy.py"), "-c", code, "300"], check=True, stdout=subprocess.DEVNULL)
SHOW = """
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    tags = [str(t) for t in a.tags]
    for i in range(6):
        if "an%%d" %% i in tags: a.set_is_temporarily_hidden_in_editor(i != %d); a.set_actor_hidden_in_game(i != %d)
        if "an%%dn" %% i in tags: a.set_is_temporarily_hidden_in_editor(i == %d)
"""
first = True
for k, name, pov in SHOTS:
    ue(SHOW % (k, k, k))
    subprocess.run([sys.executable, os.path.join(here, "shot.py"), out, "%s:%s" % (name, pov)], check=True, env=dict(os.environ, SHOT_WARMUP="120" if first else "6", SHOT_TICKS="16"), stdout=subprocess.DEVNULL); first = False
ue(SHOW % (-1, -1, -1)); print("done", len(os.listdir(out)))
