// Physical constraints and primitive gains are authored in physical_sfg/models.json.
// Run build_physical_sfg.py first; this step only lays out the retained DOT graphs.
import {instance} from '../tmp/ch02/web-deps/node_modules/@viz-js/viz/dist/viz.js';
import fs from 'node:fs';
const viz=await instance();
const models=JSON.parse(fs.readFileSync('derivations/ch02/physical_sfg/models.json','utf8'));
for(const m of models){
 const stem=`derivations/ch02/assets/${m.id}-sfg`;
 fs.writeFileSync(`${stem}.svg`,viz.renderString(fs.readFileSync(`${stem}.dot`,'utf8'),{format:'svg',engine:'dot'}));
}
console.log(`Rendered ${models.length} Physical / Causal SFGs from retained DOT constraints.`);
