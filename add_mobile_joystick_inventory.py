from pathlib import Path
import re

path = Path('index.html')
s = path.read_text()


def rep(old: str, new: str, label: str) -> None:
    global s
    if old not in s:
        raise SystemExit(f'{label}: source not found')
    s = s.replace(old, new, 1)

# Replace the old button-based mobile control CSS with joystick/action controls.
old_controls_css = (
    ".controls{position:absolute;left:max(10px,env(safe-area-inset-left));right:max(10px,env(safe-area-inset-right));bottom:max(10px,env(safe-area-inset-bottom));display:flex;justify-content:space-between;align-items:end;z-index:6;pointer-events:none}"
    ".cluster{display:flex;gap:9px;pointer-events:auto}"
    ".ctrl{width:clamp(58px,16vw,86px);height:clamp(58px,16vw,86px);border-radius:23px;border:2px solid #a72b4d;background:#25131ddd;color:#fff;font-size:clamp(25px,7vw,38px);font-weight:1000;box-shadow:0 6px 0 #4b0b20;touch-action:none;user-select:none}"
    ".ctrl.active{transform:translateY(4px);box-shadow:0 2px 0 #4b0b20;background:#8f1b40}"
)
new_controls_css = (
    ".controls{position:absolute;left:max(12px,env(safe-area-inset-left));right:max(12px,env(safe-area-inset-right));bottom:max(12px,env(safe-area-inset-bottom));display:flex;justify-content:space-between;align-items:end;z-index:6;pointer-events:none}"
    ".joystick{position:relative;width:clamp(112px,29vw,142px);height:clamp(112px,29vw,142px);border-radius:50%;border:2px solid #f3cf20;background:radial-gradient(circle,#3a300dcc 0 34%,#211907cc 36% 65%,#100c05bb 67%);box-shadow:0 0 22px #ffd90040,inset 0 0 20px #0008;pointer-events:auto;touch-action:none;user-select:none}"
    ".joystick:before,.joystick:after{content:'';position:absolute;background:#ffe34b55;pointer-events:none}.joystick:before{left:50%;top:13%;bottom:13%;width:2px;transform:translateX(-50%)}.joystick:after{top:50%;left:13%;right:13%;height:2px;transform:translateY(-50%)}"
    ".joy-knob{position:absolute;left:50%;top:50%;width:45%;height:45%;border-radius:50%;transform:translate(-50%,-50%);background:radial-gradient(circle at 35% 30%,#fff4a0,#e2ad00 65%,#6e4b00);border:2px solid #fff1a1;box-shadow:0 5px 0 #795400,0 0 16px #ffd90066;pointer-events:none;will-change:transform}"
    ".actions{display:flex;flex-direction:column;align-items:flex-end;gap:10px;pointer-events:auto}"
    ".action-btn{border:2px solid #f3cf20;border-radius:50%;background:#2a220be8;color:#fff5a6;font-weight:1000;box-shadow:0 6px 0 #806000;touch-action:none;user-select:none}"
    ".action-btn.active{transform:translateY(4px);box-shadow:0 2px 0 #806000;background:#9c7600;color:#fff}"
    "#jumpBtn{width:clamp(62px,16vw,78px);height:clamp(62px,16vw,78px);font-size:clamp(26px,7vw,38px);margin-right:15px}"
    "#fireBtn{width:clamp(88px,23vw,110px);height:clamp(88px,23vw,110px);font-size:clamp(34px,10vw,50px)}"
    ".weapon-dock{position:absolute;top:calc(env(safe-area-inset-top) + 54px);right:max(8px,env(safe-area-inset-right));display:flex;gap:5px;z-index:7;pointer-events:auto}"
    ".weapon-slot{min-width:43px;height:46px;padding:3px 5px;border:2px solid #b99200;border-radius:12px;background:#211907e8;color:#fff2a3;font-size:14px;font-weight:1000;line-height:1;box-shadow:0 3px 0 #715000;touch-action:manipulation}"
    ".weapon-slot .slot-icon{display:block;font-size:18px}.weapon-slot .ammo{display:block;margin-top:2px;font-size:10px;font-weight:900}"
    ".weapon-slot.active{border-color:#fff7a6;background:#ae8200;color:#1e1600;transform:translateY(2px);box-shadow:0 1px 0 #715000}"
    ".weapon-slot.locked{opacity:.34;filter:grayscale(1)}"
)
rep(old_controls_css, new_controls_css, 'mobile controls css')

# Replace old responsive rules that referred to .ctrl/.cluster.
rep(
    "@media(max-width:370px){.ctrl{width:52px;height:52px;font-size:24px}.cluster{gap:6px}.pill{padding:6px 9px;font-size:11px}}@media (pointer:fine){.controls{opacity:.5}.ctrl{width:62px;height:62px;font-size:28px}.hint{bottom:78px}}@media (orientation:landscape) and (max-height:520px){.hud{top:5px}.pill{padding:5px 9px}.controls{bottom:5px}.ctrl{width:56px;height:56px;border-radius:17px}.hint{display:none}.card{padding:14px}.help{margin:8px auto}.title{font-size:46px}.sub{font-size:14px}}",
    "@media(max-width:370px){.joystick{width:102px;height:102px}.weapon-slot{min-width:39px;height:42px;padding:2px 4px}.weapon-slot .slot-icon{font-size:16px}.pill{padding:6px 9px;font-size:11px}}@media (pointer:fine){.controls{display:none}.hint{bottom:78px}}@media (orientation:landscape) and (max-height:520px){.hud{top:5px}.pill{padding:5px 9px}.controls{bottom:5px}.joystick{width:94px;height:94px}#jumpBtn{width:54px;height:54px;font-size:24px}#fireBtn{width:72px;height:72px;font-size:32px}.weapon-dock{top:45px}.weapon-slot{height:40px;min-width:39px}.hint{display:none}.card{padding:14px}.help{margin:8px auto}.title{font-size:46px}.sub{font-size:14px}}",
    'responsive controls css',
)

# Remove leftover .ctrl theme overrides.
s = s.replace(".ctrl{border-color:#f3cf20;background:#2a220bdd;box-shadow:0 6px 0 #806000;color:#fff5a6}\n.ctrl.active{box-shadow:0 2px 0 #806000;background:#9c7600;color:#fff}\n", "", 1)

new_controls_html = (
    '<div class="weapon-dock" id="weaponDock">'
    '<button class="weapon-slot active" data-weapon="thunder" aria-label="Donnerblitz"><span class="slot-icon">1⚡</span><span class="ammo">∞</span></button>'
    '<button class="weapon-slot locked" data-weapon="storm" aria-label="Himmelszorn"><span class="slot-icon">2🌩️</span><span class="ammo">—</span></button>'
    '<button class="weapon-slot locked" data-weapon="skull" aria-label="Schädelwerfer"><span class="slot-icon">3☠️</span><span class="ammo">—</span></button>'
    '<button class="weapon-slot locked" data-weapon="saw" aria-label="Volt-Säge"><span class="slot-icon">4🪚</span><span class="ammo">—</span></button>'
    '</div>'
    '<div class="controls">'
    '<div class="joystick" id="joystick" aria-label="Bewegungs-Joystick"><div class="joy-knob" id="joyKnob"></div></div>'
    '<div class="actions"><button class="action-btn" id="jumpBtn" data-key="up" aria-label="Springen">▲</button><button class="action-btn" id="fireBtn" data-key="shoot" aria-label="Feuern">⚡</button></div>'
    '</div>'
)
s, n = re.subn(r'<div class="controls">\s*<div class="cluster"><button class="ctrl" data-key="left">◀</button><button class="ctrl" data-key="right">▶</button></div>\s*<div class="cluster"><button class="ctrl" data-key="shoot">💥</button><button class="ctrl" data-key="down">▼</button><button class="ctrl" data-key="up">▲</button></div>\s*</div>', new_controls_html, s, count=1)
if n != 1:
    raise SystemExit(f'controls html: expected 1, got {n}')

# Update onboarding text.
s = s.replace('📱 Tippe ins Spielfeld, um gezielt dorthin zu springen.<br>◀ ▶ bewegen · ▲ kurz = kleiner Sprung · ▲ halten = hoher Sprung · ▼ ducken<br>', '📱 Links: Joystick zum Laufen, Springen und Ducken.<br>👉 Rechts: großer Feuerknopf und zusätzlicher Sprungknopf.<br>', 1)
s = s.replace('🎁 Himmelszorn, Schädelwerfer und Volt-Säge haben jeweils 50 Schuss.<br>', '🎁 Waffen landen im Inventar. Oben rechts wechselst du zwischen Slot 1–4.<br>', 1)

# DOM references.
rep(
    "const start=$('start'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),hint=$('hint');",
    "const start=$('start'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),hint=$('hint'),joystick=$('joystick'),joyKnob=$('joyKnob'),fireBtn=$('fireBtn'),jumpBtn=$('jumpBtn');",
    'dom refs',
)

# Add inventory and joystick state after weapon names.
rep(
    "const weaponNames={thunder:'⚡ Donnerblitz',storm:'🌩️ Himmelszorn',skull:'☠️ Schädelwerfer',saw:'🪚 Volt-Säge'};",
    "const weaponNames={thunder:'⚡ Donnerblitz',storm:'🌩️ Himmelszorn',skull:'☠️ Schädelwerfer',saw:'🪚 Volt-Säge'};\nconst weaponInventory={thunder:Infinity,storm:0,skull:0,saw:0};\nconst weaponOrder=['thunder','storm','skull','saw'];\nlet joyPointer=null,joyUp=false;",
    'inventory state',
)

# Reset inventory each new run while preserving selected skin.
rep(
    "function reset(){t=worldX=bossClock=bossCount=score=clock=0;speed=330;spawn=.7;pickClock=1.2;objects=[];pickups=[];shots=[];bossShots=[];laser=null;boss=null;particles=[];target=null;Object.assign(p,{x:Math.min(120,W*.18),y:G-70,w:58,h:70,vx:0,vy:0,on:true,duck:false,lives:3,inv:0,hold:0,weapon:'thunder',ammo:Infinity,cool:0,earthGuard:0});hud()}",
    "function reset(){t=worldX=bossClock=bossCount=score=clock=0;speed=330;spawn=.7;pickClock=1.2;objects=[];pickups=[];shots=[];bossShots=[];laser=null;boss=null;particles=[];target=null;weaponInventory.thunder=Infinity;weaponInventory.storm=weaponInventory.skull=weaponInventory.saw=0;resetJoy();Object.assign(p,{x:Math.min(120,W*.18),y:G-70,w:58,h:70,vx:0,vy:0,on:true,duck:false,lives:3,inv:0,hold:0,weapon:'thunder',ammo:Infinity,cool:0,earthGuard:0});hud()}",
    'reset inventory',
)

old_weapon_logic = (
    "function hud(){scoreEl.textContent='Punkte '+Math.floor(score).toLocaleString('de-DE');weaponEl.textContent=weaponNames[p.weapon]+(p.weapon==='thunder'?' ∞':' '+p.ammo);livesEl.textContent='❤️'.repeat(Math.max(0,p.lives))+'☠️'.repeat(Math.max(0,3-p.lives))}\n"
    "function togglePause(force){if(!running||!start.classList.contains('hidden')||!over.classList.contains('hidden'))return;paused=force===undefined?!paused:!!force;pauseMenu.classList.toggle('hidden',!paused);if(paused){Object.keys(key).forEach(k=>key[k]=false);document.querySelectorAll('.ctrl').forEach(el=>el.classList.remove('active'));syncSkinButtons();hint.textContent='PAUSE · Skin wählen oder P drücken';hint.style.opacity='1'}else{hint.style.opacity='.15'}}\n"
    "function equipWeapon(kind){p.weapon=kind;p.ammo=50;hint.textContent=weaponNames[kind]+' eingesammelt · 50 Schuss';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},1800);tone(kind==='storm'?980:kind==='skull'?180:520,.08,kind==='skull'?'sawtooth':'square',.018);hud()}\n"
    "function spendAmmo(){if(p.weapon==='thunder')return;p.ammo--;if(p.ammo<=0){p.weapon='thunder';p.ammo=Infinity;hint.textContent='Spezialwaffe leer · zurück zum Donnerblitz';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},1500)}hud()}"
)
new_weapon_logic = (
    "function syncWeaponSlots(){document.querySelectorAll('[data-weapon]').forEach(btn=>{let kind=btn.dataset.weapon,amount=weaponInventory[kind],locked=kind!=='thunder'&&amount<=0;btn.classList.toggle('locked',locked);btn.classList.toggle('active',p.weapon===kind);let ammo=btn.querySelector('.ammo');if(ammo)ammo.textContent=kind==='thunder'?'∞':amount>0?amount:'—'})}\n"
    "function hud(){let amount=weaponInventory[p.weapon];p.ammo=amount;scoreEl.textContent='Punkte '+Math.floor(score).toLocaleString('de-DE');weaponEl.textContent=weaponNames[p.weapon]+(p.weapon==='thunder'?' ∞':' '+amount);livesEl.textContent='❤️'.repeat(Math.max(0,p.lives))+'☠️'.repeat(Math.max(0,3-p.lives));syncWeaponSlots()}\n"
    "function selectWeapon(kind,silent=false){if(!weaponNames[kind])return false;if(kind!=='thunder'&&weaponInventory[kind]<=0){if(!silent){hint.textContent=weaponNames[kind]+' noch nicht eingesammelt';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},1100)}return false}p.weapon=kind;p.ammo=weaponInventory[kind];if(!silent){hint.textContent=weaponNames[kind]+' ausgewählt';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},900)}hud();return true}\n"
    "function togglePause(force){if(!running||!start.classList.contains('hidden')||!over.classList.contains('hidden'))return;paused=force===undefined?!paused:!!force;pauseMenu.classList.toggle('hidden',!paused);if(paused){resetJoy();Object.keys(key).forEach(k=>key[k]=false);document.querySelectorAll('.action-btn').forEach(el=>el.classList.remove('active'));syncSkinButtons();hint.textContent='PAUSE · Skin wählen oder P drücken';hint.style.opacity='1'}else{hint.style.opacity='.15'}}\n"
    "function equipWeapon(kind){if(!weaponInventory.hasOwnProperty(kind)||kind==='thunder')return;weaponInventory[kind]=50;hint.textContent=weaponNames[kind]+' eingesammelt · Slot '+(weaponOrder.indexOf(kind)+1)+' bereit';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},1800);tone(kind==='storm'?980:kind==='skull'?180:520,.08,kind==='skull'?'sawtooth':'square',.018);hud()}\n"
    "function spendAmmo(){if(p.weapon==='thunder')return;let kind=p.weapon;weaponInventory[kind]=Math.max(0,weaponInventory[kind]-1);p.ammo=weaponInventory[kind];if(weaponInventory[kind]<=0){p.weapon='thunder';p.ammo=Infinity;hint.textContent=weaponNames[kind]+' leer · zurück zum Donnerblitz';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},1500)}hud()}"
)
rep(old_weapon_logic, new_weapon_logic, 'weapon inventory logic')

old_bindings = (
    "function bindButton(b){let n=b.dataset.key;b.addEventListener('pointerdown',e=>{e.preventDefault();b.setPointerCapture?.(e.pointerId);control(n,true)});['pointerup','pointercancel','lostpointercapture'].forEach(ev=>b.addEventListener(ev,e=>{e.preventDefault();control(n,false)}))}document.querySelectorAll('.ctrl').forEach(bindButton);document.querySelectorAll('[data-skin]').forEach(btn=>btn.addEventListener('click',e=>{e.preventDefault();setSkin(btn.dataset.skin)}));setSkin(p.skin,true);\n"
    "addEventListener('keydown',e=>{if(e.code==='KeyP'){e.preventDefault();if(!e.repeat)togglePause();return}let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m&&!paused){e.preventDefault();if(!e.repeat)control(m,true)}});addEventListener('keyup',e=>{if(e.code==='KeyP'){e.preventDefault();return}let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m){e.preventDefault();control(m,false)}});addEventListener('blur',()=>Object.keys(key).forEach(k=>control(k,false)));"
)
new_bindings = (
    "function applyJoy(nx,ny){let left=nx<-.22,right=nx>.22,up=ny<-.47,down=ny>.5;if(key.left!==left)control('left',left);if(key.right!==right)control('right',right);if(up&&!joyUp){control('up',true);joyUp=true}else if(!up&&joyUp){control('up',false);joyUp=false}if(key.down!==down)control('down',down)}\n"
    "function moveJoy(e){let r=joystick.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,dx=e.clientX-cx,dy=e.clientY-cy,max=r.width*.31,dist=Math.hypot(dx,dy)||1;if(dist>max){dx=dx/dist*max;dy=dy/dist*max}joyKnob.style.transform='translate(calc(-50% + '+dx+'px),calc(-50% + '+dy+'px))';applyJoy(dx/max,dy/max)}\n"
    "function resetJoy(){joyPointer=null;joyUp=false;if(joyKnob)joyKnob.style.transform='translate(-50%,-50%)';if(key.left)control('left',false);if(key.right)control('right',false);if(key.up)control('up',false);if(key.down)control('down',false)}\n"
    "joystick.addEventListener('pointerdown',e=>{e.preventDefault();joyPointer=e.pointerId;try{joystick.setPointerCapture?.(e.pointerId)}catch(_){}moveJoy(e)});joystick.addEventListener('pointermove',e=>{if(e.pointerId===joyPointer){e.preventDefault();moveJoy(e)}});['pointerup','pointercancel','lostpointercapture'].forEach(ev=>joystick.addEventListener(ev,e=>{if(joyPointer===null||e.pointerId===joyPointer){e.preventDefault();resetJoy()}}));\n"
    "function bindAction(btn,name){let stop=e=>{e.preventDefault();control(name,false)};btn.addEventListener('pointerdown',e=>{e.preventDefault();try{btn.setPointerCapture?.(e.pointerId)}catch(_){}control(name,true)});['pointerup','pointercancel','lostpointercapture'].forEach(ev=>btn.addEventListener(ev,stop))}bindAction(fireBtn,'shoot');bindAction(jumpBtn,'up');\n"
    "document.querySelectorAll('[data-skin]').forEach(btn=>btn.addEventListener('click',e=>{e.preventDefault();setSkin(btn.dataset.skin)}));document.querySelectorAll('[data-weapon]').forEach(btn=>btn.addEventListener('click',e=>{e.preventDefault();selectWeapon(btn.dataset.weapon)}));setSkin(p.skin,true);syncWeaponSlots();\n"
    "addEventListener('keydown',e=>{if(e.code==='KeyP'){e.preventDefault();if(!e.repeat)togglePause();return}let weapon={Digit1:'thunder',Digit2:'storm',Digit3:'skull',Digit4:'saw'}[e.code];if(weapon&&!e.repeat){e.preventDefault();selectWeapon(weapon);return}let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m&&!paused){e.preventDefault();if(!e.repeat)control(m,true)}});addEventListener('keyup',e=>{if(e.code==='KeyP'||e.code.startsWith('Digit')){e.preventDefault();return}let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m){e.preventDefault();control(m,false)}});addEventListener('blur',()=>{resetJoy();Object.keys(key).forEach(k=>control(k,false))});"
)
rep(old_bindings, new_bindings, 'joystick bindings')

rep(
    "let bw=Math.min(W*.72,560),bh=18,bx=(W-bw)/2,by=Math.max(66,H*.11);",
    "let bw=Math.min(W*.72,560),bh=18,bx=(W-bw)/2,by=lowPower?Math.max(112,H*.15):Math.max(66,H*.11);",
    'boss bar position',
)

path.write_text(s)
print('Mobile joystick and weapon inventory added.')
