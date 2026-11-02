import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
const {loadOmowright}=await import(pathToFileURL(process.env.OMOWRIGHT_LOADER).href);
import {mkdtempSync,rmSync,writeFileSync,readFileSync} from 'node:fs';
const {omowright}=await loadOmowright();const profile=mkdtempSync('/tmp/illo-measure-');const b=await omowright.connectPipe({browserPath:process.env.CHROME_PATH,browserArgs:['--headless','--no-sandbox',`--user-data-dir=${profile}`],storageRoot:profile});
try {const p=await b.newTab('about:blank');const rows=[];
for(const width of [1440,390,320])for(const kind of (process.env.QA_PAGE?[process.env.QA_PAGE]:['compare','list']))for(const result of kind==='compare'?[false,true]:[false]){
 const name=(width===1440?'':'m-')+(kind==='compare'?'S3-compare.html':'S1-list.html');await p.goto('about:blank',{waitUntil:'commit'});await p.goto(`file://${process.cwd()}/prototype/${name}?view=${width===1440?'desktop':'mobile'}${result?'#result':''}`);await omowright.repinViewport(p,{width,height:900});await p.evaluate(()=>document.fonts.ready);await p.snapshot();
 const metrics=await p.evaluate(()=>{const a=document.querySelector('article');const sections=a?[...a.querySelectorAll('section')]:[];const first=document.querySelector('[aria-labelledby$="list"] [aria-label="저장"]');return {bodyHeight:sections.length?sections.at(-1).getBoundingClientRect().bottom-sections[0].getBoundingClientRect().top:null,scrollHeight:document.documentElement.scrollHeight,firstTop:first?.getBoundingClientRect().top??null};});rows.push({width,kind,result,...metrics});}
writeFileSync(process.env.QA_MEASURE,JSON.stringify(rows,null,2));
if(process.env.QA_BASELINE){
 const before=JSON.parse(readFileSync(process.env.QA_BASELINE));
 for(const row of rows){const old=before.find(v=>v.width===row.width&&v.kind===row.kind&&v.result===row.result);assert(old);
  if(row.kind==='compare'){assert(row.bodyHeight<old.bodyHeight,'P03-T53 body reduction');assert(row.scrollHeight<=old.scrollHeight,'P03-T53 total page must not grow');}
  else assert(row.firstTop<=old.firstTop,'P02-T22 first posting');
 }
 console.log('PASS P03-T53 / P02-T22 height and first posting measurements');
}else console.log('Baseline recorded; no reduction claims');
}finally{await b.close();rmSync(profile,{recursive:true,force:true});}
