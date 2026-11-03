// Demonstration data only. New rows arrive exclusively when the real refresh
// button is clicked; the page never starts its own refresh or click timer.
const c=JSON.parse(document.getElementById('demoCopy').textContent);
const rows=document.getElementById('orderRows');
const search=document.getElementById('orderSearch');
const refresh=document.getElementById('refreshOrders');
const icons=[
 '<path d="m7 5 6-2 6 7-8 3-4-8Zm4 8-4 7m-4 1h12m-8-1 5-6"/>',
 '<path d="M5 8h14l1 13H4L5 8Zm4 0V6a3 3 0 0 1 6 0v2"/>',
 '<path d="M4 5h13v10a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V5Zm13 1h2a3 3 0 0 1 0 6h-2M3 22h17"/>',
 '<path d="M4 14V11a8 8 0 0 1 16 0v3M4 12h3v8H5a2 2 0 0 1-2-2v-4a2 2 0 0 1 1-2Zm16 0h-3v8h2a2 2 0 0 0 2-2v-4a2 2 0 0 0-1-2Z"/>',
 '<path d="M6 3h14v18H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2ZM8 3v18m4-13h5m-5 4h5"/>',
 '<path d="M9 2h6v4l3 3v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V9l3-3V2Zm-3 9h12M9 4h6"/>'
];
const sample=Array.from({length:24},(_,i)=>({id:1048-i,item:i%6,status:i%3===2?'shipped':'pending',minutes:4+i*3,fresh:false}));
let orders=[...sample],status='all',limit=6,refreshes=0,page=1;
const number=n=>new Intl.NumberFormat(document.documentElement.lang).format(n);
const format=(text,values)=>text.replace(/\{(\w+)\}/g,(_,key)=>number(values[key]));
const escape=text=>text.replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
function filtered(){const query=search.value.trim().toLocaleLowerCase();return orders.filter(order=>(status==='all'||order.status===status)&&(!query||c.products[order.item].toLocaleLowerCase().includes(query)||String(order.id).includes(query)));}
function render(){
 const matches=filtered(),visible=matches.slice(0,limit);
 rows.innerHTML=visible.map(order=>`<tr data-order="${order.id}" class="${order.fresh?'is-new':''}"><td class="order-id"><bdi>#${order.id}</bdi></td><td><div class="product-cell"><span class="product-icon tone-${order.item%4}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">${icons[order.item]}</svg></span><span><span class="product-name">${escape(c.products[order.item])}${order.fresh?`<span class="new-tag">${escape(c.new)}</span>`:''}</span><span class="product-sku"><bdi>LM-${['101','204','302','410','516','602'][order.item]}</bdi></span></span></div></td><td><span class="status-tag ${order.status}">${escape(c[order.status])}</span></td><td class="time-cell">${escape(order.fresh?c.now:format(c.minutes,{n:order.minutes}))}</td></tr>`).join('');
 if(!visible.length) rows.innerHTML=`<tr><td colspan="4" class="empty">${escape(c.empty)}</td></tr>`;
 document.getElementById('pendingCount').textContent=number(orders.filter(o=>o.status==='pending').length);
 document.getElementById('shippedCount').textContent=number(orders.filter(o=>o.status==='shipped').length);
 document.getElementById('matchingCount').textContent=number(matches.length);
 document.getElementById('pendingBadge').textContent=number(orders.filter(o=>o.status==='pending').length);
 document.getElementById('showing').textContent=format(c.showing,{n:visible.length,total:matches.length});
 document.getElementById('loadMore').disabled=limit>=matches.length;
 document.getElementById('clearFilters').hidden=status==='all'&&!search.value;
 document.querySelectorAll('[data-status]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.status===status)));
 document.documentElement.dataset.refreshCount=String(refreshes);
 document.documentElement.dataset.page=String(page);
}
document.querySelectorAll('[data-status]').forEach(button=>button.addEventListener('click',()=>{status=button.dataset.status;limit=6;page=1;render();}));
search.addEventListener('input',()=>{limit=6;page=1;render();});
search.addEventListener('keydown',event=>{if(event.key==='Enter'&&!event.isComposing){event.preventDefault();search.blur();}});
document.getElementById('clearFilters').addEventListener('click',()=>{status='all';search.value='';limit=6;page=1;render();});
refresh.addEventListener('click',()=>{
 refreshes++;
 orders=orders.map(order=>({...order,fresh:false}));
 orders.unshift({id:1048+refreshes*2,item:0,status:'pending',minutes:0,fresh:true},{id:1047+refreshes*2,item:2,status:'pending',minutes:0,fresh:true});
 const sync=document.getElementById('syncStatus');sync.textContent=format(c.newOrders,{n:2});sync.classList.add('received');
 refresh.classList.remove('refreshed');void refresh.offsetWidth;refresh.classList.add('refreshed');render();
});
function advance(event){event.preventDefault();if(limit>=filtered().length)return;page++;limit+=6;render();}
document.getElementById('loadMore').addEventListener('click',advance);
document.getElementById('language').addEventListener('change',event=>{location.href=`./repeat-${event.target.value.toLowerCase()}.html`;});
render();
