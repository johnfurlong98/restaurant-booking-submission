// Increase default timeout to 30s so Puppeteer has enough time
jest.setTimeout(30000);

const puppeteer = require('puppeteer');

describe('Basic Puppeteer Test', () => {
  let browser;
  let page;

  // Change this if your Django server runs elsewhere or on a different port
  const baseUrl = 'http://localhost:8000';

  beforeAll(async () => {
    // Launch the browser
    browser = await puppeteer.launch({
      headless: true,
      // slowMo: 100, // Uncomment for debugging (slows actions by 100ms)
    });
    page = await browser.newPage();
  });

  afterAll(async () => {
    // Close the browser if it was successfully launched
    if (browser) {
      await browser.close();
    }
  });

  test('Loads the homepage and checks the title', async () => {
    // Go to the homepage
    await page.goto(baseUrl);

    // Wait for the <title> or any main element to load
    // (optional step, but good practice)
    await page.waitForSelector('title');

    // Get the title text
    const title = await page.title();
    // Adjust this string to match your site’s <title> exactly
    expect(title).toMatch(/Restaurant Booking/i);
  });

  // Optional second test: Just check if a “Make a Booking” link exists
  test('Checks if "Make a Booking" link is on the homepage', async () => {
    await page.goto(baseUrl);
    // Wait for the navbar or link
    await page.waitForSelector('nav.navbar');

    // Does the link exist in the DOM?
    const bookingLink = await page.$('a[href="/bookings/create/"]');
    expect(bookingLink).not.toBeNull();
  });
});
