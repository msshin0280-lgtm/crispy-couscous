const DATA = {
  linkedin: "https://www.linkedin.com/",
  metrics: {reports: 6, topics: 4, qualifications: 5, activities: 5},
  reports: [
    {type:"기업분석",title:"삼성전자 재무 분석 대시보드",workflow:"DART API · Python · Dashboard",date:"2026.09",desc:"OpenDART 데이터를 자동 수집하고 매출·영업이익·순이익 및 재무비율을 계산해 대시보드로 표현.",url:"../dashboard/"},
    {type:"기업분석",title:"AI 기업분석 Report Workflow",workflow:"AI · Research · Automation",date:"2026.09",desc:"기업 자료 수집부터 핵심 지표 정리와 보고서 작성까지 반복 가능한 workflow로 구조화.",url:"#"},
    {type:"시장분석",title:"산업 동향 및 시장 리서치",workflow:"AI · Web Research",date:"2026.08",desc:"뉴스와 공개자료를 수집해 산업 변화와 주요 이슈를 요약하고 비교.",url:"#"},
    {type:"데이터분석",title:"KPI 기반 기업 비교 분석",workflow:"Python · Data Visualization",date:"2026.07",desc:"핵심 지표를 표준화하고 비교 가능한 형태로 시각화.",url:"#"},
    {type:"리서치",title:"AI 기반 보고서 생성 Workflow",workflow:"LLM · Prompt · Automation",date:"2026.06",desc:"수집 → 정제 → 분석 → 요약 → 보고서의 과정을 하나의 작업 흐름으로 정리.",url:"#"},
    {type:"리서치",title:"뉴스 모니터링 및 요약",workflow:"AI · Automation",date:"2026.05",desc:"반복적인 정보 탐색을 줄이고 핵심 정보만 빠르게 확인하는 구조를 설계.",url:"#"}
  ],
  qualifications: [
    {name:"간호학 전공교육",org:"한림성심대학교 간호학과",date:"2023 — Present",type:"Education"},
    {name:"말초정맥 술기 프로그램",org:"Clinical Skills Training",date:"2026",type:"Training"},
    {name:"임상실습",org:"Healthcare / Clinical Practice",date:"2026",type:"Clinical"},
    {name:"국가근로",org:"병원 간호부",date:"Experience",type:"Experience"},
    {name:"자격증 / 수료증",org:"추가 입력 가능",date:"—",type:"Certification"}
  ],
  activities: [
    {date:"2026.09",title:"AI 기업분석 & Portfolio Dashboard",type:"Project",desc:"OpenDART 기반 분석 프로젝트를 포트폴리오 대시보드로 확장."},
    {date:"2026.08",title:"AI / Data Research",type:"Research",desc:"기업·산업 자료를 수집하고 AI를 활용해 분석·요약하는 workflow 구축."},
    {date:"2026.07",title:"데이터 시각화 프로젝트",type:"Project",desc:"핵심 지표를 카드·그래프·테이블로 연결해 읽기 쉬운 화면으로 구성."},
    {date:"2026.06",title:"교내외 활동 및 프로젝트",type:"Activity",desc:"전공과 데이터·AI 관심사를 연결하는 프로젝트 및 활동 참여."},
    {date:"2026.05",title:"개인 포트폴리오 구축",type:"Portfolio",desc:"분석 결과물과 경험을 재사용 가능한 데이터 구조로 정리."}
  ]
};

const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];

function metric(label,value,note){return `<div class="metric"><span>${label}</span><strong>${value}</strong><small>${note}</small></div>`}

function renderMetrics(){
  $("#overviewMetrics").innerHTML=[
    metric("AI-GENERATED REPORTS",DATA.metrics.reports+"+","기업·시장·리서치"),
    metric("RESEARCH TOPICS",DATA.metrics.topics+"+","분석 영역"),
    metric("QUALIFICATIONS",DATA.metrics.qualifications+"+","교육·훈련·인증"),
    metric("ACTIVITIES",DATA.metrics.activities+"+","프로젝트·활동")
  ].join("");
  $("#reportMetrics").innerHTML=[
    metric("TOTAL REPORTS",DATA.reports.length+"+","등록 산출물"),
    metric("AUTOMATED WORKFLOW","5+","AI / Python / Data"),
    metric("REPORT TYPES",new Set(DATA.reports.map(x=>x.type)).size,"분석 카테고리"),
    metric("SOURCE","GitHub","crispy-couscous")
  ].join("");
  $("#qualificationMetrics").innerHTML=[
    metric("TOTAL",DATA.qualifications.length+"+","등록 항목"),
    metric("EDUCATION","1+","전공 교육"),
    metric("TRAINING","2+","실무·임상 교육"),
    metric("STATUS","ACTIVE","계속 업데이트")
  ].join("");
}

function renderRecent(){
 $("#recentReports").innerHTML=DATA.reports.slice(0,5).map(r=>`<tr><td><span class="type-tag">${r.type}</span></td><td><b>${r.title}</b></td><td>${r.workflow}</td><td>${r.date}</td><td><a href="${r.url}" target="_blank">↗</a></td></tr>`).join("");
}

function renderReports(filter="전체",query=""){
 const types=["전체",...new Set(DATA.reports.map(r=>r.type))];
 $("#reportFilters").innerHTML=`<div class="filters">${types.map(t=>`<button class="filter ${t===filter?"active":""}" data-filter="${t}">${t}</button>`).join("")}</div>`;
 $$("#reportFilters .filter").forEach(b=>b.onclick=()=>renderReports(b.dataset.filter,$("#reportSearch").value));
 const q=query.toLowerCase();
 const list=DATA.reports.filter(r=>(filter==="전체"||r.type===filter)&&(!q||(r.title+r.desc+r.workflow).toLowerCase().includes(q)));
 $("#reportGrid").innerHTML=list.map((r,i)=>`<article class="report-card"><div class="report-no">${String(i+1).padStart(2,"0")}</div><span class="type-tag">${r.type}</span><h3>${r.title}</h3><p>${r.desc}</p><div class="meta"><span>${r.workflow}</span><span>${r.date}</span></div><a href="${r.url}" target="_blank">PROJECT / REPORT ↗</a></article>`).join("")||`<div class="panel">검색 결과가 없습니다.</div>`;
}

function renderQualifications(){
 $("#qualificationGrid").innerHTML=DATA.qualifications.map((q,i)=>`<article class="qualification-card"><div class="icon">${String(i+1).padStart(2,"0")}</div><b>${q.type}</b><h3>${q.name}</h3><p>${q.org}</p><small>${q.date}</small></article>`).join("");
}

function renderActivities(){
 $("#activityTimeline").innerHTML=DATA.activities.map(a=>`<div class="activity-item"><div class="activity-date">${a.date}</div><div class="activity-dot"></div><div class="activity-body"><b>${a.title}</b><span>${a.type} · ${a.desc}</span></div></div>`).join("");
 const counts={};DATA.activities.forEach(a=>counts[a.type]=(counts[a.type]||0)+1);
 $("#activitySummary").innerHTML=Object.entries(counts).map(([k,v])=>`<div class="summary-row"><span>${k}</span><b>${v}</b></div>`).join("");
}

function charts(){
 const ctx=$("#activityChart");
 new Chart(ctx,{type:"line",data:{labels:["04","05","06","07","08","09"],datasets:[{label:"Projects / Research",data:[1,2,3,4,5,7],borderColor:"#1764c0",backgroundColor:"#1764c018",fill:true,tension:.35,pointRadius:3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:"#edf1f5"},ticks:{stepSize:2}},x:{grid:{display:false}}}}});
 new Chart($("#focusChart"),{type:"doughnut",data:{labels:["AI / Data","Healthcare","Research","Activities"],datasets:[{data:[35,25,25,15],backgroundColor:["#1764c0","#20a47b","#e99a36","#765bd6"],borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,cutout:"68%",plugins:{legend:{position:"bottom",labels:{boxWidth:10,font:{size:9}}}}}});
}

const titles={overview:"Portfolio Overview",about:"About Me",reports:"AI Research Dashboard",qualifications:"Qualifications",activities:"Activities"};
function navigate(view){
 $$(".view").forEach(v=>v.classList.toggle("active",v.id===view));
 $$(".nav-item").forEach(v=>v.classList.toggle("active",v.dataset.view===view));
 $("#pageTitle").textContent=titles[view]||"Portfolio Overview";
 window.scrollTo({top:0,behavior:"smooth"});
}
$$(".nav-item").forEach(b=>b.onclick=()=>navigate(b.dataset.view));
$$("[data-jump]").forEach(b=>b.onclick=()=>navigate(b.dataset.jump));
$("#reportSearch").addEventListener("input",e=>{
 const active=$(".filter.active")?.dataset.filter||"전체";renderReports(active,e.target.value);
});

["linkedinSide","linkedinAbout","linkedinIdentity"].forEach(id=>{$("#"+id).href=DATA.linkedin});
renderMetrics();renderRecent();renderReports();renderQualifications();renderActivities();charts();
