# Normalise AircraftShapesSVG files: solid white body + dark detail lines, square viewBox around the
# aircraft, editor metadata removed. Output = shapes/<TYPE>.svg + shapes/index.json
import json,os,re,sys
from playwright.sync_api import sync_playwright
src,dst=sys.argv[1],sys.argv[2]
files=sorted(f for f in os.listdir(src) if f.endswith('.svg'))
os.makedirs(dst,exist_ok=True)
JS=r"""(txt)=>{
  const host=document.getElementById('h');host.innerHTML=txt.replace(/fill:none/gi,'fill:#ffffff').replace(/stroke:#000000/gi,'stroke:#1a1a1a');
  const svg=host.querySelector('svg');svg.removeAttribute('width');svg.removeAttribute('height');
  const bb=svg.getBBox(),side=Math.max(bb.width,bb.height)*1.08;
  svg.setAttribute('viewBox',[(bb.x+bb.width/2-side/2).toFixed(3),(bb.y+bb.height/2-side/2).toFixed(3),side.toFixed(3),side.toFixed(3)].join(' '));
  svg.querySelectorAll('metadata,title,desc,defs').forEach(n=>n.remove());
  svg.querySelectorAll('*').forEach(n=>{[...n.attributes].forEach(a=>{if(/^(inkscape|sodipodi):|^id$|^xml:space$/.test(a.name))n.removeAttribute(a.name);});
    if(/^(sodipodi|inkscape):/.test(n.tagName))n.remove();});
  [...svg.attributes].forEach(a=>{if(!/^(viewBox|xmlns|version)$/.test(a.name))svg.removeAttribute(a.name);});
  svg.setAttribute('xmlns','http://www.w3.org/2000/svg');
  return new XMLSerializer().serializeToString(svg);
}"""
codes=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.set_content('<div id="h"></div>')
    for f in files:
        code=f[:-4].upper()
        if not re.fullmatch(r'[A-Z0-9]{2,4}',code):continue
        out=pg.evaluate(JS,open(os.path.join(src,f),encoding='utf-8').read())
        out=re.sub(r'\s+xmlns:(inkscape|sodipodi|rdf|cc|dc|svg)="[^"]*"','',out)
        out=re.sub(r'>\s+<','><',out)
        open(os.path.join(dst,code+'.svg'),'w').write(out);codes.append(code)
    b.close()
have=set(codes)
cands={'E75L':['E175','E170','E190'],'E75S':['E175','E170','E190'],'E170':['E190'],'E290':['E190'],'E295':['E195'],
 'A20N':['A320'],'A21N':['A321'],'A19N':['A319'],'A318':['A319'],'A339':['A333','A332'],'A338':['A332'],'A35K':['A359'],
 'B37M':['B737'],'B38M':['B738'],'B39M':['B739','B738'],'B3XM':['B39M','B739','B738'],'B736':['B737'],
 'B78X':['B789','B788'],'B77W':['B773','B772'],'B77L':['B772'],'B778':['B77W','B773'],'B779':['B77W','B773'],'B764':['B763'],'B762':['B763'],
 'B748':['B744'],'B753':['B752'],'BCS3':['BCS1'],'A223':['BCS3','BCS1'],'A221':['BCS1','BCS3'],
 'CRJ7':['CRJ9','CRJ2'],'CRJX':['CRJ9'],'CRJ2':['CRJ9'],'E135':['E145'],'E145':['E135'],'AT76':['AT72'],'AT75':['AT72'],'DH8D':['DH8C'],
 'C182':['C172'],'C152':['C172'],'P28A':['C172'],'PA28':['C172'],'SR22':['C172'],'SR20':['C172'],'BE36':['C172'],
 'C25A':['C25B','C525'],'C25B':['C25A','C525'],'C25C':['C25B','C525'],'C56X':['C560'],'C68A':['C680'],'C700':['C680'],
 'GLF5':['GLF6','GLF4'],'GLF6':['GLF5'],'GL7T':['GLEX','GL5T'],'GL5T':['GLEX'],'CL35':['CL30'],'CL30':['CL35'],
 'H60':['S70','UH60'],'EC45':['EC35'],'B407':['B06','EC35'],'R22':['R44'],'R66':['R44']}
alias={}
for t,opts in cands.items():
    if t in have:continue
    for o in opts:
        if o in have:alias[t]=o;break
generic={'A1':'C172','A2':'PC12','A3':'A320','A4':'B752','A5':'B772','A6':'F16','A7':'R44'}
generic={k:v for k,v in generic.items() if v in have}
json.dump({'codes':sorted(have),'alias':alias,'byCategory':generic},open(os.path.join(dst,'index.json'),'w'),separators=(',',':'))
print(len(have),'shapes;',len(alias),'aliases;',generic)
