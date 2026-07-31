from pathlib import Path
import re

path = Path('index.html')
s = path.read_text()


def rep(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'{label}: source not found')
    s = s.replace(old, new, 1)


def sub(pattern, replacement, label, count=1):
    global s
    s, n = re.subn(pattern, replacement, s, count=count, flags=re.S)
    if n != count:
        raise SystemExit(f'{label}: expected {count}, got {n}')

# UI / CSS
rep(
    '#sound{pointer-events:auto;border:0;color:#fff;min-width:44px}',
    '#sound,#pauseBtn{pointer-events:auto;border:0;color:#fff;min-width:44px}',
    'pause button pointer events',
)
rep(
    '#weapon,#sound{color:#ffe545}',
    '#weapon,#sound,#pauseBtn{color:#ffe545}',
    'pause button color',
)
rep(
    '.hint{background:#211a08e8;border:1px solid #c99c00;color:#fff2a3}\n</style>',
    '.hint{background:#211a08e8;border:1px solid #c99c00;color:#fff2a3}'
    '.skin-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:14px 0 18px}'
    '.skin-btn{border:2px solid #d5ae17;border-radius:17px;padding:12px 10px;background:#2a210ae8;color:#fff7bd;font-weight:950;font-size:clamp(13px,3.2vw,17px);box-shadow:0 4px 0 #7f6100;touch-action:manipulation}'
    '.skin-btn.active{background:#d3a500;color:#211700;transform:translateY(2px);box-shadow:0 2px 0 #7f6100}'
    '.skin-note{display:block;font-size:11px;line-height:1.25;font-weight:750;opacity:.86;margin-top:4px}'
    '@media(max-width:520px){.skin-grid{grid-template-columns:1fr;gap:7px}.skin-btn{padding:9px 8px}}\n</style>',
    'skin css',
)
rep(
    '<div class="hud"><span class="pill" id="score">Punkte 0</span><span class="pill" id="weapon">⚡ Donnerblitz ∞</span><span class="pill" id="lives">❤️❤️❤️</span><button class="pill" id="sound">🔊</button></div>',
    '<div class="hud"><span class="pill" id="score">Punkte 0</span><span class="pill" id="weapon">⚡ Donnerblitz ∞</span><span class="pill" id="lives">❤️❤️❤️</span><button class="pill" id="sound">🔊</button><button class="pill" id="pauseBtn">⏸</button></div>',
    'hud pause button',
)
rep(
    '<div class="hint" id="hint">Unendlicher Donnerblitz · 💥 feuern · F auf Tastatur</div>',
    '<div class="hint" id="hint">Donnerblitz ∞ · 💥/F feuern · P pausiert</div>',
    'hint text',
)

start_skin_grid = '''<div class="skin-grid">
<button class="skin-btn active" data-skin="electric">⚡ Blitzschildkröte<span class="skin-note">16 % schneller feuern</span></button>
<button class="skin-btn" data-skin="water">💧 Wasserschildkröte<span class="skin-note">1,8 Sekunden Schutz nach Treffern</span></button>
<button class="skin-btn" data-skin="air">🌪️ Luftschildkröte<span class="skin-note">20 % schneller · 10 % höher springen</span></button>
<button class="skin-btn" data-skin="earth">🌿 Erdschildkröte<span class="skin-note">Jeder 3. Treffer wird geblockt · etwas langsamer</span></button>
</div>'''

s = s.replace('als Pikachu', 'als Blitzschildkröte', 1)
rep(
    'Gelbe Linien warnen vor tödlichen Blitzwänden.</div><button class="primary" id="play">JETZT SPIELEN</button>',
    'Gelbe Linien warnen vor tödlichen Blitzwänden.<br>⌨️ P oder ⏸ öffnet die Pause.</div>' + start_skin_grid + '<button class="primary" id="play">JETZT SPIELEN</button>',
    'start skin selector',
)

pause_overlay = '''<div class="overlay hidden" id="pause">
 <div class="card"><div class="badge">PAUSE</div><h2 class="title" style="font-size:clamp(34px,8vw,62px)">Spiel pausiert</h2><p class="sub">Wähle deine Element-Schildkröte. Die Welt bleibt vollständig stehen.</p>
 <div class="skin-grid">
 <button class="skin-btn active" data-skin="electric">⚡ Blitzschildkröte<span class="skin-note">16 % schneller feuern</span></button>
 <button class="skin-btn" data-skin="water">💧 Wasserschildkröte<span class="skin-note">1,8 Sekunden Schutz nach Treffern</span></button>
 <button class="skin-btn" data-skin="air">🌪️ Luftschildkröte<span class="skin-note">20 % schneller · 10 % höher springen</span></button>
 <button class="skin-btn" data-skin="earth">🌿 Erdschildkröte<span class="skin-note">Jeder 3. Treffer wird geblockt · etwas langsamer</span></button>
 </div><button class="primary" id="resumeBtn">WEITER</button></div>
</div>
'''
rep('</div>\n<script>\n(()=>{\'use strict\';', '</div>\n' + pause_overlay + '<script>\n(()=>{\'use strict\';', 'pause overlay')

# State / skin definitions
rep(
    "const start=$('start'),over=$('over'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),hint=$('hint');",
    "const start=$('start'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),hint=$('hint');",
    'dom refs',
)
rep(
    "let W=0,H=0,G=0,dpr=1,running=false,last=performance.now(),t=0,worldX=0,bossClock=0,bossCount=0,score=0,clock=0,speed=330,spawn=1,pickClock=1.4,objects=[],pickups=[],shots=[],bossShots=[],laser=null,boss=null,particles=[],high=+(localStorage.brainFeastHigh||0),audio=true,ac=null,target=null,bg=null,shotSoundAt=0,lowPower=matchMedia('(pointer:coarse)').matches;",
    "let W=0,H=0,G=0,dpr=1,running=false,last=performance.now(),t=0,worldX=0,bossClock=0,bossCount=0,score=0,clock=0,speed=330,spawn=1,pickClock=1.4,objects=[],pickups=[],shots=[],bossShots=[],laser=null,boss=null,particles=[],high=+(localStorage.brainFeastHigh||0),audio=true,ac=null,target=null,bg=null,shotSoundAt=0,lowPower=matchMedia('(pointer:coarse)').matches,paused=false;",
    'paused global',
)
rep(
    "const p={x:120,y:0,w:58,h:70,vx:0,vy:0,on:true,duck:false,lives:3,inv:0,hold:0,weapon:'thunder',ammo:Infinity,cool:0};",
    "const savedSkin=(()=>{try{return localStorage.brainFeastSkin||'electric'}catch(e){return'electric'}})();\n"
    "const p={x:120,y:0,w:58,h:70,vx:0,vy:0,on:true,duck:false,lives:3,inv:0,hold:0,weapon:'thunder',ammo:Infinity,cool:0,skin:savedSkin,earthGuard:0};\n"
    "const skinDefs={"
    "electric:{label:'⚡ Blitzschildkröte',speed:1,jump:1,fire:.84,inv:1.15,body:'#ffd83b',shell:'#936d00',shell2:'#604600',accent:'#fff4a6',mark:'#6e5100'},"
    "water:{label:'💧 Wasserschildkröte',speed:1,jump:1,fire:1,inv:1.8,body:'#69d7ff',shell:'#1477a4',shell2:'#0c4e70',accent:'#e2faff',mark:'#08364e'},"
    "air:{label:'🌪️ Luftschildkröte',speed:1.2,jump:1.1,fire:1,inv:1.15,body:'#f4fbff',shell:'#c6d9e4',shell2:'#8fa8b7',accent:'#83d9ff',mark:'#6d8999'},"
    "earth:{label:'🌿 Erdschildkröte',speed:.9,jump:.94,fire:1.06,inv:1.25,body:'#9dca73',shell:'#705738',shell2:'#493821',accent:'#d9efae',mark:'#30451f'}"
    "};\n"
    "function syncSkinButtons(){document.querySelectorAll('[data-skin]').forEach(b=>b.classList.toggle('active',b.dataset.skin===p.skin))}\n"
    "function setSkin(kind,silent=false){if(!skinDefs[kind])kind='electric';p.skin=kind;p.earthGuard=0;try{localStorage.brainFeastSkin=kind}catch(e){}syncSkinButtons();if(!silent){hint.textContent=skinDefs[kind].label+' aktiviert';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},1500)}hud()}",
    'skin definitions',
)

# Pause lifecycle
rep(
    "function begin(){reset();running=true;start.classList.add('hidden');over.classList.add('hidden');hint.style.opacity='1';setTimeout(()=>hint.style.opacity='.15',3500);tone(220,.12,'sawtooth')}",
    "function begin(){reset();paused=false;running=true;pauseMenu.classList.add('hidden');start.classList.add('hidden');over.classList.add('hidden');hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},3500);tone(220,.12,'sawtooth')}",
    'begin pause reset',
)
rep(
    "function end(){if(!running)return;running=false;high=Math.max(high,Math.floor(score));localStorage.brainFeastHigh=high;result.textContent=`Punkte: ${Math.floor(score).toLocaleString('de-DE')} · Highscore: ${high.toLocaleString('de-DE')}`;over.classList.remove('hidden');tone(120,.35,'sawtooth',.04)}",
    "function end(){if(!running)return;running=false;paused=false;pauseMenu.classList.add('hidden');high=Math.max(high,Math.floor(score));try{localStorage.brainFeastHigh=high}catch(e){}result.textContent=`Punkte: ${Math.floor(score).toLocaleString('de-DE')} · Highscore: ${high.toLocaleString('de-DE')}`;over.classList.remove('hidden');tone(120,.35,'sawtooth',.04)}",
    'end pause reset',
)

sub(
    r"function hud\(\)\{.*?\}\nfunction equipWeapon",
    "function hud(){scoreEl.textContent='Punkte '+Math.floor(score).toLocaleString('de-DE');weaponEl.textContent=weaponNames[p.weapon]+(p.weapon==='thunder'?' ∞':' '+p.ammo);livesEl.textContent='❤️'.repeat(Math.max(0,p.lives))+'☠️'.repeat(Math.max(0,3-p.lives))}\n"
    "function togglePause(force){if(!running||!start.classList.contains('hidden')||!over.classList.contains('hidden'))return;paused=force===undefined?!paused:!!force;pauseMenu.classList.toggle('hidden',!paused);if(paused){Object.keys(key).forEach(k=>key[k]=false);document.querySelectorAll('.ctrl').forEach(b=>b.classList.remove('active'));syncSkinButtons();hint.textContent='PAUSE · Skin wählen oder P drücken';hint.style.opacity='1'}else{hint.style.opacity='.15'}}\n"
    "function equipWeapon",
    'hud and pause function',
)

# Skin abilities
rep(
    "function jump(force=1){if(!running||!p.on)return;p.on=false;p.vy=-Math.max(520,H*.78)*force;p.hold=0;tone(420,.08,'sine')}",
    "function jump(force=1){if(!running||paused||!p.on)return;let st=skinDefs[p.skin]||skinDefs.electric;p.on=false;p.vy=-Math.max(520,H*.78)*force*st.jump;p.hold=0;tone(420,.08,'sine')}",
    'air jump ability',
)

sub(
    r"function hurt\(\)\{.*?\}\nfunction burst",
    "function hurt(){if(p.inv>0)return;let st=skinDefs[p.skin]||skinDefs.electric;if(p.skin==='earth'){p.earthGuard++;if(p.earthGuard>=3){p.earthGuard=0;p.inv=.45;hint.textContent='🌿 Steinpanzer blockt den Treffer!';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},900);sparks(p.x+p.w/2,p.y+p.h/2,4);tone(110,.07,'square',.02);return}}p.lives--;p.inv=st.inv;p.vy=-330;p.on=false;burst(p.x+p.w/2,p.y+p.h/2);tone(150,.18,'sawtooth',.045);hud();if(p.lives<=0)setTimeout(end,220)}\nfunction burst",
    'defense abilities',
)

# Add fire-rate modifier after weapon-specific cooldown has been selected.
rep(
    "if(t>=shotSoundAt){let f=p.weapon==='storm'?1040:p.weapon==='skull'?170:p.weapon==='saw'?480:880;",
    "p.cool*=((skinDefs[p.skin]||skinDefs.electric).fire);if(t>=shotSoundAt){let f=p.weapon==='storm'?1040:p.weapon==='skull'?170:p.weapon==='saw'?480:880;",
    'electric fire ability',
)

rep(
    "let accel=1350,max=330,dir=(key.right?1:0)-(key.left?1:0);",
    "let st=skinDefs[p.skin]||skinDefs.electric,accel=1350*st.speed,max=330*st.speed,dir=(key.right?1:0)-(key.left?1:0);",
    'movement ability',
)

# Input / controls
rep(
    "addEventListener('keydown',e=>{let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m){e.preventDefault();if(!e.repeat)control(m,true)}});addEventListener('keyup',e=>{let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m){e.preventDefault();control(m,false)}});addEventListener('blur',()=>Object.keys(key).forEach(k=>control(k,false)));",
    "addEventListener('keydown',e=>{if(e.code==='KeyP'){e.preventDefault();if(!e.repeat)togglePause();return}let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m&&!paused){e.preventDefault();if(!e.repeat)control(m,true)}});addEventListener('keyup',e=>{if(e.code==='KeyP'){e.preventDefault();return}let m={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',Space:'up',KeyF:'shoot',KeyX:'shoot'}[e.code];if(m){e.preventDefault();control(m,false)}});addEventListener('blur',()=>Object.keys(key).forEach(k=>control(k,false)));",
    'keyboard pause',
)
rep(
    "function robust(btn,fn){let done=false,fire=e=>{e.preventDefault();if(done)return;done=true;fn();setTimeout(()=>done=false,350)};btn.addEventListener('pointerup',fire);btn.addEventListener('touchend',fire,{passive:false});btn.addEventListener('click',fire)}robust($('play'),begin);robust($('again'),begin);soundBtn.onclick=e=>{e.preventDefault();audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()};",
    "function robust(btn,fn){let done=false,fire=e=>{e.preventDefault();if(done)return;done=true;fn();setTimeout(()=>done=false,350)};btn.addEventListener('pointerup',fire);btn.addEventListener('touchend',fire,{passive:false});btn.addEventListener('click',fire)}robust($('play'),begin);robust($('again'),begin);robust($('resumeBtn'),()=>togglePause(false));soundBtn.onclick=e=>{e.preventDefault();audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()};pauseBtn.onclick=e=>{e.preventDefault();togglePause()};document.querySelectorAll('[data-skin]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();setSkin(b.dataset.skin)}));setSkin(p.skin,true);",
    'skin and pause bindings',
)

# Replace Pikachu drawing with a lightweight elemental turtle.
turtle_draw = """function drawPlayer(){if(p.inv>0&&Math.floor(t*18)%2===0)return;let h=p.duck?p.h*.62:p.h,yy=p.y+p.h-h,bob=p.on?Math.sin(t*10)*1.5:0,st=skinDefs[p.skin]||skinDefs.electric,cx=p.x+p.w*.5,cy=yy+h*.54+bob;x.save();x.translate(cx,cy);x.fillStyle=st.shell;x.beginPath();x.ellipse(0,0,p.w*.29,h*.23,0,0,7);x.fill();x.fillStyle=st.shell2;x.beginPath();x.ellipse(0,0,p.w*.205,h*.16,0,0,7);x.fill();x.strokeStyle=st.mark;x.lineWidth=2;x.beginPath();x.moveTo(-p.w*.12,-h*.04);x.lineTo(p.w*.12,-h*.04);x.moveTo(-p.w*.12,h*.045);x.lineTo(p.w*.12,h*.045);x.moveTo(0,-h*.13);x.lineTo(0,h*.13);x.stroke();x.fillStyle=st.body;x.beginPath();x.arc(p.w*.235,-h*.035,h*.115,0,7);x.fill();x.fillStyle='#111';x.beginPath();x.arc(p.w*.275,-h*.06,2.8,0,7);x.fill();x.strokeStyle=st.body;x.lineWidth=6;x.lineCap='round';x.beginPath();x.moveTo(-p.w*.12,h*.11);x.lineTo(-p.w*.22,h*.2);x.moveTo(p.w*.05,h*.14);x.lineTo(p.w*.16,h*.24);x.moveTo(-p.w*.08,-h*.055);x.lineTo(-p.w*.2,-h*.14);x.moveTo(p.w*.02,-h*.05);x.lineTo(p.w*.13,-h*.16);x.stroke();x.strokeStyle=st.body;x.lineWidth=4;x.beginPath();x.moveTo(-p.w*.26,-h*.01);x.lineTo(-p.w*.37,-h*.075);x.stroke();if(p.skin==='electric'){x.strokeStyle=st.accent;x.lineWidth=2.5;x.beginPath();x.moveTo(p.w*.31,-h*.19);x.lineTo(p.w*.23,-h*.065);x.lineTo(p.w*.33,-h*.065);x.lineTo(p.w*.25,h*.08);x.stroke()}else if(p.skin==='water'){x.strokeStyle=st.accent;x.lineWidth=2;x.beginPath();x.arc(-p.w*.17,-h*.18,8,0,Math.PI);x.arc(0,-h*.2,9,0,Math.PI);x.stroke()}else if(p.skin==='air'){x.strokeStyle=st.accent;x.lineWidth=2;x.beginPath();x.arc(-7,-h*.19,7,.3,5.8);x.arc(9,-h*.15,10,.4,5.6);x.stroke()}else{x.fillStyle=st.accent;x.beginPath();x.moveTo(-p.w*.05,-h*.18);x.quadraticCurveTo(p.w*.02,-h*.29,p.w*.12,-h*.17);x.quadraticCurveTo(p.w*.05,-h*.1,-p.w*.05,-h*.18);x.fill();if(p.earthGuard===2){x.strokeStyle='#fff0a8';x.lineWidth=2;x.beginPath();x.arc(0,0,p.w*.34,0,7);x.stroke()}}x.restore()}"""
sub(r"function drawPlayer\(\)\{.*?\}\nfunction loop", turtle_draw + "\nfunction loop", 'turtle drawing')

# Freeze all game calculations and rendering while paused.
sub(
    r"function loop\(now\)\{let dt=Math\.min\(\.033,\(now-last\)/1000\|\|0\);last=now;update\(dt\);draw\(\);requestAnimationFrame\(loop\)\}",
    "function loop(now){let dt=Math.min(.033,(now-last)/1000||0);last=now;if(!paused){update(dt);draw()}requestAnimationFrame(loop)}",
    'pause loop',
)

path.write_text(s)
print('Turtle skins, abilities and pause menu added.')
