from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def rep(old: str, new: str, label: str) -> None:
    global s
    if old not in s:
        raise SystemExit(f'{label}: source not found')
    s = s.replace(old, new, 1)

# Dynamic viewport: iOS Safari's 100vh includes browser chrome and hid the start buttons.
rep(
    "#stage{position:absolute;left:50%;top:50%;width:min(100vw,calc(100vh * 16 / 9));height:min(100vh,calc(100vw * 9 / 16));",
    "#stage{position:absolute;left:50%;top:50%;width:min(100vw,calc(100dvh * 16 / 9));height:min(100dvh,calc(100vw * 9 / 16));",
    'dynamic viewport stage',
)

extra_css = r'''
/* iOS guaranteed start controls v2 */
#start{padding:5px;overflow:hidden;touch-action:auto}
#start .card{position:relative;width:min(1180px,99%);height:calc(100% - 4px);max-height:none;overflow:hidden;padding:7px 10px 76px;display:block;touch-action:auto}
#start .badge{display:none}
#start .title{margin:0;font-size:clamp(26px,8vh,46px);line-height:.92}
#start .sub{margin:2px 0 4px;font-size:clamp(11px,2.6vh,16px);line-height:1.12}
#start .help{display:none}
#start .skin-grid{grid-template-columns:repeat(4,minmax(0,1fr));gap:5px;margin:5px 0}
#start .skin-btn{min-height:48px;padding:5px 3px;border-radius:12px;font-size:clamp(9px,2.1vh,14px);line-height:1.05;pointer-events:auto;touch-action:manipulation}
#start .small-note{font-size:clamp(7px,1.55vh,10px);line-height:1.05;margin-top:2px}
#start .start-actions{position:absolute!important;left:8px;right:8px;bottom:max(7px,env(safe-area-inset-bottom));z-index:1000;display:flex;gap:8px;margin:0;padding:0;background:none;pointer-events:auto;touch-action:manipulation}
#start .start-actions button{display:block!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;touch-action:manipulation!important;position:relative;z-index:1001;min-height:54px}
#play{flex:1.35!important}
#startFullscreenBtn{flex:.65!important}
.start-mini-help{display:block;margin:4px 0 1px;color:#fff0a2;font-size:clamp(9px,2vh,13px);font-weight:900;line-height:1.15}
@media (orientation:landscape) and (max-height:560px){
 #start .title{font-size:30px}
 #start .sub{font-size:11px}
 #start .skin-grid{margin:3px 0;gap:4px}
 #start .skin-btn{min-height:42px;padding:3px 2px;font-size:9px}
 #start .small-note{font-size:7px}
 #start .card{padding:4px 7px 68px}
 #start .start-actions button{min-height:48px;padding:7px 8px;font-size:17px}
}
'''
if '/* iOS guaranteed start controls v2 */' not in s:
    rep('</style>', extra_css + '\n</style>', 'append emergency CSS')

# Replace the oversized instruction panel with one compact line on the start screen.
old_help = '<div class="help">📱 Nur Querformat 16:9 – im Hochformat musst du das Handy drehen.<br>🕹️ Rechts: Joystick zum Laufen, Springen und Ducken.<br>🔥 Links: großer Feuerknopf und zusätzlicher Sprungknopf.<br>⚡ Standard-Donnerblitz unendlich · 💥, F oder X feuern.<br>🎁 Waffen landen im Inventar. Oben rechts wechselst du zwischen Slot 1–4.<br>⌨️ P oder ⏸ pausiert und öffnet die Skin-Auswahl.<br>☠️ Alle 30 Sekunden stoppt die Welt für den Bosskampf.</div>'
new_help = '<div class="start-mini-help">Rechts steuern · links feuern · oben Waffen wechseln · ⏸ öffnet Skins</div>'
rep(old_help, new_help, 'compact start help')

# Make the two main buttons explicit form-independent buttons.
rep(
    '<div class="start-actions"><button class="primary secondary" id="startFullscreenBtn">⛶ VOLLBILD</button><button class="primary" id="play">JETZT SPIELEN</button></div>',
    '<div class="start-actions"><button type="button" class="primary secondary" id="startFullscreenBtn">⛶ VOLLBILD</button><button type="button" class="primary" id="play">JETZT SPIELEN</button></div>',
    'button types',
)
rep(
    '<button class="primary rotate-start" id="rotateStartBtn">⛶ VOLLBILD &amp; STARTEN</button>',
    '<button type="button" class="primary rotate-start" id="rotateStartBtn">⛶ VOLLBILD &amp; STARTEN</button>',
    'rotate button type',
)

# Remove the previous pointerdown fullscreen request. On iOS it could swallow the following pointerup/click.
old_bindings = "function robust(btn,fn){let done=false,fire=e=>{e.preventDefault();e.stopPropagation();if(done)return;done=true;fn(e);setTimeout(()=>done=false,320)};btn.addEventListener('pointerup',fire,{passive:false});btn.addEventListener('touchend',fire,{passive:false});btn.addEventListener('click',fire)}const playBtn=$('play');playBtn.addEventListener('pointerdown',()=>requestImmersive(),{passive:true});robust(playBtn,begin);robust(startFullscreenBtn,requestImmersive);robust(rotateStartBtn,async()=>{pendingLandscapeStart=true;await requestImmersive();syncOrientation();if(!orientationBlocked){pendingLandscapeStart=false;begin()}else{let txt=rotateNotice.querySelector('.rotate-text');if(txt)txt.textContent='Vollbild wurde angefordert. Drehe das Handy jetzt ins Querformat.'}});robust($('again'),begin);robust($('resumeBtn'),()=>togglePause(false));soundBtn.onclick=e=>{e.preventDefault();audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()};pauseBtn.onclick=e=>{e.preventDefault();togglePause()};fullscreenBtn.onclick=e=>{e.preventDefault();requestImmersive()};"
new_bindings = "function tapAction(btn,fn){if(!btn)return;let locked=false;let run=e=>{if(e){e.preventDefault();e.stopPropagation()}if(locked)return;locked=true;setTimeout(()=>locked=false,260);fn(e)};btn.addEventListener('click',run,false);btn.addEventListener('pointerup',run,false);btn.addEventListener('touchend',run,{passive:false})}const playBtn=$('play');tapAction(playBtn,()=>{requestImmersive();setTimeout(begin,0)});tapAction(startFullscreenBtn,()=>requestImmersive());tapAction(rotateStartBtn,async()=>{pendingLandscapeStart=true;requestImmersive();syncOrientation();if(!orientationBlocked){pendingLandscapeStart=false;setTimeout(begin,0)}else{let txt=rotateNotice.querySelector('.rotate-text');if(txt)txt.textContent='Drehe das Handy jetzt ins Querformat. Danach startet das Spiel.'}});tapAction($('again'),begin);tapAction($('resumeBtn'),()=>togglePause(false));tapAction(soundBtn,()=>{audio=!audio;soundBtn.textContent=audio?'🔊':'🔇';if(audio)tone()});tapAction(pauseBtn,()=>togglePause());tapAction(fullscreenBtn,()=>requestImmersive());"
rep(old_bindings, new_bindings, 'safe iOS button bindings')

# Keep the start controls at the top of the visual viewport after rotations/browser-bar changes.
rep(
    "function resetStartScroll(){try{start.scrollTop=0;let card=start.querySelector('.card');if(card)card.scrollTop=0}catch(e){}}",
    "function resetStartScroll(){try{start.scrollTop=0;let card=start.querySelector('.card');if(card)card.scrollTop=0;let actions=start.querySelector('.start-actions');if(actions)actions.style.transform='translateZ(0)'}catch(e){}}",
    'start reset',
)

path.write_text(s, encoding='utf-8')
print('iOS start v2 repair installed')
