const puppeteer = require('puppeteer');

(async () => {
  // Launch a headless browser
  const browser = await puppeteer.launch({ headless: true }); // Set to false to see the browser
  const page = await browser.newPage();

  // Go to the form page
  await page.goto('https://www.t-mobile.com/brand/project-10-million-form/start');

  // Fill out the form
  await page.type('[name="firstName"]', 'Eli');
  await page.type('[name="lastName"]', 'Roitblat');
  await page.type('[name="email"]', 'rebar_princes_0d@icloud.com');
  await page.type('[name="confirmEmail"]', 'rebar_princes_0d@icloud.com');

  // Submit the form
  await page.click('button[type="submit"]');

  // Optionally, wait for navigation or confirmation
  // await page.waitForNavigation(); // Uncomment if needed

  console.log('Form submitted successfully with the provided details!');

  // Close the browser
  await browser.close();
})();
