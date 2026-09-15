const state={posts:[],channels:[]};
const $=s=>document.querySelector(s);

async function getJSON(url){
  const r=await fetch(url,{headers:{Accept:"application/json"}});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
function escapeHTML(s=""){return s.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function dateText(v){try{return new Date(v).toLocaleString(undefined,{dateStyle:"medium",timeStyle:"short"});}catch{return ""}}
function renderChannels(){
  const nav=$("#channelsTop");
  nav.innerHTML=state.channels.slice(0,4).map(c=>`<a href="${escapeHTML(c.url)}" target="_blank" rel="noopener">${escapeHTML(c.name)}</a>`).join("");
  const main=state.channels.find(c=>c.is_main);
  if(main) $("#telegramMain").href=main.url;
  else if(state.channels[0]) $("#telegramMain").href=state.channels[0].url;
}
function render(){
  const q=$("#search").value.trim().toLowerCase();
  const items=state.posts.filter(p=>(p.title+" "+p.content).toLowerCase().includes(q));
  $("#status").textContent=`${items.length} update${items.length===1?"":"s"}`;
  $("#empty").hidden=items.length!==0;
  $("#posts").innerHTML=items.map(p=>{
    const image=p.image_url?`<img class="poster" src="${escapeHTML(p.image_url)}" alt="" loading="lazy">`:`<div class="poster"></div>`;
    const link=p.message_url||"#";
    return `<article class="card">${image}<div class="body"><h4>${escapeHTML(p.title||"New Update")}</h4><p>${escapeHTML(p.content||"")}</p><div class="meta"><span>${escapeHTML(p.category||"Update")}</span><span>${dateText(p.published_at)}</span></div>${link!=="#" ? `<a class="watch" href="${escapeHTML(link)}" target="_blank" rel="noopener">Open Telegram Post →</a>`:""}</div></article>`;
  }).join("");
}
async function load(){
  $("#status").textContent="Loading…";
  try{
    const data=await getJSON("/api/posts");
    state.posts=data.posts||[]; state.channels=data.channels||[];
    renderChannels(); render();
  }catch(e){
    console.error(e); $("#status").textContent="Could not load updates";
    $("#empty").hidden=false; $("#empty").textContent="Database is not configured yet. Check the Vercel environment variables.";
  }
}
$("#search").addEventListener("input",render);
$("#refresh").addEventListener("click",load);
load();
