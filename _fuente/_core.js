// ---- Núcleo de factores de ingeniería económica ----
const FP=(i,n)=>Math.pow(1+i,n);
const PF=(i,n)=>1/Math.pow(1+i,n);
const PA=(i,n)=>i===0?n:(Math.pow(1+i,n)-1)/(i*Math.pow(1+i,n));
const AP=(i,n)=>i===0?1/n:i*Math.pow(1+i,n)/(Math.pow(1+i,n)-1);
const FA=(i,n)=>i===0?n:(Math.pow(1+i,n)-1)/i;
const AF=(i,n)=>i===0?1/n:i/(Math.pow(1+i,n)-1);
const PG=(i,n)=>i===0?n*(n-1)/2:(PA(i,n)-n*PF(i,n))/i;
const AG=(i,n)=>i===0?(n-1)/2:1/i-n/(Math.pow(1+i,n)-1);
const Pg=(i,g,n)=>Math.abs(i-g)<1e-10?n/(1+i):(1-Math.pow((1+g)/(1+i),n))/(i-g);
const npv=(i,cf)=>cf.reduce((s,c,t)=>s+c/Math.pow(1+i,t),0);
function irr(cf,lo,hi){lo=lo??-0.9;hi=hi??10;const f=r=>npv(r,cf);let a=lo,b=hi;if(f(a)*f(b)>0)return null;
  for(let k=0;k<200;k++){const m=(a+b)/2;if(f(a)*f(m)<=0)b=m;else a=m;}return (a+b)/2;}
function irrAll(cf){const r=[];let prev=npv(-0.89,cf);
  for(let x=-890;x<=3000;x++){const i=x/1000,cur=npv(i,cf);
    if(prev===0||prev*cur<0){const root=irr(cf,i-0.001,i);if(root!==null)r.push(root);}prev=cur;}
  return r;}
// ---- Formato ----
const money=v=>(v<0?"-":"")+"$"+Math.abs(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const money0=v=>(v<0?"-":"")+"$"+Math.abs(v).toLocaleString('en-US',{maximumFractionDigits:0});
const pct=(v,d)=>(v*100).toFixed(d??4)+"%";
const f5=v=>v.toLocaleString('en-US',{minimumFractionDigits:5,maximumFractionDigits:5});
// ---- Tema Plotly común ----
const PL={paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',
  font:{family:'JetBrains Mono, monospace',size:10,color:'#888'},
  xaxis:{gridcolor:'#1a1a1a',zerolinecolor:'#333',linecolor:'#2a2a2a'},
  yaxis:{gridcolor:'#1a1a1a',zerolinecolor:'#333',linecolor:'#2a2a2a'},
  margin:{l:62,r:22,t:28,b:46},showlegend:true,
  legend:{bgcolor:'rgba(0,0,0,0)',font:{size:9},orientation:'h',y:1.14,x:0}};
const PLC={displayModeBar:false,responsive:true};
// ---- Navegación de diapositivas ----
let currentSlide=0,slides,progressBar,counter;
function updateSlides(){
  slides.forEach((s,i)=>i===currentSlide?s.classList.add('active'):s.classList.remove('active'));
  progressBar.style.width=((currentSlide+1)/slides.length)*100+"%";
  counter.innerText=`${currentSlide+1} / ${slides.length}`;
  if(typeof onSlideChange==='function')onSlideChange(currentSlide);
}
function nextSlide(){if(currentSlide<slides.length-1){currentSlide++;updateSlides();}}
function prevSlide(){if(currentSlide>0){currentSlide--;updateSlides();}}
function initNav(){
  slides=document.querySelectorAll('.slide');
  progressBar=document.getElementById('progress-bar');
  counter=document.getElementById('slide-counter');
  window.addEventListener('keydown',e=>{
    if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;
    if(e.key==='ArrowRight'||e.key===' ')nextSlide();
    if(e.key==='ArrowLeft')prevSlide();
  });
  updateSlides();
}
