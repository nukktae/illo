// Run with Node 24+, OMOWRIGHT_LOADER and CHROME_PATH pointing to local QA tools.
import assert from 'node:assert/strict';
import {mkdtempSync, rmSync, mkdirSync, writeFileSync} from 'node:fs';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
const {loadOmowright} = await import(pathToFileURL(process.env.OMOWRIGHT_LOADER).href);
const {omowright} = await loadOmowright();
const root = fileURLToPath(new URL('../prototype/', import.meta.url));
const output = process.env.QA_OUTPUT || '/tmp/illo-p03-qa';
mkdirSync(output,{recursive:true});
const profile = mkdtempSync('/tmp/illo-browser-');
const browser = await omowright.connectPipe({browserPath:process.env.CHROME_PATH,browserArgs:['--headless','--no-sandbox',`--user-data-dir=${profile}`],storageRoot:profile});
const passed=[];
try {
 const p=await browser.newTab('about:blank');
 async function go(name, mobile=false, hash='', width=mobile?390:1440, dir=root){
  await p.goto('about:blank',{waitUntil:'commit'});
  await p.goto(`${pathToFileURL(resolve(dir,name)).href}?view=${mobile?'mobile':'desktop'}${hash}`);
  await omowright.repinViewport(p,{width,height:900});
  await p.snapshot();
  await p.evaluate(()=>document.fonts.ready.then(()=>true));
  assert.equal(await p.evaluate(()=>innerWidth),width);
 }
 async function click(label,role='button',partial=false){
  const tree=omowright.compactSnapshot(await p.snapshot());
  const line=tree.split('\n').find(l=>l.includes(`${role} "${label}${partial?'':'"'}`)&&l.includes('ref='));
  assert(line,`Missing ${role} ${label}\n${tree}`);
  await p.locator(line.match(/ref=(\w+)/)[1]).click();
 }
 async function state(){return p.evaluate(()=>({url:location.href,article:document.querySelector('article').innerHTML,aside:document.querySelector('aside').innerHTML}));}
 async function highlights(done){
  const styles=await p.evaluate(()=>[...document.querySelectorAll('article li > span > span')].map(e=>{const c=getComputedStyle(e);return {bg:c.backgroundColor,color:c.color,decoration:c.textDecorationLine,radius:c.borderRadius,weight:c.fontWeight,clone:c.boxDecorationBreak,border:c.borderTopColor,borderWidth:c.borderTopWidth};}));
  // P03-T56/T58: validate all three states and absence before/reset.
  const expected=[['rgb(232, 245, 236)','rgb(22, 101, 52)','rgb(22, 101, 52)'],['rgb(255, 246, 229)','rgb(194, 106, 0)','rgb(194, 106, 0)'],['rgb(253, 236, 236)','rgb(180, 35, 24)','rgb(180, 35, 24)']];
  for(const [bg,color,border] of expected){
   const found=styles.filter(s=>s.bg===bg);
   if(done){assert(found.length>0,`P03-T56 missing ${bg}`);for(const s of found){assert.equal(s.color,color);assert.equal(s.decoration,'none');assert.equal(s.radius,'4px');assert.equal(s.weight,'600');assert.equal(s.clone,'clone');assert.equal(s.border,border);assert.equal(s.borderWidth,'1px');}}
   else assert.equal(found.length,0,'P03-T58 reset has no highlight');
  }
  // P03-T61/T63: summary tiles must match the text highlights in every result state.
  const tiles=await p.evaluate(()=>[...document.querySelectorAll('aside div')].filter(e=>e.children.length===2 && e.children[0].tagName==='SPAN' && e.children[1].tagName==='SPAN' && ['맞음','일부','없음'].includes(e.children[1].textContent)).map(e=>({label:e.children[1].textContent,count:e.children[0].textContent,bg:getComputedStyle(e).backgroundColor,colors:[...e.children].map(x=>getComputedStyle(x).color),border:getComputedStyle(e).borderTopWidth})));
  if(done){assert.equal(tiles.length,3,'P03-T61');for(const [i,t] of tiles.entries()){assert.equal(t.label,['맞음','일부','없음'][i]);assert.equal(t.count,['1','1','4'][i]);assert.equal(t.bg,expected[i][0]);assert.deepEqual(t.colors,[expected[i][1],expected[i][1]]);assert.equal(t.border,'0px');}}
  else assert.equal(tiles.length,0,'P03-T63 no result tiles before comparison');

  const badges=await p.evaluate(()=>[...document.querySelectorAll('article span')].filter(e=>['맞음','일부','없음'].includes(e.textContent)).map(e=>({label:e.textContent,bg:getComputedStyle(e).backgroundColor,color:getComputedStyle(e).color,border:getComputedStyle(e).borderTopWidth})));
  if(done){assert(badges.length>0,'P03-T64 evidence badges');for(const badge of badges){const i=['맞음','일부','없음'].indexOf(badge.label);assert.equal(badge.bg,expected[i][0],'P03-T64 badge background');assert.equal(badge.color,expected[i][1],'P03-T64 badge text');assert.equal(badge.border,'0px');}}
  else assert.equal(badges.length,0,'P03-T64 no badges before comparison');

  const rings=await p.evaluate(()=>[...document.querySelectorAll('aside [role="img"]')].map(e=>({label:e.getAttribute('aria-label'),text:e.textContent,arcs:[...e.querySelectorAll('circle[stroke-dasharray]')].map(x=>({color:x.getAttribute('stroke'),length:x.getAttribute('stroke-dasharray'),offset:x.getAttribute('stroke-dashoffset')}))})));
  if(done){assert.equal(rings.length,1,'P03-T65');const ring=rings[0];assert.equal(ring.label,'6개 중 맞음 1, 일부 1, 없음 4');assert.equal(ring.text,'2/6');assert.deepEqual(ring.arcs.map(a=>a.color),['#22C55E','#F59E0B','#EF4444']);for(const [i,a] of ring.arcs.entries()){const [length,c]=a.length.split(' ').map(Number);assert(Math.abs((length+2)/c-[1,1,4][i]/6)<.001);assert(Math.abs(Number(a.offset)/c+i/6)<.001);}}
  else assert.equal(rings.length,0,'P03-T65 no ring before comparison');

 }
 async function cards(){
  const data=await p.evaluate(()=>{const a=document.querySelector('article');const body=a.querySelector('[aria-label="공고 본문"]');const sections=[...body.querySelectorAll('section')];return {titles:sections.map(e=>e.querySelector('h3').textContent),bodyCount:a.querySelectorAll('[aria-label="공고 본문"]').length,bg:getComputedStyle(body).backgroundColor,borders:sections.slice(1).map(e=>getComputedStyle(e).borderTopWidth),overflow:document.documentElement.scrollWidth>innerWidth};});
  assert.deepEqual(data.titles,['담당업무','자격요건','우대사항','전형절차']);assert.equal(data.bodyCount,1);assert.equal(data.bg,'rgb(255, 255, 255)');assert(data.borders.every(n=>n==='1px'));assert.equal(data.overflow,false);
 }
 async function buttons(){
  const data=await p.evaluate(()=>{const a=[...document.querySelectorAll('a')].find(e=>e.textContent==='나의 이력서 수정');const b=[...document.querySelectorAll('button')].find(e=>e.textContent==='AI로 비교하기');const x=a.getBoundingClientRect(),y=b.getBoundingClientRect();return {innerW:innerWidth,sizes:[x.width,y.width,x.height,y.height,x.top-y.bottom],colors:[getComputedStyle(a).backgroundColor,getComputedStyle(b).backgroundColor],small:[...document.querySelectorAll('a')].some(e=>e.textContent==='이력서 수정 ›')};});
  const desk=data.innerW>=768;if(desk){assert.equal(data.sizes[0],data.sizes[1]);assert.deepEqual(data.sizes.slice(2),[52,52,8]);assert.deepEqual(data.colors,['rgb(242, 244, 246)','rgb(49, 130, 246)']);}else{assert(data.sizes[0]<data.sizes[1]);assert.deepEqual(data.sizes.slice(2),[44,54,8]);assert.deepEqual(data.colors,['rgb(255, 255, 255)','rgb(49, 130, 246)']);}assert.equal(data.small,false);
  const notice=await p.evaluate(()=>document.querySelector('aside').textContent);assert(notice.includes('시연용 예시 비교 결과')&&notice.includes('실제 AI 분석은 아직 연결되지 않았어요'),'P03-T55');
 }
 for(const mobile of [false,true]){
  const pre=mobile?'m-':'';
  await go(`${pre}S3-compare.html`,mobile);await cards();await buttons();await highlights(false);
  writeFileSync(`${output}/${pre}before-comparison.png`,await p.screenshot({fullPage:true}));
  await click('나의 이력서 수정','link');
  // Current main gates desktop resume only; mobile still opens its prototype directly.
  if(mobile){await p.waitForURL(/m-S5-resume\.html/);assert((await p.evaluate(()=>location.pathname)).endsWith('m-S5-resume.html'));}
  else {await p.waitForURL(/L1-login\.html/);assert((await p.evaluate(()=>location.pathname)).endsWith('/L1-login.html'));assert.equal(await p.evaluate(()=>new URLSearchParams(location.search).get('next')),'S5-resume.html');}
  await go(`${pre}S3-compare.html`,mobile);await click('AI로 비교하기');await cards();await highlights(true);
  const before=await state();
  for(const close of ['닫기','공고 비교로 돌아가기','Escape']){
   await click('트렌드 보기 ›');assert.equal(await p.evaluate(()=>document.querySelectorAll('[role=dialog]').length),1);
   assert((await p.evaluate(()=>document.querySelector('[role=dialog]').textContent)).includes('출처:'));
   if(close==='Escape') await p.keyboard.press('Escape');else await click(close);assert.deepEqual(await state(),before);await highlights(true);
  }
  writeFileSync(`${output}/${pre}result.png`,await p.screenshot({fullPage:true}));
  await click('다시 비교');await cards();await buttons();await highlights(false);
  await go(`${pre}S3-compare.html`,mobile,'#result');await cards();await highlights(true);const direct=await state();await click('트렌드 보기 ›');await click('닫기');assert.deepEqual(await state(),direct);
  await click('프로젝트 ›','link');await p.waitForURL(/S4-activity\.html/);assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S4-activity.html`));
  await go(`${pre}S1-list.html`,mobile,'#trend');
  const listPopup=await p.evaluate(()=>document.querySelector('[role=dialog]').textContent);
  await click('닫기');assert.equal(await p.evaluate(()=>document.querySelectorAll('[role=dialog]').length),0);
  await go(`${pre}S1-list.html`,mobile,'#trend');await click('공고 목록으로 돌아가기');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S1-list.html`));
  await click('비교하기','link',true);await cards();
  await go(mobile?'m-Main.html':'index.html',mobile,'#trend');await click('닫기');assert((await p.evaluate(()=>location.pathname)).endsWith(mobile?'m-Main.html':'index.html'));
  await go(mobile?'m-Main.html':'index.html',mobile,'#trend');await click('이 직무 공고 보기','link');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S1-list.html`));
  await go(`${pre}P1-trend.html`,mobile);await click('공고 목록으로 돌아가기');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S1-list.html`));
  await go(`${pre}S3-compare.html`,mobile,'#result');await click('트렌드 보기 ›');const comparePopup=await p.evaluate(()=>document.querySelector('[role=dialog]').textContent);assert.equal(comparePopup.replace('공고 비교로 돌아가기','공고 목록으로 돌아가기'),listPopup);
  passed.push(`${mobile?'mobile':'desktop'}: P03-T01~T13,T15,T17~T21,T26,T28,T32~T34,T55,T56,T58,T59,T60~T65 (T19 complete state only)`);console.log(passed.at(-1));
 }
 await go('m-S3-compare.html',true,'',320);await cards();await buttons();await highlights(false);await click('AI로 비교하기');await cards();await highlights(true);writeFileSync(`${output}/mobile-320.png`,await p.screenshot({fullPage:true}));passed.push('P03-T11,T25,T33~T35,T55: 320px');
 if(process.env.QA_FIXTURES){for(const kind of ['empty','long']){for(const width of [1440,390,320]){
  await go(`${width===1440?'':'m-'}S3-compare.html`,width!==1440,'#result',width,resolve(process.env.QA_FIXTURES,kind));await cards();
  if(kind==='empty') assert.equal(await p.evaluate(()=>[...document.querySelectorAll('article section')].filter(e=>e.textContent.includes('공고에 기재된 내용이 없어요')).length),4);
  else {
   await highlights(true);
   const bounds=await p.evaluate(()=>({width:innerWidth,overflow:[...document.querySelectorAll('article section')].filter(e=>e.scrollWidth>e.clientWidth).map(e=>({title:e.getAttribute('aria-label'),scroll:e.scrollWidth,client:e.clientWidth}))}));
   assert.equal(bounds.width,width);assert.deepEqual(bounds.overflow,[],'P03-T57 fixed viewport overflow');
   writeFileSync(`${output}/long-${width}-result.png`,await p.screenshot({fullPage:true}));
   // Full-page captures temporarily resize the viewport; restore before more assertions.
   await omowright.repinViewport(p,{width,height:900});await p.snapshot();
   await click('다시 비교');await buttons();await highlights(false);
  }
  writeFileSync(`${output}/${kind}-${width}.png`,await p.screenshot({fullPage:true}));passed.push(`${kind} fixture ${kind==='empty'?'P03-T24':'P03-T14,T25,T35'} at ${width}px; P03-T57/T59/T62/T63`);
 }}}
 writeFileSync(`${output}/results.json`,JSON.stringify({passed,blocked:['T16','T19 processing','T22','T23','T27','T30'],notRun:['T29','T31']},null,2));
 console.log('PASS',passed);
} finally {await browser.close();rmSync(profile,{recursive:true,force:true});}
