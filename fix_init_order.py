from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old_state = "orientationBlocked=false,pendingLandscapeStart=false;"
new_state = "orientationBlocked=false,pendingLandscapeStart=false,joyPointer=null,joyUp=false;"
if old_state not in s:
    raise SystemExit('global state anchor not found')
s = s.replace(old_state, new_state, 1)

late_state = "let joyPointer=null,joyUp=false;"
if late_state not in s:
    raise SystemExit('late joystick state declaration not found')
s = s.replace(late_state, "// joystick state is initialized before the first resize() call", 1)

ready_anchor = "setSkin(p.skin,true);syncWeaponSlots();"
if ready_anchor not in s:
    raise SystemExit('ready marker anchor not found')
s = s.replace(ready_anchor, ready_anchor + "document.documentElement.dataset.brainFeastReady='1';", 1)

path.write_text(s, encoding='utf-8')
print('Initialization order fixed')
