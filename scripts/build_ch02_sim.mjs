import fs from 'node:fs';
import {Marked} from '../tmp/ch02/web-deps/node_modules/marked/lib/marked.esm.js';
import katex from '../tmp/ch02/web-deps/node_modules/katex/dist/katex.mjs';
const out='output/simulations/ch02';const marked=new Marked({gfm:true});let count=0;
const math=[];let text=fs.readFileSync(`${out}/report.md`,'utf8');
text=text.replace(/\$\$([\s\S]*?)\$\$|(?<![\\$])\$(?!\$)((?:\\.|[^$\n])+?)\$/g,(all,block,inline)=>{
 const display=block!==undefined,key=`SIMMATHTOKEN${math.length}END`;
 math.push({key,display,html:katex.renderToString((display?block:inline).trim(),{displayMode:display,throwOnError:true,strict:'ignore',trust:false})});count++;
 return display?`\n\n${key}\n\n`:key;
});
let html=marked.parse(text);
for(const m of math){if(m.display)html=html.replace(`<p>${m.key}</p>`,m.html);html=html.replaceAll(m.key,m.html)}
html=html.replaceAll('<img ','<img loading="lazy" ');
const groups=JSON.parse(fs.readFileSync(`${out}/module_summary.json`));
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const nav=Object.entries(groups).map(([id,g])=>`<a href="#${id}">${id.slice(0,2)} · ${esc(g.title)}</a>`).join('');
const page=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sansen 第二章 · Spectre 仿真</title><link rel="stylesheet" href="../../derivations/ch02/assets/ch02.css"><link rel="stylesheet" href="../../derivations/ch02/assets/katex/katex.min.css"><style>article h4{font-size:18px;margin-top:32px}article img{max-height:780px;object-fit:contain}article>a[id]{scroll-margin-top:20px}nav strong{display:block;margin:15px 10px;font-size:13px}</style></head><body><header><div class="eyebrow">SANSEN · CHAPTER 02 · CADENCE SPECTRE 18.1</div><h1>从推导到实际仿真</h1><p>32 组线性 AC · 7 个 MOS 电路 · 5 组极零分析 · 3 组瞬态验证</p></header><div class="layout"><nav aria-label="仿真目录"><a href="../../derivations/ch02/index.html">← 第二章公式推导</a><a href="../../extraction/index.html">全书抽取数据库</a><a href="report.md">完整 Markdown</a><a href="verification.json">验证数值与运行记录</a><strong>20 组代表模型</strong>${nav}</nav><main><div class="links"><a href="report.md">Markdown</a><a href="README.md">模型与重建说明</a><a href="gmid_selection.json">gm/Id 法确定尺寸</a></div><article>${html}</article><footer>本地离线页面。原始 Spectre PSF、netlist 与解析结果保存在工作区。MOS1 为教学模型，尚无 晶圆厂 PDK 验证。</footer></main></div></body></html>`;
fs.writeFileSync(`${out}/index.html`,page);
fs.writeFileSync(`${out}/render_verification.json`,JSON.stringify({status:'passed',math_expressions_rendered:count,renderer:'marked + KaTeX; throwOnError=true',browser_qa:false},null,2));
console.log(`Simulation page rendered: ${count} math expressions.`);
