import puppeteer from 'puppeteer';
const browser = await puppeteer.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 375, height: 812 });
await page.goto('http://localhost:3000', { waitUntil: 'networkidle2', timeout: 30000 });
await page.screenshot({ path: '/home/user/GlobalChay/temporary screenshots/screenshot-mobile.png', fullPage: true });
await browser.close();
console.log('Saved.');
