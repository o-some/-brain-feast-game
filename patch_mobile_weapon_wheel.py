from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def rep(old: str, new: str, label: str) -> None:
    global s
    if old not in s:
        raise SystemExit(f'{label}: source not found')
    s = s.replace(old, new, 1)

# PWA / standalone metadata.
rep(
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="apple-mobile-web-app-title" content="Brain Feast">\n<link rel="manifest" href="manifest.webmanifest">',
    'manifest metadata',
)

# Mobile-game interaction styles and radial weapon wheel.
extra_css = r'''
/* Mobile weapon wheel, no text selection, and fullscreen fallback */
html,body,#stage,#stage *{-webkit-user-select:none!important;user-select:none!important;-webkit-touch-callout:none!important;-webkit-user-drag:none!important}
button,canvas{touch-action:none;-webkit-tap-highlight-color:transparent;-webkit-appearance:none;appearance:none}
.weapon-wheel{position:relative;width:clamp(148px,31vw,188px);height:clamp(148px,31vw,188px);pointer-events:auto;touch-action:none;user-select:none}
.wheel-fire,.radial-weapon{position:absolute;border:2px solid #f3cf20;border-radius:50%;background:#2a220be8;color:#fff5a6;font-weight:1000;box-shadow:0 6px 0 #806000;touch-action:none;user-select:none;display:grid;place-items:center;align-content:center;line-height:1}
.wheel-fire{left:0;bottom:0;width:clamp(82px,20vw,104px);height:clamp(82px,20vw,104px);font-size:clamp(25px,6vw,38px);z-index:4}
.radial-weapon{width:clamp(52px,12vw,66px);height:clamp(52px,12vw,66px);font-size:clamp(16px,4vw,23px);z-index:3}
.radial-weapon.slot-storm{left:5px;top:0}
.radial-weapon.slot-skull{left:50%;top:2px;transform:translateX(-50%)}
.radial-weapon.slot-saw{right:0;top:43%;transform:translateY(-50%)}
.wheel-fire.active,.radial-weapon.active,.radial-weapon.firing{transform:translateY(4px);box-shadow:0 2px 0 #806000;background:#a77d00;color:#171000}
.radial-weapon.slot-skull.active,.radial-weapon.slot-skull.firing{transform:translate(-50%,4px)}
.radial-weapon.slot-saw.active,.radial-weapon.slot-saw.firing{transform:translateY(calc(-50% + 4px))}
.radial-weapon.locked{opacity:.38;filter:grayscale(1)}
.wheel-icon{display:block;pointer-events:none}.wheel-ammo{display:block;margin-top:3px;font-size:10px;pointer-events:none}
.fullscreen-help .card{width:min(620px,94vw)}
.fs-steps{margin:16px 0;padding:14px;border:2px solid #d8a900;border-radius:18px;background:#2b220acc;text-align:left;font-weight:900;line-height:1.55}
@media(pointer:coarse){.weapon-dock{display:none!important}}
@media(orientation:landscape) and (max-height:520px){.weapon-wheel{width:132px;height:132px}.wheel-fire{width:72px;height:72px;font-size:27px}.radial-weapon{width:46px;height:46px;font-size:16px}.wheel-ammo{font-size:8px}}
'''
if '/* Mobile weapon wheel, no text selection, and fullscreen fallback */' not in s:
    rep('</style>', extra_css + '\n</style>', 'append mobile wheel CSS')

old_controls = '<div class="weapon-dock" id="weaponDock"><button class="weapon-slot active" data-weapon="thunder" aria-label="Donnerblitz"><span class="slot-icon">1⚡</span><span class="ammo">∞</span></button><button class="weapon-slot locked" data-weapon="storm" aria-label="Himmelszorn"><span class="slot-icon">2🌩️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="skull" aria-label="Schädelwerfer"><span class="slot-icon">3☠️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="saw" aria-label="Volt-Säge"><span class="slot-icon">4🪚</span><span class="ammo">—</span></button></div><div class="controls"><div class="actions"><button class="action-btn" id="jumpBtn" data-key="up" aria-label="Springen">▲</button><button class="action-btn" id="fireBtn" data-key="shoot" aria-label="Feuern">⚡</button></div><div class="joystick" id="joystick" aria-label="Bewegungs-Joystick"><div class="joy-knob" id="joyKnob"></div></div></div>'
new_controls = '<div class="weapon-dock" id="weaponDock"><button class="weapon-slot active" data-weapon="thunder" aria-label="Donnerblitz"><span class="slot-icon">1⚡</span><span class="ammo">∞</span></button><button class="weapon-slot locked" data-weapon="storm" aria-label="Himmelszorn"><span class="slot-icon">2🌩️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="skull" aria-label="Schädelwerfer"><span class="slot-icon">3☠️</span><span class="ammo">—</span></button><button class="weapon-slot locked" data-weapon="saw" aria-label="Volt-Säge"><span class="slot-icon">4🪚</span><span class="ammo">—</span></button></div><div class="controls"><div class="weapon-wheel" id="weaponWheel" aria-label="Waffenrad und Feuer"><button type="button" class="radial-weapon slot-storm locked" data-wheel-weapon="storm" aria-label="Himmelszorn"><span class="wheel-icon">2🌩️</span><span class="wheel-ammo">—</span></button><button type="button" class="radial-weapon slot-skull locked" data-wheel-weapon="skull" aria-label="Schädelwerfer"><span class="wheel-icon">3☠️</span><span class="wheel-ammo">—</span></button><button type="button" class="radial-weapon slot-saw locked" data-wheel-weapon="saw" aria-label="Volt-Säge"><span class="wheel-icon">4🪚</span><span class="wheel-ammo">—</span></button><button type="button" class="action-btn wheel-fire" id="fireBtn" aria-label="Standard-Donnerblitz feuern oder zu einer Spezialwaffe ziehen"><span class="wheel-icon">1⚡</span><span class="wheel-ammo">∞</span></button></div><div class="joystick" id="joystick" aria-label="Bewegungs-Joystick"><div class="joy-knob" id="joyKnob"></div></div></div>'
rep(old_controls, new_controls, 'replace mobile controls')

# Fullscreen explanation for iPhone/iPad Safari. It is shown only when the browser refuses the Fullscreen API.
fullscreen_overlay = '''<div class="overlay hidden fullscreen-help" id="fullscreenHelp">\n <div class="card"><div class="badge">ECHTES VOLLBILD</div><h2 class="title" style="font-size:clamp(32px,7vw,58px)">Als Handyspiel öffnen</h2><p class="sub">Safari lässt Webseiten auf iPhone und iPad nicht immer direkt in echtes Vollbild wechseln.</p><div class="fs-steps">1. Oben auf <strong>Teilen</strong> tippen.<br>2. <strong>Zum Home-Bildschirm</strong> wählen.<br>3. Brain Feast über das neue Symbol starten.</div><p class="sub">Dann startet das Spiel ohne Safari-Leisten im Querformat.</p><button type="button" class="primary" id="closeFullscreenHelp">VERSTANDEN</button></div>\n</div>\n'''
if 'id="fullscreenHelp"' not in s:
    rep('<script>\n(()=>', fullscreen_overlay + '<script>\n(()=>', 'fullscreen fallback overlay')

# DOM references.
rep(
    "const stage=$('stage'),rotateNotice=$('rotateNotice'),rotateStartBtn=$('rotateStartBtn'),start=$('start'),startFullscreenBtn=$('startFullscreenBtn'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),fullscreenBtn=$('fullscreenBtn'),hint=$('hint'),joystick=$('joystick'),joyKnob=$('joyKnob'),fireBtn=$('fireBtn'),jumpBtn=$('jumpBtn');",
    "const stage=$('stage'),rotateNotice=$('rotateNotice'),rotateStartBtn=$('rotateStartBtn'),start=$('start'),startFullscreenBtn=$('startFullscreenBtn'),over=$('over'),pauseMenu=$('pause'),fullscreenHelp=$('fullscreenHelp'),closeFullscreenHelp=$('closeFullscreenHelp'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),fullscreenBtn=$('fullscreenBtn'),hint=$('hint'),joystick=$('joystick'),joyKnob=$('joyKnob'),fireBtn=$('fireBtn'),weaponWheel=$('weaponWheel');",
    'DOM references',
)

# Prevent Safari selection/callout/context menus during long presses.
rep(
    "const key={left:false,right:false,up:false,down:false,shoot:false};",
    "const key={left:false,right:false,up:false,down:false,shoot:false};\n['contextmenu','selectstart','dragstart'].forEach(type=>document.addEventListener(type,e=>e.preventDefault(),{passive:false}));",
    'selection prevention',
)

# Update both desktop weapon slots and the radial mobile buttons.
old_sync = "function syncWeaponSlots(){document.querySelectorAll('[data-weapon]').forEach(btn=>{let kind=btn.dataset.weapon,amount=weaponInventory[kind],locked=kind!=='thunder'&&amount<=0;btn.classList.toggle('locked',locked);btn.classList.toggle('active',p.weapon===kind);let ammo=btn.querySelector('.ammo');if(ammo)ammo.textContent=kind==='thunder'?'∞':amount>0?amount:'—'})}"
new_sync = "function syncWeaponSlots(){document.querySelectorAll('[data-weapon]').forEach(btn=>{let kind=btn.dataset.weapon,amount=weaponInventory[kind],locked=kind!=='thunder'&&amount<=0;btn.classList.toggle('locked',locked);btn.classList.toggle('active',p.weapon===kind);let ammo=btn.querySelector('.ammo');if(ammo)ammo.textContent=kind==='thunder'?'∞':amount>0?amount:'—'});document.querySelectorAll('[data-wheel-weapon]').forEach(btn=>{let kind=btn.dataset.wheelWeapon,amount=weaponInventory[kind],locked=amount<=0;btn.classList.toggle('locked',locked);btn.classList.toggle('active',p.weapon===kind);let ammo=btn.querySelector('.wheel-ammo');if(ammo)ammo.textContent=amount>0?amount:'—'})}"
rep(old_sync, new_sync, 'radial ammo sync')

# Try every available Fullscreen API. If Safari refuses, show the standalone/PWA instructions.
old_fullscreen = "async function requestImmersive(){let supported=false,entered=false;try{let el=stage||document.documentElement,req=el.requestFullscreen||el.webkitRequestFullscreen;supported=!!req;if(req&&!document.fullscreenElement&&!document.webkitFullscreenElement){let result;try{result=req.call(el,{navigationUI:'hide'})}catch(_){result=req.call(el)}if(result&&result.catch)await result.catch(()=>{});entered=!!(document.fullscreenElement||document.webkitFullscreenElement)}}catch(e){}try{if(screen.orientation&&screen.orientation.lock)await screen.orientation.lock('landscape')}catch(e){}try{window.scrollTo(0,1)}catch(e){}fullscreenBtn.textContent=entered?'↙':'⛶';if(!supported){hint.textContent='Safari: Für echtes Vollbild über Teilen → Zum Home-Bildschirm öffnen';hint.style.opacity='1'}setTimeout(()=>{resize();resetStartScroll()},120);return entered}"
new_fullscreen = "function isStandalone(){return !!(window.navigator.standalone||matchMedia('(display-mode: fullscreen)').matches||matchMedia('(display-mode: standalone)').matches)}async function requestImmersive(showHelp=true){let entered=isStandalone(),supported=false;if(!entered){for(let el of [document.documentElement,stage,document.body]){if(!el)continue;let req=el.requestFullscreen||el.webkitRequestFullscreen||el.webkitRequestFullScreen;if(!req)continue;supported=true;try{let result;try{result=req.call(el,{navigationUI:'hide'})}catch(_){result=req.call(el)}if(result&&result.then)await result.catch(()=>{});entered=!!(document.fullscreenElement||document.webkitFullscreenElement||document.webkitCurrentFullScreenElement);if(entered)break}catch(e){}}}try{if(screen.orientation&&screen.orientation.lock)await screen.orientation.lock('landscape')}catch(e){}try{window.scrollTo(0,1)}catch(e){}fullscreenBtn.textContent=(entered||isStandalone())?'↙':'⛶';if(!entered&&!isStandalone()&&showHelp){fullscreenHelp.classList.remove('hidden');hint.textContent=supported?'Safari hat Vollbild abgelehnt · als App öffnen':'Für echtes Vollbild als App zum Home-Bildschirm hinzufügen';hint.style.opacity='1'}setTimeout(()=>{resize();resetStartScroll()},120);return entered}"
rep(old_fullscreen, new_fullscreen, 'fullscreen fallback logic')

# Replace the left jump/fire stack with the radial weapon-fire control.
old_binding = "function bindAction(btn,name){let stop=e=>{e.preventDefault();control(name,false)};btn.addEventListener('pointerdown',e=>{e.preventDefault();try{btn.setPointerCapture?.(e.pointerId)}catch(_){}control(name,true)});['pointerup','pointercancel','lostpointercapture'].forEach(ev=>btn.addEventListener(ev,stop))}bindAction(fireBtn,'shoot');bindAction(jumpBtn,'up');"
new_binding = "let weaponPointer=null,wheelWeapon='thunder';function setWheelVisual(kind,on){document.querySelectorAll('[data-wheel-weapon]').forEach(btn=>btn.classList.toggle('firing',on&&btn.dataset.wheelWeapon===kind));fireBtn.classList.toggle('active',on&&kind==='thunder')}function wheelWeaponAt(e){let r=weaponWheel.getBoundingClientRect(),fr=fireBtn.getBoundingClientRect(),cx=fr.left+fr.width/2,cy=fr.top+fr.height/2,dx=e.clientX-cx,dy=e.clientY-cy,dist=Math.hypot(dx,dy);if(dist<fr.width*.62)return'thunder';let angle=Math.atan2(dy,dx)*180/Math.PI;if(angle<-67)return'storm';if(angle<-20)return'skull';return'saw'}function activateWheelWeapon(kind,notify=false){if(kind!=='thunder'&&weaponInventory[kind]<=0){if(notify)selectWeapon(kind,false);return false}wheelWeapon=kind;selectWeapon(kind,true);setWheelVisual(kind,true);return true}function stopWheelFire(e){if(e){e.preventDefault();e.stopPropagation()}control('shoot',false);weaponPointer=null;setWheelVisual(wheelWeapon,false);wheelWeapon='thunder';selectWeapon('thunder',true)}fireBtn.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();weaponPointer=e.pointerId;try{weaponWheel.setPointerCapture?.(e.pointerId)}catch(_){}activateWheelWeapon('thunder');control('shoot',true)});weaponWheel.addEventListener('pointermove',e=>{if(e.pointerId!==weaponPointer)return;e.preventDefault();let kind=wheelWeaponAt(e);if(kind!==wheelWeapon&&activateWheelWeapon(kind,true)){fire()}});['pointerup','pointercancel','lostpointercapture'].forEach(ev=>weaponWheel.addEventListener(ev,e=>{if(weaponPointer===null||e.pointerId===weaponPointer)stopWheelFire(e)}));document.querySelectorAll('[data-wheel-weapon]').forEach(btn=>{let kind=btn.dataset.wheelWeapon;btn.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();if(!activateWheelWeapon(kind,true))return;weaponPointer=e.pointerId;try{btn.setPointerCapture?.(e.pointerId)}catch(_){}control('shoot',true)});['pointerup','pointercancel','lostpointercapture'].forEach(ev=>btn.addEventListener(ev,stopWheelFire))});"
rep(old_binding, new_binding, 'radial weapon controls')

# Fullscreen and start button bindings. Starting never waits for or depends on fullscreen.
old_taps = "function tapAction(btn,fn){if(!btn)return;let locked=false;let run=e=>{if(e){e.preventDefault();e.stopPropagation()}if(locked)return;locked=true;setTimeout(()=>locked=false,260);fn(e)};btn.addEventListener('click',run,false);btn.addEventListener('pointerup',run,false);btn.addEventListener('touchend',run,{passive:false})}const playBtn=$('play');tapAction(playBtn,()=>{requestImmersive();setTimeout(begin,0)});tapAction(startFullscreenBtn,()=>requestImmersive());tapAction(rotateStartBtn,async()=>{pendingLandscapeStart=true;requestImmersive();syncOrientation();if(!orientationBlocked){pendingLandscapeStart=false;setTimeout(begin,0)}else{let txt=rotateNotice.querySelector('.rotate-text');if(txt)txt.textContent='Drehe das Handy jetzt ins Querformat. Danach startet das Spiel.'}});tapAction($('again'),begin);tapAction($('resumeBtn'),()=>togglePause(false));tapAction(soundBtn,()=>{audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()});tapAction(pauseBtn,()=>togglePause());tapAction(fullscreenBtn,()=>requestImmersive());"
new_taps = "function tapAction(btn,fn){if(!btn)return;let locked=false;let run=e=>{if(e){e.preventDefault();e.stopPropagation()}if(locked)return;locked=true;setTimeout(()=>locked=false,260);fn(e)};btn.addEventListener('click',run,false);btn.addEventListener('pointerup',run,false);btn.addEventListener('touchend',run,{passive:false})}const playBtn=$('play');tapAction(playBtn,()=>{requestImmersive(false);setTimeout(begin,0)});tapAction(startFullscreenBtn,()=>requestImmersive(true));tapAction(rotateStartBtn,async()=>{pendingLandscapeStart=true;requestImmersive(false);syncOrientation();if(!orientationBlocked){pendingLandscapeStart=false;setTimeout(begin,0)}else{let txt=rotateNotice.querySelector('.rotate-text');if(txt)txt.textContent='Drehe das Handy jetzt ins Querformat. Danach startet das Spiel.'}});tapAction($('again'),begin);tapAction($('resumeBtn'),()=>togglePause(false));tapAction(closeFullscreenHelp,()=>fullscreenHelp.classList.add('hidden'));tapAction(soundBtn,()=>{audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()});tapAction(pauseBtn,()=>togglePause());tapAction(fullscreenBtn,()=>requestImmersive(true));"
rep(old_taps, new_taps, 'fullscreen button bindings')

# Update the compact start hint.
s = s.replace('Rechts steuern · links feuern · oben Waffen wechseln · ⏸ öffnet Skins', 'Rechts steuern · links Waffenrad & feuern · ⏸ öffnet Skins', 1)

path.write_text(s, encoding='utf-8')

manifest = '''{
  "name": "Brain Feast",
  "short_name": "Brain Feast",
  "description": "Element-Schildkröten Endless Runner",
  "start_url": "./?mode=standalone",
  "scope": "./",
  "display": "fullscreen",
  "display_override": ["fullscreen", "standalone"],
  "orientation": "landscape",
  "background_color": "#100d05",
  "theme_color": "#f2c500"
}
'''
Path('manifest.webmanifest').write_text(manifest, encoding='utf-8')
print('Mobile weapon wheel, selection lock, and fullscreen fallback installed')
