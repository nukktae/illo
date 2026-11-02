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
  const missing=styles.filter(s=>s.bg==='rgb(213, 220, 229)');
  if(done){assert(missing.length>0);for(const s of missing){assert.equal(s.color,'rgb(51, 61, 75)');assert.equal(s.decoration,'none');assert.equal(s.radius,'4px');assert.equal(s.weight,'600');assert.equal(s.clone,'clone');assert.equal(s.border,'rgb(107, 118, 132)');assert.equal(s.borderWidth,'1px');}}
  else assert.equal(missing.length,0);
 }
 async function cards(){
  const data=await p.evaluate(()=>{const a=document.querySelector('article');const body=a.querySelector('[aria-label="공고 본문"]');const sections=[...body.querySelectorAll('section')];return {titles:sections.map(e=>e.querySelector('h3').textContent),bodyCount:a.querySelectorAll('[aria-label="공고 본문"]').length,bg:getComputedStyle(body).backgroundColor,borders:sections.slice(1).map(e=>getComputedStyle(e).borderTopWidth),overflow:document.documentElement.scrollWidth>innerWidth};});
  assert.deepEqual(data.titles,['담당업무','자격요건','우대사항','전형절차']);assert.equal(data.bodyCount,1);assert.equal(data.bg,'rgb(255, 255, 255)');assert(data.borders.every(n=>n==='1px'));assert.equal(data.overflow,false);
 }
 async function buttons(){
  const data=await p.evaluate(()=>{const a=[...document.querySelectorAll('a')].find(e=>e.textContent==='나의 이력서 수정');const b=[...document.querySelectorAll('button')].find(e=>e.textContent==='AI로 비교하기');const x=a.getBoundingClientRect(),y=b.getBoundingClientRect();return {sizes:[x.width,y.width,x.height,y.height,x.top-y.bottom],colors:[getComputedStyle(a).backgroundColor,getComputedStyle(b).backgroundColor],small:[...document.querySelectorAll('a')].some(e=>e.textContent==='이력서 수정 ›')};});
  assert(data.sizes[0]<data.sizes[1]);assert.deepEqual(data.sizes.slice(2),[44,54,8]);assert.deepEqual(data.colors,['rgb(255, 255, 255)','rgb(49, 130, 246)']);assert.equal(data.small,false);
  const notice=await p.evaluate(()=>document.querySelector('aside').textContent);assert(notice.includes('시연용 예시 비교 결과')&&notice.includes('실제 AI 분석은 아직 연결되지 않았어요'),'P03-T55');
 }
 for(const mobile of [false,true]){
  const pre=mobile?'m-':'';
  await go(`${pre}S3-compare.html`,mobile);await cards();await buttons();await highlights(false);
  writeFileSync(`${output}/${pre}before-comparison.png`,await p.screenshot({fullPage:true}));
  await click('나의 이력서 수정','link');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S5-resume.html`));
  await go(`${pre}S3-compare.html`,mobile);await click('AI로 비교하기');await cards();await highlights(true);
  const before=await state();
  for(const close of ['닫기','공고 비교로 돌아가기','닫기']){
   await click('트렌드 보기 ›');assert.equal(await p.evaluate(()=>document.querySelectorAll('[role=dialog]').length),1);
   assert((await p.evaluate(()=>document.querySelector('[role=dialog]').textContent)).includes('출처:'));
   await click(close);assert.deepEqual(await state(),before);await highlights(true);
  }
  writeFileSync(`${output}/${pre}result.png`,await p.screenshot({fullPage:true}));
  await click('다시 비교');await cards();await buttons();await highlights(false);
  await go(`${pre}S3-compare.html`,mobile,'#result');await cards();await highlights(true);const direct=await state();await click('트렌드 보기 ›');await click('닫기');assert.deepEqual(await state(),direct);
  await click('프로젝트 ›','link');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S4-activity.html`));
  await go(`${pre}S1-list.html`,mobile,'#trend');
  const listPopup=await p.evaluate(()=>document.querySelector('[role=dialog]').textContent);
  await click('닫기');assert.equal(await p.evaluate(()=>document.querySelectorAll('[role=dialog]').length),0);
  await go(`${pre}S1-list.html`,mobile,'#trend');await click('공고 목록으로 돌아가기');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S1-list.html`));
  await click('비교하기','link',true);await cards();
  await go(mobile?'m-Main.html':'index.html',mobile,'#trend');await click('닫기');assert((await p.evaluate(()=>location.pathname)).endsWith(mobile?'m-Main.html':'index.html'));
  await go(mobile?'m-Main.html':'index.html',mobile,'#trend');await click('이 직무 공고 보기','link');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S1-list.html`));
  await go(`${pre}P1-trend.html`,mobile);await click('공고 목록으로 돌아가기');assert((await p.evaluate(()=>location.pathname)).endsWith(`${pre}S1-list.html`));
  await go(`${pre}S3-compare.html`,mobile,'#result');await click('트렌드 보기 ›');const comparePopup=await p.evaluate(()=>document.querySelector('[role=dialog]').textContent);assert.equal(comparePopup.replace('공고 비교로 돌아가기','공고 목록으로 돌아가기'),listPopup);
  passed.push(`${mobile?'mobile':'desktop'}: P03-T01~T13,T15,T17~T21,T26,T28,T32~T34,T55 (T19 complete state only)`);console.log(passed.at(-1));
 }
 await go('m-S3-compare.html',true,'',320);await cards();await buttons();await highlights(false);await click('AI로 비교하기');await cards();await highlights(true);writeFileSync(`${output}/mobile-320.png`,await p.screenshot({fullPage:true}));passed.push('P03-T11,T25,T33~T35,T55: 320px');
 if(process.env.QA_FIXTURES){for(const kind of ['empty','long']){
  await go('m-S3-compare.html',true,'#result',320,resolve(process.env.QA_FIXTURES,kind));await cards();
  if(kind==='empty') assert.equal(await p.evaluate(()=>[...document.querySelectorAll('article section')].filter(e=>e.textContent.includes('공고에 기재된 내용이 없어요')).length),4);
  else {await highlights(true);assert.equal(await p.evaluate(()=>[...document.querySelectorAll('article section')].some(e=>e.scrollWidth>e.clientWidth)),false);await click('다시 비교');await buttons();}
  writeFileSync(`${output}/${kind}-320.png`,await p.screenshot({fullPage:true}));passed.push(`${kind} fixture ${kind==='empty'?'P03-T24':'P03-T14,T25,T35'} at 320px`);
 }}
 writeFileSync(`${output}/results.json`,JSON.stringify({passed,blocked:['T16','T19 processing','T22','T23','T27','T30'],notRun:['T29','T31']},null,2));
 console.log('PASS',passed);
} finally {await browser.close();rmSync(profile,{recursive:true,force:true});}
