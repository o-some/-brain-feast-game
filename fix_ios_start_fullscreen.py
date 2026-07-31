from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str) -> None:
    global s
    if old not in s:
        raise SystemExit(f'{label}: source not found')
    s = s.replace(old, new, 1)

# The body-level touch-action:none blocked scrolling inside the landscape start card on iOS.
# Keep game controls locked, but allow the overlays/cards to scroll and remain clickable.
extra_css = r'''
/* iOS landscape start/fullscreen repair */
html,body{touch-action:manipulation;height:100dvh}
#game,.controls,.joystick,.action-btn{touch-action:none}
.overlay,.card{touch-action:pan-y;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
.primary,.skin-btn,.weapon-slot,#fullscreenBtn,.rotate-start{touch-action:manipulation;pointer-events:auto}
#start{padding:6px;place-items:center;overflow:hidden}
#start .card{width:min(1180px,99%);height:calc(100% - 8px);max-height:none;padding:8px 12px;display:flex;flex-direction:column;overflow-y:auto;overflow-x:hidden}
#start .badge{padding:4px 10px;font-size:clamp(10px,2.1vh,14px)}
#start .title{margin:2px 0;font-size:clamp(30px,8.5vh,58px);line-height:.92}
#start .sub{margin:2px 0;font-size:clamp(12px,2.7vh,18px);line-height:1.15}
#start .help{margin:5px 0;padding:7px 10px;font-size:clamp(10px,2.25vh,15px);line-height:1.2}
#start .skin-grid{grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin:5px 0}
#start .skin-btn{padding:6px 4px;border-radius:13px;font-size:clamp(10px,2.25vh,15px);box-shadow:0 3px 0 #7f6100}
#start .skin-btn.active{transform:translateY(1px);box-shadow:0 2px 0 #7f6100}
#start .small-note{font-size:clamp(8px,1.65vh,10px);margin-top:2px}
.start-actions{position:sticky;bottom:-1px;z-index:25;display:flex;gap:8px;margin-top:auto;padding:7px 0 2px;background:linear-gradient(180deg,#1c160800,#1c1608 28%);pointer-events:auto}
.start-actions .primary{min-width:0;flex:1;padding:10px 12px;border-radius:16px;font-size:clamp(16px,4.4vh,28px);box-shadow:0 5px 0 #8b6100}
.start-actions .secondary{flex:.55;background:linear-gradient(#40330f,#211908);color:#fff2a3;border:2px solid #e7bd17;box-shadow:0 5px 0 #6b4c00}
.rotate-start{margin-top:18px;min-width:min(320px,82vw);font-size:22px;padding:14px 18px}
.fullscreen-fallback{font-size:12px;opacity:.78;margin-top:7px}
@media (orientation:landscape) and (max-height:520px){
 #start .card{padding:5px 9px}
 #start .badge{display:none}
 #start .title{font-size:clamp(28px,9vh,44px)}
 #start .sub{font-size:12px}
 #start .help{font-size:10px;line-height:1.14;margin:3px 0;padding:5px 7px}
 #start .skin-grid{gap:4px;margin:3px 0}
 #start .skin-btn{padding:4px 3px;font-size:10px}
 .start-actions{padding-top:4px}
 .start-actions .primary{padding:7px 10px;font-size:18px}
}
'''
if '/* iOS landscape start/fullscreen repair */' not in s:
    replace_once('</style>', extra_css + '\n</style>', 'append iOS CSS')

replace_once(
    '<div class="rotate-notice hidden" id="rotateNotice"><div class="rotate-card"><span class="rotate-icon">📱</span><div class="rotate-title">Handy drehen</div><div class="rotate-text">Brain Feast läuft im Querformat 16:9. Drehe dein Handy nach links oder rechts.</div></div></div>',
    '<div class="rotate-notice hidden" id="rotateNotice"><div class="rotate-card"><span class="rotate-icon">📱</span><div class="rotate-title">Handy drehen</div><div class="rotate-text">Brain Feast läuft im Querformat 16:9. Drehe dein Handy nach links oder rechts.</div><button class="primary rotate-start" id="rotateStartBtn">⛶ VOLLBILD &amp; STARTEN</button><div class="fullscreen-fallback">Falls Safari kein echtes Vollbild zulässt, startet das Spiel trotzdem direkt nach dem Drehen.</div></div></div>',
    'rotate start button',
)

replace_once(
    '</div><button class="primary" id="play">JETZT SPIELEN</button></div>',
    '</div><div class="start-actions"><button class="primary secondary" id="startFullscreenBtn">⛶ VOLLBILD</button><button class="primary" id="play">JETZT SPIELEN</button></div></div>',
    'sticky start actions',
)

replace_once(
    "const stage=$('stage'),rotateNotice=$('rotateNotice'),start=$('start'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),fullscreenBtn=$('fullscreenBtn'),hint=$('hint'),joystick=$('joystick'),joyKnob=$('joyKnob'),fireBtn=$('fireBtn'),jumpBtn=$('jumpBtn');",
    "const stage=$('stage'),rotateNotice=$('rotateNotice'),rotateStartBtn=$('rotateStartBtn'),start=$('start'),startFullscreenBtn=$('startFullscreenBtn'),over=$('over'),pauseMenu=$('pause'),scoreEl=$('score'),weaponEl=$('weapon'),livesEl=$('lives'),soundBtn=$('sound'),pauseBtn=$('pauseBtn'),fullscreenBtn=$('fullscreenBtn'),hint=$('hint'),joystick=$('joystick'),joyKnob=$('joyKnob'),fireBtn=$('fireBtn'),jumpBtn=$('jumpBtn');",
    'DOM references',
)

replace_once(
    "lowPower=matchMedia('(pointer:coarse)').matches,orientationBlocked=false;",
    "lowPower=matchMedia('(pointer:coarse)').matches,orientationBlocked=false,pendingLandscapeStart=false;",
    'pending landscape state',
)

replace_once(
    "async function requestImmersive(){try{let el=document.documentElement,req=el.requestFullscreen||el.webkitRequestFullscreen;if(req&&!document.fullscreenElement&&!document.webkitFullscreenElement){let result=req.call(el);if(result&&result.catch)await result.catch(()=>{})}}catch(e){}try{if(screen.orientation&&screen.orientation.lock)await screen.orientation.lock('landscape')}catch(e){}setTimeout(resize,180)}",
    "async function requestImmersive(){let supported=false,entered=false;try{let el=stage||document.documentElement,req=el.requestFullscreen||el.webkitRequestFullscreen;supported=!!req;if(req&&!document.fullscreenElement&&!document.webkitFullscreenElement){let result;try{result=req.call(el,{navigationUI:'hide'})}catch(_){result=req.call(el)}if(result&&result.catch)await result.catch(()=>{});entered=!!(document.fullscreenElement||document.webkitFullscreenElement)}}catch(e){}try{if(screen.orientation&&screen.orientation.lock)await screen.orientation.lock('landscape')}catch(e){}try{window.scrollTo(0,1)}catch(e){}fullscreenBtn.textContent=entered?'↙':'⛶';if(!supported){hint.textContent='Safari: Für echtes Vollbild über Teilen → Zum Home-Bildschirm öffnen';hint.style.opacity='1'}setTimeout(()=>{resize();resetStartScroll()},120);return entered}",
    'immersive function',
)

replace_once(
    "function syncOrientation(){let blocked=lowPower&&innerHeight>innerWidth;orientationBlocked=blocked;rotateNotice.classList.toggle('hidden',!blocked);if(blocked){resetJoy();Object.keys(key).forEach(k=>key[k]=false)}}",
    "function resetStartScroll(){try{start.scrollTop=0;let card=start.querySelector('.card');if(card)card.scrollTop=0}catch(e){}}\nfunction syncOrientation(){let wasBlocked=orientationBlocked,blocked=lowPower&&innerHeight>innerWidth;orientationBlocked=blocked;rotateNotice.classList.toggle('hidden',!blocked);if(blocked){resetJoy();Object.keys(key).forEach(k=>key[k]=false)}else{resetStartScroll();try{window.scrollTo(0,1)}catch(e){}if(wasBlocked){requestImmersive();if(pendingLandscapeStart){pendingLandscapeStart=false;setTimeout(begin,90)}}}}",
    'orientation sync',
)

replace_once(
    "addEventListener('resize',resize);addEventListener('orientationchange',()=>setTimeout(resize,180));resize();",
    "addEventListener('resize',resize);addEventListener('orientationchange',()=>setTimeout(()=>{resize();if(!orientationBlocked)requestImmersive()},220));if(window.visualViewport)visualViewport.addEventListener('resize',()=>setTimeout(resize,60));resize();",
    'orientation listeners',
)

replace_once(
    "function begin(){requestImmersive();reset();paused=false;running=true;pauseMenu.classList.add('hidden');start.classList.add('hidden');over.classList.add('hidden');hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},3500);electricSound('win')}",
    "function begin(){requestImmersive();syncOrientation();if(orientationBlocked){pendingLandscapeStart=true;rotateNotice.classList.remove('hidden');return}pendingLandscapeStart=false;reset();paused=false;running=true;pauseMenu.classList.add('hidden');start.classList.add('hidden');over.classList.add('hidden');hint.style.opacity='1';setTimeout(()=>{if(!paused)hint.style.opacity='.15'},3500);electricSound('win')}",
    'begin function',
)

replace_once(
    "function robust(btn,fn){let done=false,fire=e=>{e.preventDefault();if(done)return;done=true;fn();setTimeout(()=>done=false,350)};btn.addEventListener('pointerup',fire);btn.addEventListener('touchend',fire,{passive:false});btn.addEventListener('click',fire)}robust($('play'),begin);robust($('again'),begin);robust($('resumeBtn'),()=>togglePause(false));soundBtn.onclick=e=>{e.preventDefault();audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()};pauseBtn.onclick=e=>{e.preventDefault();togglePause()};fullscreenBtn.onclick=e=>{e.preventDefault();requestImmersive()};",
    "function robust(btn,fn){let done=false,fire=e=>{e.preventDefault();e.stopPropagation();if(done)return;done=true;fn(e);setTimeout(()=>done=false,320)};btn.addEventListener('pointerup',fire,{passive:false});btn.addEventListener('touchend',fire,{passive:false});btn.addEventListener('click',fire)}const playBtn=$('play');playBtn.addEventListener('pointerdown',()=>requestImmersive(),{passive:true});robust(playBtn,begin);robust(startFullscreenBtn,requestImmersive);robust(rotateStartBtn,async()=>{pendingLandscapeStart=true;await requestImmersive();syncOrientation();if(!orientationBlocked){pendingLandscapeStart=false;begin()}else{let txt=rotateNotice.querySelector('.rotate-text');if(txt)txt.textContent='Vollbild wurde angefordert. Drehe das Handy jetzt ins Querformat.'}});robust($('again'),begin);robust($('resumeBtn'),()=>togglePause(false));soundBtn.onclick=e=>{e.preventDefault();audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()};pauseBtn.onclick=e=>{e.preventDefault();togglePause()};fullscreenBtn.onclick=e=>{e.preventDefault();requestImmersive()};",
    'button bindings',
)

path.write_text(s, encoding='utf-8')
print('iOS start/fullscreen repair installed')
