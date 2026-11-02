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
 for(const width of [1440,390,320]){
  const mobile=width!==1440;await go(`${mobile?'m-':''}S3-compare.html`,mobile,'#result',width);
  await click('트렌드 보기 ›');
  await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));
  assert.equal(await p.evaluate(()=>document.activeElement?.getAttribute('aria-label')),'닫기','P03-T51 initial focus');
  await p.keyboard.press('Shift+Tab');assert.equal(await p.evaluate(()=>document.activeElement.textContent.trim()),'공고 비교로 돌아가기');
  await p.keyboard.press('Tab');assert.equal(await p.evaluate(()=>document.activeElement.getAttribute('aria-label')),'닫기');
  await p.keyboard.press('Escape');await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));
  assert.equal(await p.evaluate(()=>document.querySelectorAll('[role=dialog]').length),0,'P03-T50 Escape');
  assert.equal(await p.evaluate(()=>document.activeElement.id),'p03-trend-trigger');
  for(const close of ['닫기','공고 비교로 돌아가기']){
   await click('트렌드 보기 ›');await click(close);await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));assert.equal(await p.evaluate(()=>document.activeElement.id),'p03-trend-trigger');
  }
  // The detached trigger fallback is a deliberately isolated DOM edge-case fixture.
  await click('트렌드 보기 ›');
  await p.evaluate(()=>{const trigger=document.getElementById('dc').content.querySelector('#p03-trend-trigger');trigger.remove();});
  await p.keyboard.press('Escape');await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));
  assert.equal(await p.evaluate(()=>document.activeElement.id),'p03-posting','P03-T52 fallback');
  passed.push(`P03-T50,T51,T52 ${width}px`);
 }
 writeFileSync(`${output}/keyboard-results.json`,JSON.stringify({passed},null,2));console.log('PASS',passed);
} finally {await browser.close();rmSync(profile,{recursive:true,force:true});}
