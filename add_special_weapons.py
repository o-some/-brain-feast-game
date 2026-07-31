from pathlib import Path
import re

path = Path('index.html')
s = path.read_text()

def sub(pattern, replacement, label, count=1):
    global s
    s, n = re.subn(pattern, replacement, s, count=count, flags=re.S)
    if n != count:
        raise SystemExit(f'{label}: expected {count}, got {n}')

s = s.replace(
    '⚡ Donnerblitz von Anfang an · unendlich · 💥 oder F feuern.<br>',
    '⚡ Donnerblitz von Anfang an · unendlich · 💥 oder F feuern.<br>🎁 Unterwegs erscheinen drei Spezialwaffen mit jeweils 50 Schuss.<br>',
    1,
)

sub(
    r"function hud\(\)\{.*?\}\nfunction jump",
    r"""const weaponNames={thunder:'⚡ Donnerblitz',storm:'🌩️ Himmelszorn',skull:'☠️ Schädelwerfer',saw:'🪚 Volt-Säge'};
function hud(){scoreEl.textContent='Punkte '+Math.floor(score).toLocaleString('de-DE');weaponEl.textContent=weaponNames[p.weapon]+(p.weapon==='thunder'?' ∞':' '+p.ammo);livesEl.textContent='❤️'.repeat(Math.max(0,p.lives))+'☠️'.repeat(Math.max(0,3-p.lives))}
function equipWeapon(kind){p.weapon=kind;p.ammo=50;hint.textContent=weaponNames[kind]+' eingesammelt · 50 Schuss';hint.style.opacity='1';setTimeout(()=>hint.style.opacity='.15',1800);tone(kind==='storm'?980:kind==='skull'?180:520,.1,kind==='skull'?'sawtooth':'square',.022);hud()}
function spendAmmo(){if(p.weapon==='thunder')return;p.ammo--;if(p.ammo<=0){p.weapon='thunder';p.ammo=Infinity;hint.textContent='Spezialwaffe leer · zurück zum Donnerblitz';hint.style.opacity='1';setTimeout(()=>hint.style.opacity='.15',1600)}hud()}
function nearestTargetX(){if(boss)return boss.x+boss.w/2;let tx=Math.min(W-70,p.x+Math.min(430,W*.56)),best=1e9;for(let o of objects){if(o.destroyed||o.type==='platform'||o.x<p.x)continue;if(o.x<best){best=o.x;tx=o.x+o.w/2}}return tx}
function jump""",
    'hud helpers',
)

sub(
    r"function pickup\(\)\{.*?\}\nfunction box",
    r"""function pickup(){let r=Math.random();if(r<.16){let kinds=['storm','skull','saw'],weapon=kinds[Math.floor(Math.random()*kinds.length)];pickups.push({type:'weapon',weapon,x:W+50,y:G-(85+Math.random()*150),r:22,phase:Math.random()*6});return}r=(r-.16)/.84;let type=r<.12?'heart':r<.30?'gold':'brain';pickups.push({type,weapon:null,x:W+50,y:G-(70+Math.random()*180),r:18,phase:Math.random()*6})}
function box""",
    'pickup function',
)

sub(
    r"function fire\(\)\{.*?\}\nfunction destroyObstacle",
    r"""function fire(){if(!running||p.cool>0)return;let limit=p.weapon==='thunder'?3:4;if(shots.length>=limit)return;let sy=p.y+(p.duck?p.h*.62:p.h*.34);if(p.weapon==='storm'){let tx=nearestTargetX(),s={x:tx,y:G,r:24,life:.14,pierce:99,type:'storm',phase:0,damage:2};shots.push(s);if(boss)hitBoss(s);for(let o of objects){if(o.destroyed||o.type==='platform')continue;if(Math.abs(o.x+o.w/2-tx)<52)destroyObstacle(o,s)}p.cool=.34}else if(p.weapon==='skull'){shots.push({x:p.x+p.w-2,y:sy,vx:980,r:11,life:.72,pierce:3,type:'skull',phase:0,damage:1});p.cool=.27}else if(p.weapon==='saw'){shots.push({x:p.x+p.w-2,y:sy,vx:900,r:13,life:.78,pierce:5,type:'saw',phase:0,damage:1});p.cool=.3}else{shots.push({x:p.x+p.w-2,y:sy,vx:1250,r:5,life:.46,pierce:1,type:'thunder',phase:Math.random()*10,damage:1});p.cool=.22}if(t>=shotSoundAt){let f=p.weapon==='storm'?1040:p.weapon==='skull'?170:p.weapon==='saw'?480:880;tone(f,.025,p.weapon==='skull'?'sawtooth':'square',.01);shotSoundAt=t+.45}spendAmmo()}
function destroyObstacle""",
    'fire function',
)

sub(
    r"function hitBoss\(s\)\{.*?\}\nfunction bossAttack",
    r"""function hitBoss(s){if(!boss||s.life<=0)return false;let hb={x:boss.x+12,y:boss.y+8,w:boss.w-24,h:boss.h-10},sb={x:s.x-s.r,y:s.y-s.r,w:s.r*2,h:s.r*2};if(!hit(sb,hb))return false;let dmg=s.damage||1;boss.hp-=dmg;boss.flash=.08;if(s.type!=='storm')s.life=0;score+=25*dmg;sparks(s.x,s.y,s.type==='storm'?5:3);if(boss.hp<=0)beatBoss();return true}
function bossAttack""",
    'boss damage',
)

s = s.replace(
    "for(let q of shots){q.x+=q.vx*dt;q.phase=(q.phase||0)+dt*18;q.life-=dt}",
    "for(let q of shots){if(q.type!=='storm')q.x+=q.vx*dt;q.phase=(q.phase||0)+dt*18;q.life-=dt}",
    1,
)
if "if(q.type!=='storm')q.x" not in s:
    raise SystemExit('shot update replacement failed')

s = s.replace(
    "for(let q of shots){if(q.life<=0)continue;if(boss&&hitBoss(q))continue;",
    "for(let q of shots){if(q.life<=0||q.type==='storm')continue;if(boss&&hitBoss(q))continue;",
    1,
)
if "q.life<=0||q.type==='storm'" not in s:
    raise SystemExit('shot collision replacement failed')

old_pickup_collision = "for(let q of pickups){if(Math.hypot(p.x+p.w/2-q.x,p.y+p.h/2-q.y)<45){q.got=true;if(q.type==='heart')p.lives=Math.min(3,p.lives+1);else score+=q.type==='gold'?500:100;hud();tone(q.type==='gold'?980:700,.08)}}"
new_pickup_collision = "for(let q of pickups){if(Math.hypot(p.x+p.w/2-q.x,p.y+p.h/2-q.y)<48){q.got=true;if(q.type==='weapon'){equipWeapon(q.weapon);score+=250}else if(q.type==='heart'){p.lives=Math.min(3,p.lives+1);tone(700,.08)}else{score+=q.type==='gold'?500:100;tone(q.type==='gold'?980:700,.08)}hud()}}"
if old_pickup_collision not in s:
    raise SystemExit('pickup collision source not found')
s = s.replace(old_pickup_collision, new_pickup_collision, 1)

sub(
    r"function drawPick\(q\)\{.*?\}\nfunction drawBossShot",
    r"""function drawPick(q){x.save();x.translate(q.x,q.y+Math.sin(q.phase)*5);if(q.type==='weapon'){let col=q.weapon==='storm'?'#68d7ff':q.weapon==='skull'?'#f2efe3':'#ffb52e';x.fillStyle='#17130b';x.strokeStyle=col;x.lineWidth=4;x.beginPath();x.arc(0,0,23,0,7);x.fill();x.stroke();x.fillStyle=col;if(q.weapon==='storm'){x.beginPath();x.moveTo(3,-16);x.lineTo(-8,2);x.lineTo(1,2);x.lineTo(-5,17);x.lineTo(12,-4);x.lineTo(3,-4);x.closePath();x.fill()}else if(q.weapon==='skull'){x.beginPath();x.arc(0,-3,12,0,7);x.fill();x.fillRect(-7,6,14,8);x.fillStyle='#17130b';x.beginPath();x.arc(-4,-4,3,0,7);x.arc(4,-4,3,0,7);x.fill()}else{x.beginPath();for(let i=0;i<16;i++){let a=i/16*Math.PI*2,r=i%2?10:17;i?x.lineTo(Math.cos(a)*r,Math.sin(a)*r):x.moveTo(Math.cos(a)*r,Math.sin(a)*r)}x.closePath();x.fill();x.fillStyle='#17130b';x.beginPath();x.arc(0,0,5,0,7);x.fill()}x.restore();return}x.shadowColor=q.type==='gold'?'#ffcd45':'#ff4873';x.shadowBlur=8;x.fillStyle=q.type==='gold'?'#f1b722':q.type==='heart'?'#da1748':'#d97891';if(q.type==='heart'){x.beginPath();x.moveTo(0,15);x.bezierCurveTo(-24,-2,-17,-18,-7,-15);x.bezierCurveTo(0,-14,0,-7,0,-5);x.bezierCurveTo(1,-14,14,-18,20,-8);x.bezierCurveTo(25,2,12,12,0,15);x.fill()}else{for(let a=0;a<6;a++){let ang=a/6*6.28;x.beginPath();x.arc(Math.cos(ang)*8,Math.sin(ang)*7,9,0,7);x.fill()}x.strokeStyle='#6e263a';x.lineWidth=2;x.beginPath();x.moveTo(0,-15);x.lineTo(0,15);x.stroke()}x.restore()}
function drawBossShot""",
    'draw pickup',
)

sub(
    r"function drawShot\(s\)\{.*?\}\nfunction drawPlayer",
    r"""function drawShot(s){x.save();if(s.type==='storm'){let alpha=Math.max(0,Math.min(1,s.life/.14));x.globalAlpha=alpha;x.strokeStyle='#73dcff';x.lineWidth=8;x.beginPath();let yy=8;x.moveTo(s.x,yy);for(let i=1;i<=7;i++){yy=i/7*(G-8);x.lineTo(s.x+(i%2?12:-10),yy)}x.stroke();x.strokeStyle='#fffbd1';x.lineWidth=3;x.stroke();x.fillStyle='#dfffff';x.beginPath();x.arc(s.x,G-5,18,0,7);x.fill();x.restore();return}x.translate(s.x,s.y);x.rotate(s.phase*.12);if(s.type==='skull'){x.fillStyle='#eee9dc';x.beginPath();x.arc(0,-2,11,0,7);x.fill();x.fillRect(-7,6,14,8);x.fillStyle='#241709';x.beginPath();x.arc(-4,-3,3,0,7);x.arc(4,-3,3,0,7);x.fill();x.restore();return}if(s.type==='saw'){x.fillStyle='#ffb52e';x.beginPath();for(let i=0;i<20;i++){let a=i/20*Math.PI*2,r=i%2?10:15;i?x.lineTo(Math.cos(a)*r,Math.sin(a)*r):x.moveTo(Math.cos(a)*r,Math.sin(a)*r)}x.closePath();x.fill();x.fillStyle='#34240b';x.beginPath();x.arc(0,0,5,0,7);x.fill();x.restore();return}x.lineCap='round';x.strokeStyle='#ffe33b';x.lineWidth=4;x.beginPath();x.moveTo(-18,0);x.lineTo(-8,-4);x.lineTo(0,3);x.lineTo(8,-3);x.lineTo(17,0);x.stroke();x.strokeStyle='#fffbd1';x.lineWidth=1.5;x.beginPath();x.moveTo(-15,0);x.lineTo(-6,-2);x.lineTo(1,2);x.lineTo(9,-1);x.lineTo(15,0);x.stroke();x.restore()}
function drawPlayer""",
    'draw shot',
)

path.write_text(s)
print('Special weapons added.')
