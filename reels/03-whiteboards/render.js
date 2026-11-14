const {chromium}=require('playwright');
(async()=>{const [,,html,out]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+html);await p.waitForTimeout(800);const T=await p.evaluate(()=>window.TOTAL);const fps=30,n=Math.round(T*fps);
for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/fps);await p.screenshot({path:`${out}/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();console.log(n)})();
