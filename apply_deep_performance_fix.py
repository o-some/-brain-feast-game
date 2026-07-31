from pathlib import Path

path = Path('index.html')
s = path.read_text()

def rep(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {count}')
    s = s.replace(old, new, 1)

rep(
"let W=0,H=0,G=0,dpr=1,running=false,last=performance.now(),t=0,worldX=0,bossClock=0,bossCount=0,score=0,clock=0,speed=330,spawn=1,pickClock=1.4,objects=[],pickups=[],shots=[],bossShots=[],laser=null,boss=null,particles=[],high=+(localStorage.brainFeastHigh||0),audio=true,ac=null,target=null;",
"let W=0,H=0,G=0,dpr=1,running=false,last=performance.now(),t=0,worldX=0,bossClock=0,bossCount=0,score=0,clock=0,speed=330,spawn=1,pickClock=1.4,objects=[],pickups=[],shots=[],bossShots=[],laser=null,boss=null,particles=[],high=+(localStorage.brainFeastHigh||0),audio=true,ac=null,target=null,bg=null,shotSoundAt=0,lowPower=matchMedia('(pointer:coarse)').matches;",
'globals')

rep(
"function resize(){dpr=Math.min(2,devicePixelRatio||1);W=innerWidth;H=innerHeight;c.width=W*dpr;c.height=H*dpr;c.style.width=W+'px';c.style.height=H+'px';x.setTransform(dpr,0,0,dpr,0,0);G=H*.78;if(!running)p.y=G-p.h;p.x=Math.min(Math.max(65,p.x),W-p.w-20)}addEventListener('resize',resize);resize();",
"function resize(){let cap=lowPower?1:1.5;dpr=Math.min(cap,devicePixelRatio||1);W=innerWidth;H=innerHeight;c.width=W*dpr;c.height=H*dpr;c.style.width=W+'px';c.style.height=H+'px';x.setTransform(dpr,0,0,dpr,0,0);G=H*.78;bg=x.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#100d05');bg.addColorStop(.65,'#302407');bg.addColorStop(1,'#6a4c00');if(!running)p.y=G-p.h;p.x=Math.min(Math.max(65,p.x),W-p.w-20)}addEventListener('resize',resize);resize();",
'resize')

rep(
"function sparks(px,py,n=12){let room=Math.max(0,90-particles.length);n=Math.min(n,room);for(let i=0;i<n;i++){let a=Math.random()*Math.PI*2,v=90+Math.random()*250;particles.push({x:px,y:py,vx:Math.cos(a)*v,vy:Math.sin(a)*v,l:.16+Math.random()*.22,electric:true})}}",
"function sparks(px,py,n=6){let room=Math.max(0,36-particles.length);n=Math.min(n,room);for(let i=0;i<n;i++){let a=Math.random()*Math.PI*2,v=80+Math.random()*170;particles.push({x:px,y:py,vx:Math.cos(a)*v,vy:Math.sin(a)*v,l:.12+Math.random()*.14,electric:true})}}",
'sparks')

rep(
"function burst(px,py){for(let i=0;i<18;i++)particles.push({x:px,y:py,vx:(Math.random()-.5)*260,vy:(Math.random()-.8)*240,l:.7})}",
"function burst(px,py,n=8){let room=Math.max(0,36-particles.length);n=Math.min(n,room);for(let i=0;i<n;i++)particles.push({x:px,y:py,vx:(Math.random()-.5)*190,vy:(Math.random()-.75)*180,l:.3})}",
'burst')

rep(
"function fire(){if(!running||p.cool>0||shots.length>=5)return;let sy=p.y+(p.duck?p.h*.62:p.h*.34);shots.push({x:p.x+p.w-2,y:sy,vx:1180,r:6,life:.62,pierce:1,type:'thunder',phase:Math.random()*10,trail:[]});p.cool=.19;sparks(p.x+p.w,sy,3);electricSound('fire')}",
"function fire(){if(!running||p.cool>0||shots.length>=3)return;let sy=p.y+(p.duck?p.h*.62:p.h*.34);shots.push({x:p.x+p.w-2,y:sy,vx:1250,r:5,life:.46,pierce:1,type:'thunder',phase:Math.random()*10});p.cool=.22;if(t>=shotSoundAt){tone(880,.025,'square',.01);shotSoundAt=t+.5}}",
'fire')

rep(
"function destroyObstacle(o,s){if(o.destroyed||o.type==='platform')return;o.destroyed=true;score+=o.type==='human'?180:120;burst(o.x+o.w/2,o.y+o.h/2);sparks(o.x+o.w/2,o.y+o.h/2,28);for(let i=0;i<9;i++)particles.push({x:o.x+o.w/2,y:o.y+o.h/2,vx:(Math.random()-.5)*360,vy:(Math.random()-.8)*300,l:.55,metal:o.type!=='human'});electricSound('hit');hud()}",
"function destroyObstacle(o,s){if(o.destroyed||o.type==='platform')return;o.destroyed=true;score+=o.type==='human'?180:120;burst(o.x+o.w/2,o.y+o.h/2,5);sparks(o.x+o.w/2,o.y+o.h/2,4);hud()}",
'destroy obstacle')

rep(
"function hitBoss(s){if(!boss||s.life<=0)return false;let hb={x:boss.x+12,y:boss.y+8,w:boss.w-24,h:boss.h-10},sb={x:s.x-s.r,y:s.y-s.r,w:s.r*2,h:s.r*2};if(!hit(sb,hb))return false;boss.hp--;boss.flash=.12;s.life=0;score+=25;sparks(s.x,s.y,16);electricSound('hit');if(boss.hp<=0)beatBoss();return true}",
"function hitBoss(s){if(!boss||s.life<=0)return false;let hb={x:boss.x+12,y:boss.y+8,w:boss.w-24,h:boss.h-10},sb={x:s.x-s.r,y:s.y-s.r,w:s.r*2,h:s.r*2};if(!hit(sb,hb))return false;boss.hp--;boss.flash=.08;s.life=0;score+=25;sparks(s.x,s.y,3);if(boss.hp<=0)beatBoss();return true}",
'hit boss')

rep(
"for(let q of shots){q.trail=q.trail||[];q.trail.push({x:q.x,y:q.y});if(q.trail.length>3)q.trail.shift();q.x+=q.vx*dt;q.phase=(q.phase||0)+dt*22;q.life-=dt}",
"for(let q of shots){q.x+=q.vx*dt;q.phase=(q.phase||0)+dt*18;q.life-=dt}",
'shot update')

rep(
"for(let z of particles){z.l-=dt;z.vy+=500*dt;z.x+=z.vx*dt;z.y+=z.vy*dt}particles=particles.filter(z=>z.l>0);if(particles.length>90)particles.splice(0,particles.length-90)}",
"for(let z of particles){z.l-=dt;z.vy+=420*dt;z.x+=z.vx*dt;z.y+=z.vy*dt}particles=particles.filter(z=>z.l>0);if(particles.length>36)particles.splice(0,particles.length-36)}",
'particle cap')

rep(
"function draw(){let g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#100d05');g.addColorStop(.65,'#302407');g.addColorStop(1,'#6a4c00');x.fillStyle=g;x.fillRect(0,0,W,H);x.fillStyle='#ffd52e';x.shadowColor='#ffe13a';x.shadowBlur=25;x.beginPath();x.arc(W*.82,H*.14,Math.min(45,H*.07),0,7);x.fill();x.shadowBlur=0;",
"function draw(){x.fillStyle=bg||'#100d05';x.fillRect(0,0,W,H);x.fillStyle='#ffd52e';x.beginPath();x.arc(W*.82,H*.14,Math.min(45,H*.07),0,7);x.fill();",
'background draw')

rep(
"for(let o of objects)drawObj(o);for(let q of pickups)drawPick(q);for(let s of shots)drawShot(s);for(let b of bossShots)drawBossShot(b);if(laser)drawLaser();if(boss)drawBoss();drawPlayer();for(let z of particles){x.globalAlpha=Math.max(0,z.l);if(z.electric){x.globalCompositeOperation='lighter';x.strokeStyle='#fff7b0';x.shadowColor='#ffe12f';x.shadowBlur=13;x.lineWidth=2.4;x.beginPath();x.moveTo(z.x,z.y);x.lineTo(z.x-z.vx*.035+(Math.random()-.5)*8,z.y-z.vy*.035+(Math.random()-.5)*8);x.stroke();x.shadowBlur=0;x.globalCompositeOperation='source-over'}else{x.fillStyle='#d20d3d';x.beginPath();x.arc(z.x,z.y,5,0,7);x.fill()}}x.globalAlpha=1;if(target){",
"for(let o of objects)drawObj(o);for(let q of pickups)drawPick(q);for(let s of shots)drawShot(s);for(let b of bossShots)drawBossShot(b);if(laser)drawLaser();if(boss)drawBoss();drawPlayer();for(let z of particles){x.globalAlpha=Math.max(0,z.l);if(z.electric){x.strokeStyle='#ffe85a';x.lineWidth=1.5;x.beginPath();x.moveTo(z.x,z.y);x.lineTo(z.x-z.vx*.025,z.y-z.vy*.025);x.stroke()}else{x.fillStyle='#d20d3d';x.beginPath();x.arc(z.x,z.y,3,0,7);x.fill()}}x.globalAlpha=1;if(target){",
'particle draw')

old_draw = "function drawShot(s){x.save();x.globalCompositeOperation='lighter';x.lineCap='round';if(s.trail&&s.trail.length){x.strokeStyle='#ffe23d';x.lineWidth=3.5;x.shadowColor='#ffe12f';x.shadowBlur=9;x.beginPath();x.moveTo(s.trail[0].x,s.trail[0].y);for(let i=1;i<s.trail.length;i++){let q=s.trail[i];x.lineTo(q.x,q.y+Math.sin(s.phase+i*2)*5)}x.lineTo(s.x,s.y);x.stroke()}x.translate(s.x,s.y);x.rotate(s.phase*.15);x.strokeStyle='#fffbd1';x.lineWidth=3;x.shadowColor='#ffe12f';x.shadowBlur=11;x.beginPath();x.moveTo(-8,-7);x.lineTo(-2,-3);x.lineTo(-5,1);x.lineTo(3,1);x.lineTo(-1,7);x.lineTo(8,1);x.stroke();x.fillStyle='#ffe33b';x.beginPath();x.arc(0,0,3,0,7);x.fill();x.restore()}"
new_draw = "function drawShot(s){x.save();x.translate(s.x,s.y);x.rotate(s.phase*.12);x.lineCap='round';x.strokeStyle='#ffe33b';x.lineWidth=4;x.beginPath();x.moveTo(-18,0);x.lineTo(-8,-4);x.lineTo(0,3);x.lineTo(8,-3);x.lineTo(17,0);x.stroke();x.strokeStyle='#fffbd1';x.lineWidth=1.5;x.beginPath();x.moveTo(-15,0);x.lineTo(-6,-2);x.lineTo(1,2);x.lineTo(9,-1);x.lineTo(15,0);x.stroke();x.restore()}"
rep(old_draw, new_draw, 'draw shot')

path.write_text(s)
print('Deep mobile performance fix applied.')
