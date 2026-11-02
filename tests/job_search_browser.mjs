import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
const {loadOmowright}=await import(pathToFileURL(process.env.OMOWRIGHT_LOADER).href);
const {omowright}=await loadOmowright();
const root=fileURLToPath(new URL('../prototype/',import.meta.url));
const fixtures=process.env.QA_FIXTURES;
const jobs=JSON.parse(readFileSync(resolve(fixtures,'jobs.json')));
const output='/tmp/illo-p02-qa';mkdirSync(output,{recursive:true});
const profile=mkdtempSync('/tmp/illo-p02-browser-');
const browser=await omowright.connectPipe({browserPath:process.env.CHROME_PATH,browserArgs:['--headless','--no-sandbox',`--user-data-dir=${profile}`],storageRoot:profile});
const passed=[];
try {
 const p=await browser.newTab('about:blank');
 async function go(mobile,dir=root,hash='',width=mobile?390:1440,name=mobile?'m-S1-list.html':'S1-list.html'){
  await p.goto('about:blank',{waitUntil:'commit'});
  await p.goto(`${pathToFileURL(resolve(dir,name))}?view=${mobile?'mobile':'desktop'}${hash}`);
  await omowright.repinViewport(p,{width,height:900});await p.snapshot();
 }
 async function action(label,role='button',value){
  let tree=omowright.compactSnapshot(await p.snapshot());let line=tree.split('\n').find(l=>l.includes(`${role} "${label}"`)&&l.includes('ref='));
  if(!line){await p.mouse.move(180,300);await p.mouse.wheel(0,-10000);await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));tree=omowright.compactSnapshot(await p.snapshot());line=tree.split('\n').find(l=>l.includes(`${role} "${label}"`)&&l.includes('ref='));}
  assert(line,`Missing ${role} ${label}\n${tree}`);const el=p.locator(line.match(/ref=(\w+)/)[1]);
  if(value===undefined)await el.click();else {await el.fill(value);await p.keyboard.press('Tab');}
 }
 const body=()=>p.evaluate(()=>document.body.innerText);
 const titles=()=>p.evaluate(()=>[...document.querySelectorAll('span')].filter(e=>/^테스트 공고\d+$/.test(e.textContent)&&e.children.length===0).map(e=>e.textContent));
 const entries=()=>p.evaluate(()=>[...document.querySelectorAll('[aria-labelledby$="list"] span')].filter(e=>e.textContent.startsWith('내 경험과 겹치는 역량 ')&&e.children.length===0).map(e=>Number(e.textContent.split(' ').at(-1))));
 for(const mobile of [false,true]){
  await go(mobile);
  const savedBefore=await p.evaluate(()=>document.querySelectorAll('button[aria-label="저장 해제"]').length);
  await action('저장');assert.equal(await p.evaluate(()=>document.querySelectorAll('button[aria-label="저장 해제"]').length),savedBefore+1);
  for(const [key,label] of jobs){
   await action(label);const text=await body();assert.equal(await p.evaluate(()=>document.querySelector('h1').textContent),label);
   assert(!text.includes('이력서를 등록해주세요'));assert(key==='sns'?text.includes('내 경험과 겹치는 역량'):text.includes('역량 분석 준비 중'));assert(!text.includes('체크했어요'));assert(key==='sns'?!text.includes('현재는 최신순이에요'):text.includes('현재는 최신순이에요'));
   const colors=await p.evaluate(()=>[...document.querySelectorAll('[aria-labelledby$="list"] span')].filter(e=>e.textContent==='역량 분석 준비 중').map(e=>getComputedStyle(e).backgroundColor));assert((key==='sns'||colors.length>0)&&colors.every(c=>c==='rgb(242, 244, 246)'));
   if(key!=='sns')assert(!text.includes('이 직무 트렌드 보기')&&!text.includes('트렌드 ›'));
  }
  await action('SNS 콘텐츠 마케팅');await action('최신순');assert(!(await body()).includes('현재는 최신순이에요'));
  await action('추천순');await action('회사명, 공고 제목 검색','textbox','일치하지않는가상검색어');assert((await body()).includes('검색 결과가 없어요'));await action('검색어 지우기');
  await action('직무 검색','textbox','회계');assert((await body()).includes('아직 준비 중이에요'));await action('직무 검색','textbox','');
  await action('회사명, 공고 제목 검색','textbox','올리브인터내셔널');await action('비교하기','link');assert((await p.evaluate(()=>location.pathname)).endsWith('S3-compare.html'));
  await action('AI로 비교하기');await action('트렌드 보기 ›');await action('공고 비교로 돌아가기');assert((await body()).includes('다시 비교'));
  await go(mobile,root,'',mobile?390:1440,mobile?'m-S5-resume.html':'S5-resume.html');await action('이력서 저장');
  await go(mobile);assert((await body()).includes('내 경험과 겹치는 역량'));assert(!(await body()).includes('이력서를 등록해주세요'));
  writeFileSync(`${output}/${mobile?'mobile':'desktop'}-default.png`,await p.screenshot({fullPage:true}));
  for(const [key,label] of jobs){
   await go(mobile,resolve(fixtures,'registered'),`#job=${key}`);
   assert.deepEqual((await entries()).slice(0,3),[1,3,2]);assert.equal((await entries()).length,10);
   await action('다음 페이지');const tail=await body();assert(tail.includes('내 경험과 겹치는 역량 0'));assert(tail.includes('역량 분석 준비 중'));
   await action('최신순');assert.equal((await titles())[0],'테스트 공고12');
   await action('마감 임박순');assert.equal((await titles())[0],'테스트 공고12');
   await action('회사명, 공고 제목 검색','textbox','테스트 공고1');assert(!(await body()).includes('시연 공고'));await action('회사명, 공고 제목 검색','textbox','');
   await action('추천순');assert.deepEqual((await entries()).slice(0,3),[1,3,2]);
   await action('인턴 6');assert(!(await body()).includes('시연 공고'));await action('전체 13');
  }
  await go(mobile,resolve(fixtures,'empty'));assert((await body()).includes('이력서를 등록해주세요'));assert.equal((await entries()).length,0);
  await go(mobile,resolve(fixtures,'pending'));assert((await body()).includes('역량 분석 준비 중이에요. 현재는 최신순이에요'));assert.equal((await entries()).length,0);
  passed.push(`${mobile?'mobile':'desktop'}: 7 jobs, unregistered/registered/pending, sorting, paging, search, resume and comparison flow`);console.log(passed.at(-1));
 }
 await go(true,root,'',320);assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 writeFileSync(`${output}/mobile-320.png`,await p.screenshot({fullPage:true}));passed.push('320px: no page overflow');
 writeFileSync(`${output}/results.json`,JSON.stringify({passed,blocked:['real P05 persistence','real job skill extraction']},null,2));console.log('PASS P02',passed);
} finally {await browser.close();rmSync(profile,{recursive:true,force:true});}
