from pathlib import Path
import re

path = Path('index.html')
s = path.read_text()


def replace_once(old: str, new: str, label: str) -> None:
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    s = s.replace(old, new, 1)

replace_once(
    "function sparks(px,py,n=20){for(let i=0;i<n;i++){let a=Math.random()*Math.PI*2,v=100+Math.random()*330;particles.push({x:px,y:py,vx:Math.cos(a)*v,vy:Math.sin(a)*v,l:.25+Math.random()*.35,electric:true})}}",
    "function sparks(px,py,n=12){let room=Math.max(0,90-particles.length);n=Math.min(n,room);for(let i=0;i<n;i++){let a=Math.random()*Math.PI*2,v=90+Math.random()*250;particles.push({x:px,y:py,vx:Math.cos(a)*v,vy:Math.sin(a)*v,l:.16+Math.random()*.22,electric:true})}}",
    'spark limiter',
)

replace_once(
    "function fire(){if(!running||p.cool>0)return;let sy=p.y+(p.duck?p.h*.62:p.h*.34);shots.push({x:p.x+p.w-2,y:sy,vx:1120,r:8,life:1.18,pierce:1,type:'thunder',phase:Math.random()*10,trail:[]});p.cool=.14;sparks(p.x+p.w,sy,7);electricSound('fire')}",
    "function fire(){if(!running||p.cool>0||shots.length>=5)return;let sy=p.y+(p.duck?p.h*.62:p.h*.34);shots.push({x:p.x+p.w-2,y:sy,vx:1180,r:6,life:.62,pierce:1,type:'thunder',phase:Math.random()*10,trail:[]});p.cool=.19;sparks(p.x+p.w,sy,3);electricSound('fire')}",
    'fire limiter',
)

replace_once("if(q.trail.length>8)q.trail.shift()", "if(q.trail.length>3)q.trail.shift()", 'short trail')
replace_once(
    "particles=particles.filter(z=>z.l>0)}",
    "particles=particles.filter(z=>z.l>0);if(particles.length>90)particles.splice(0,particles.length-90)}",
    'particle cap',
)
replace_once(
    "x.strokeStyle='#ffe23d';x.lineWidth=5;x.shadowColor='#ffe12f';x.shadowBlur=18;",
    "x.strokeStyle='#ffe23d';x.lineWidth=3.5;x.shadowColor='#ffe12f';x.shadowBlur=9;",
    'trail glow',
)
replace_once(
    "x.strokeStyle='#fffbd1';x.lineWidth=4;x.shadowColor='#ffe12f';x.shadowBlur=22;",
    "x.strokeStyle='#fffbd1';x.lineWidth=3;x.shadowColor='#ffe12f';x.shadowBlur=11;",
    'bolt glow',
)
replace_once(
    "x.moveTo(-12,-10);x.lineTo(-3,-4);x.lineTo(-8,1);x.lineTo(4,2);x.lineTo(-1,11);x.lineTo(13,1);",
    "x.moveTo(-8,-7);x.lineTo(-2,-3);x.lineTo(-5,1);x.lineTo(3,1);x.lineTo(-1,7);x.lineTo(8,1);",
    'short bolt shape',
)
replace_once("x.arc(0,0,4,0,7)", "x.arc(0,0,3,0,7)", 'smaller bolt core')

path.write_text(s)
print('Continuous-fire performance optimized.')
