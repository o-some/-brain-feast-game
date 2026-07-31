from pathlib import Path

path = Path('index.html')
s = path.read_text()

def rep(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'{label}: source not found')
    s = s.replace(old, new, 1)

# Mobile/PWA meta tags.
rep(
    '<meta name="theme-color" content="#f2c500">',
    '<meta name="theme-color" content="#f2c500">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
    'mobile meta tags',
)

# Full 16:9 stage and rotation overlay.
rep(
    'body{position:fixed;inset:0}#game{position:absolute;inset:0;width:100%;height:100%;display:block;background:#0b0710}',
    'body{position:fixed;inset:0;background:#000}#stage{position:absolute;left:50%;top:50%;width:min(100vw,calc(100vh * 16 / 9));height:min(100vh,calc(100vw * 9 / 16));transform:translate(-50%,-50%);overflow:hidden;background:#151006;box-shadow:0 0 50px #000}#game{position:absolute;inset:0;width:100%;height:100%;display:block;background:#0b0710}.rotate-notice{position:fixed;inset:0;z-index:50;display:grid;place-items:center;padding:28px;background:#050402;color:#fff4a0;text-align:center}.rotate-notice.hidden{display:none}.rotate-card{max-width:520px;padding:28px;border:3px solid #f2c500;border-radius:28px;background:#211a08f2;box-shadow:0 0 45px #ffd90066}.rotate-icon{font-size:72px;display:block;animation:turnPhone 1.5s ease-in-out infinite alternate}.rotate-title{font-size:clamp(28px,8vw,48px);font-weight:1000;margin:10px 0}.rotate-text{font-size:18px;line-height:1.4}@keyframes turnPhone{from{transform:rotate(0deg)}to{transform:rotate(90deg)}}',
    '16:9 stage css',
)

# Fullscreen button pointer events and theme.
s = s.replace('#sound,#pauseBtn{pointer-events:auto;border:0;color:#fff;min-width:44px}', '#sound,#pauseBtn,#fullscreenBtn{pointer-events:auto;border:0;color:#fff;min-width:44px}', 1)
s = s.replace('#sound,#pauseBtn{color:#ffe545}', '#sound,#pauseBtn,#fullscreenBtn{color:#ffe545}', 1)

# Body wrapper, rotation notice and fullscreen button.
rep(
    '<body>\n<canvas id="game"></canvas>',
    '<body>\n<div class="rotate-notice hidden" id="rotateNotice"><div class="rotate-card"><span class="rotate-icon">📱</span><div class="rotate-title">Handy drehen</div><div class="rotate-text">Brain Feast läuft im Querformat 16:9. Drehe dein Handy nach links oder rechts.</div></div></div>\n<div id="stage">\n<canvas id="game"></canvas>',
    'stage wrapper start',
)
rep(
    '<button class="pill" id="pauseBtn">⏸</button></div>',
    '<button class="pill" id="pauseBtn">⏸</button><button class="pill" id="fullscreenBtn">⛶</button></div>',
    'fullscreen hud button',
)

# Swap mobile controls: fire/jump left, joystick right.
old_controls = '<div class="weapon-dock" id="weaponDock"><button class="weapon-slot active" data-weapon="thunder" aria-label="Donnerblitz"><span class="slot-icon">1⚡</span><span class="ammo">∞</span></button><button class="weapon-slot locked" data-weapon="storm" aria-label="Himmelszorn"><span class="slot-icon">2🌩️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="skull" aria-label="Schädelwerfer"><span class="slot-icon">3☠️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="saw" aria-label="Volt-Säge"><span class="slot-icon">4🪚</span><span class="ammo">—</span></button></div><div class="controls"><div class="joystick" id="joystick" aria-label="Bewegungs-Joystick"><div class="joy-knob" id="joyKnob"></div></div><div class="actions"><button class="action-btn" id="jumpBtn" data-key="up" aria-label="Springen">▲</button><button class="action-btn" id="fireBtn" data-key="shoot" aria-label="Feuern">⚡</button></div></div>'
new_controls = '<div class="weapon-dock" id="weaponDock"><button class="weapon-slot active" data-weapon="thunder" aria-label="Donnerblitz"><span class="slot-icon">1⚡</span><span class="ammo">∞</span></button><button class="weapon-slot locked" data-weapon="storm" aria-label="Himmelszorn"><span class="slot-icon">2🌩️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="skull" aria-label="Schädelwerfer"><span class="slot-icon">3☠️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="saw" aria-label="Volt-Säge"><span class="slot-icon">4🪚</span><span class="ammo">—</span></button></div><div class="controls"><div class="actions"><button class="action-btn" id="jumpBtn" data-key="up" aria-label="Springen">▲</button><button class="action-btn" id="fireBtn" data-key="shoot" aria-label="Feuern">⚡</button></div><div class="joystick" id="joystick" aria-label="Bewegungs-Joystick"><div class="joy-knob" id="joyKnob"></div></div></div>'
rep(old_controls, new_controls, 'swap mobile controls')

# Update onboarding text.
s = s.replace('📱 Links: Joystick zum Laufen, Springen und Ducken.<br>👉 Rechts: großer Feuerknopf und zusätzlicher Sprungknopf.<br>', '📱 Nur Querformat 16:9 – im Hochformat musst du das Handy drehen.<br>🕹️ Rechts: Joystick zum Laufen, Springen und Ducken.<br>🔥 Links: großer Feuerknopf und zusätzlicher Sprungknopf.<br>', 1)

# Close stage before script.
rep(
    '</div>\n<script>\n(()=>{\'use strict\';',
    '</div>\n</div>\n<script>\n(()=>{\'use strict\';',
    'stage wrapper end',
)

# DOM references and orientation state.
rep(
    "const start=$('start'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),hint=$('hint'),joystick=$('joystick'),joyKnob=$('joyKnob'),fireBtn=$('fireBtn'),jumpBtn=$('jumpBtn');",
    "const stage=$('stage'),rotateNotice=$('rotateNotice'),start=$('start'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),fullscreenBtn=$('fullscreenBtn'),hint=$('hint'),joystick=$('joystick'),joyKnob=$('joyKnob'),fireBtn=$('fireBtn'),jumpBtn=$('jumpBtn');",
    'dom refs',
)
rep(
    ",paused=false,bg=null,shotSoundAt=0,lowPower=matchMedia('(pointer:coarse)').matches;",
    ",paused=false,bg=null,shotSoundAt=0,lowPower=matchMedia('(pointer:coarse)').matches,orientationBlocked=false;",
    'orientation state',
)

# Immersive mode and orientation blocking.
anchor = "function setSkin(kind,silent=false){if(!skinDefs[kind])kind='electric';p.skin=kind;p.earthGuard=0;try{localStorage.brainFeastSkin=kind}catch(e){}syncSkinButtons();if(!silent){hint.textContent=skinDefs[kind].label+' aktiviert';hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},1500)}hud()}"
insert = anchor + "\nasync function requestImmersive(){try{let el=document.documentElement,req=el.requestFullscreen||el.webkitRequestFullscreen;if(req&&!document.fullscreenElement&&!document.webkitFullscreenElement){let result=req.call(el);if(result&&result.catch)await result.catch(()=>{})}}catch(e){}try{if(screen.orientation&&screen.orientation.lock)await screen.orientation.lock('landscape')}catch(e){}setTimeout(resize,180)}\nfunction syncOrientation(){let blocked=lowPower&&innerHeight>innerWidth;orientationBlocked=blocked;rotateNotice.classList.toggle('hidden',!blocked);if(blocked){resetJoy();Object.keys(key).forEach(k=>key[k]=false)}}"
rep(anchor, insert, 'immersive helpers')

# Stage-based resize and orientation syncing.
old_resize = "function resize(){let cap=lowPower?1:1.5;dpr=Math.min(cap,devicePixelRatio||1);W=innerWidth;H=innerHeight;c.width=W*dpr;c.height=H*dpr;c.style.width=W+'px';c.style.height=H+'px';x.setTransform(dpr,0,0,dpr,0,0);G=H*.78;bg=x.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#100d05');bg.addColorStop(.65,'#302407');bg.addColorStop(1,'#6a4c00');if(!running)p.y=G-p.h;p.x=Math.min(Math.max(65,p.x),W-p.w-20)}addEventListener('resize',resize);resize();"
new_resize = "function resize(){let cap=lowPower?1:1.5;dpr=Math.min(cap,devicePixelRatio||1);W=stage.clientWidth;H=stage.clientHeight;c.width=Math.max(1,Math.round(W*dpr));c.height=Math.max(1,Math.round(H*dpr));c.style.width=W+'px';c.style.height=H+'px';x.setTransform(dpr,0,0,dpr,0,0);G=H*.78;bg=x.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#100d05');bg.addColorStop(.65,'#302407');bg.addColorStop(1,'#6a4c00');if(!running)p.y=G-p.h;p.x=Math.min(Math.max(65,p.x),W-p.w-20);syncOrientation()}addEventListener('resize',resize);addEventListener('orientationchange',()=>setTimeout(resize,180));resize();"
rep(old_resize, new_resize, 'stage resize')

# Request immersive mode when the game starts.
rep(
    "function begin(){reset();paused=false;running=true;pauseMenu.classList.add('hidden');start.classList.add('hidden');over.classList.add('hidden');hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},3500);electricSound('win')}",
    "function begin(){requestImmersive();reset();paused=false;running=true;pauseMenu.classList.add('hidden');start.classList.add('hidden');over.classList.add('hidden');hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},3500);electricSound('win')}",
    'begin fullscreen',
)

# Fullscreen button binding.
rep(
    "pauseBtn.onclick=e=>{e.preventDefault();togglePause()};",
    "pauseBtn.onclick=e=>{e.preventDefault();togglePause()};fullscreenBtn.onclick=e=>{e.preventDefault();requestImmersive()};",
    'fullscreen binding',
)

# Freeze game while portrait is blocked.
rep(
    "function loop(now){let dt=Math.min(.033,(now-last)/1000||0);last=now;if(!paused){update(dt);draw()}requestAnimationFrame(loop)}requestAnimationFrame(loop);",
    "function loop(now){let dt=Math.min(.033,(now-last)/1000||0);last=now;if(!paused&&!orientationBlocked){update(dt);draw()}requestAnimationFrame(loop)}requestAnimationFrame(loop);",
    'orientation game freeze',
)

path.write_text(s)
print('Landscape 16:9, fullscreen and swapped controls installed.')
