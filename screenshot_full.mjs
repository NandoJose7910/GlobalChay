import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await puppeteer.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto('http://localhost:3000/#aliados', { waitUntil: 'networkidle2', timeout: 30000 });
// scroll to aliados section
await page.evaluate(() => {
  document.getElementById('aliados')?.scrollIntoView();
});
await new Promise(r => setTimeout(r, 800));
const outFile = path.join(__dirname, 'temporary screenshots', 'aliados-full.png');
await page.screenshot({ path: outFile, fullPage: false });
await browser.close();
console.log('Saved:', outFile);
