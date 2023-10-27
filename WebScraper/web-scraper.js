const url = 'https://www.amazon.com/Sennheiser-Open-Back-Professional-Headphone/dp/B00004SY4H'
const puppeteer = require('puppeteer');
const fs = require('fs'); // Import the file system module
const numOfReviews = 10;
let reviewCount = 2;
(async () => {
  // Launch a headless browser
  const browser = await puppeteer.launch();

  // Create a new page
  const page = await browser.newPage();

  const scrapedData = []; // Create an array to store scraped data

  async function scrapePage() {

    // Click on all <a> elements with data-hook="cr-translate-this-review-link"
    const translateLinks = await page.$$('a[data-hook="cr-translate-these-reviews-link"]');
    if (translateLinks && translateLinks.length > 0) {
      await translateLinks[0].click();
      await page.waitForSelector('a[data-hook="cr-see-original-reviews-link"]');
    }
    // Scrape data from elements with data-hook="review"
    const reviews = await page.$$eval('div[data-hook="review"]', (reviewElements) => {
      return reviewElements.map((reviewElement) => {
        const reviewBody = reviewElement.querySelector('span[data-hook="review-body"]');
        let content = '';

        if (reviewBody) {
          const translatedContent = reviewBody.querySelector('span.cr-translated-review-content');
          content = translatedContent ? translatedContent.textContent : reviewBody.textContent;
          content = content.replace(/\n/g, ' ').trim("\"");
        }

        return content;
      });
    });

    console.log(reviews);
    // Append the reviews to our reviews array
    scrapedData.push(...reviews);


    // Check for pagination
    const pagination = await page.$('ul.a-pagination');
    if (pagination) {
      const nextButtonDisabled = await pagination.$('li.a-last.a-disabled');
      if (reviewCount > numOfReviews || nextButtonDisabled) {
        console.log('No more pages to scrape.');
        return;
      }

      const nextButtonEnabled = await pagination.$('li.a-last:not(.a-disabled) a');
      if (nextButtonEnabled) {
        await nextButtonEnabled.click();
        await page.waitForTimeout(2000);
        console.log('Clicked on next page ' + reviewCount);
        reviewCount++;
        await scrapePage(); // Recursively scrape the next page
      }
    } else {
      console.log('No pagination found');
    }
  }

  // Navigate to the webpage
  await page.goto(url);

  // Find and click the link with data-hook="see-all-reviews-link-foot"
  const seeAllReviewsLink = await page.$('a[data-hook="see-all-reviews-link-foot"]');
  if (seeAllReviewsLink) {
    await seeAllReviewsLink.click();
    await page.waitForNavigation();
  } else {
    console.error('See all reviews link not found');
    browser.close();
    return;
  }

  // Start scraping
  await scrapePage();


  // Close the browser
  await browser.close();

   // Save the scraped data to a text file
   fs.writeFileSync('scraped_data.txt', scrapedData.join('\n'), 'utf-8', (err) => {
    if (err) {
      console.error('Error writing to file:', err);
    } 
  });

  console.log('Scraped data saved to scraped_data.txt');

})();

