// node make_pdf.js sheet.html out.pdf  (needs playwright)
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.resolve(process.argv[2]));await p.waitForTimeout(800);
await p.pdf({path:process.argv[3],format:'A4',printBackground:true});await b.close();})();
