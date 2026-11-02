"""P02 production JS logic executed with synthetic inputs, without a browser."""
import json
import subprocess
import unittest
from screen_loader import load_screens


class JobSearchTests(unittest.TestCase):
    def test_P02_T21_mobile_title_before_controls(self):
        html = load_screens()['boards']['m-S1-list.dc.html'][1]
        self.assertLess(html.index('<h1'), html.index('aria-label="직무 검색"'))

    def test_P02_T04_T20_state_sort_and_page_contract(self):
        ns = load_screens()
        harness = r'''
const assert = require('node:assert/strict');
const page = new Page();
const profile = {resumeContent:['작성된 경험'],resumeSkillIds:['a','a','b','c']};
assert.deepEqual(page.matchState({postingSkillIds:['a','a','b']},profile), {status:'analyzed',count:2});
assert.deepEqual(page.matchState({postingSkillIds:[]},profile), {status:'analyzed',count:0});
for(const invalid of [null,undefined,[''],[3],{}]) assert.equal(page.matchState({postingSkillIds:invalid},profile).status,'pending');
assert.equal(page.matchState({postingSkillIds:['a']},{resumeContent:[]}).status,'unregistered');
assert.equal(page.hasResumeContent({resumeContent:['', '  ']}),false);
assert.equal(page.hasResumeContent({resumeContent:['', '일부 작성']}),true);
assert.equal(page.hasResumeContent({resumeRegistered:true,resumeContent:[]}),false);
assert.equal(page.matchState({presetOverlapSkillIds:['a']},{...profile,seedId:'other'}).status,'pending');
assert.equal(page.matchState({presetOverlapSkillIds:['a','a']},{...profile,seedId:'preset-resume-v1'}).count,1);
const posts = [
{id:'demo',demo:true,cr:900,postingSkillIds:['a']},
{id:'three',cr:100,postingSkillIds:['a','b','c']},
{id:'two-old',cr:100,postingSkillIds:['a','b']},
{id:'two-new',cr:200,postingSkillIds:['a','b']},
{id:'zero',cr:300,postingSkillIds:[]},
{id:'pending',cr:1000},
{id:'two-undated',cr:0,postingSkillIds:['a','b']},
{id:'two-stable',cr:0,postingSkillIds:['a','b']}
];
const original=JSON.stringify(posts);
assert.deepEqual(page.rankPosts(posts,profile,'rec').map(p=>p.id),['demo','three','two-new','two-old','two-undated','two-stable','zero','pending']);
assert.equal(JSON.stringify(posts),original);
assert.equal(page.rankPosts(posts,{resumeContent:[]},'rec')[0].id,'demo');
assert.equal(page.rankPosts(posts,profile,'new')[0].id,'pending');
const seed=JSON.parse(process.env.PROFILE_DATA);
const data=JSON.parse(process.env.JOB_DATA);
for(const job of Object.keys(data)) {
 if(job==='sns')for(const post of data[job].posts)assert.equal(page.matchState(post,seed).count,post.ov);
 page.state.job=job;page.state.sort='rec';
 const view=page.renderVals();
 assert.equal(view.jobName,data[job].label);
 assert(view.rows.every(p=>job==='sns' ? p.ov.startsWith('내 경험과 겹치는 역량 ') : p.ov==='역량 분석 준비 중'));
 assert(!view.unregistered);
 assert(job==='sns' ? view.sortNote==='' : view.sortNote.includes('최신순'));
 const dates=data[job].posts.map(p=>p.cr).filter(n=>Number.isFinite(n)&&n>0);
 if(dates.length) assert.equal(view.rows[0].t,data[job].posts.slice().sort((a,b)=>Number(b.demo===true)-Number(a.demo===true)||(job==='sns'?b.ov-a.ov:0)||b.cr-a.cr)[0].t);
 page.state.sort='rec';
 page.state.page=2;page.renderVals().sort.new.go();assert.equal(page.state.page,1);
 page.state.page=2;page.renderVals().setQ({target:{value:'NOTFOUND_TEST'}});assert.equal(page.state.page,1);assert.equal(page.renderVals().rows.length,0);
 page.renderVals().clearQ();assert(page.renderVals().rows.length<=10);
}
console.log('PASS P02 logic: match states, stable sorting, 7 jobs, search, pagination reset');
'''
        script = "class Base {setState(v){Object.assign(this.state,v)} sv(){return {}}}\nclass Page extends Base {" + ns['LIST_JS'] + "}\n" + harness
        script = script.replace('JSON.parse(process.env.JOB_DATA)', ns['JOBS_JSON']).replace('JSON.parse(process.env.PROFILE_DATA)', ns['PROFILE_JSON'])
        result = subprocess.run(['node'], input=script, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
