//testurl = 'https://www.amazon.com/Sennheiser-Open-Back-Professional-Headphone/dp/B00004SY4H'
//To run this script, type the following command in the terminal:
//node web-scraper.js <testurl> <outputFilePath>
const puppeteer = require('puppeteer');
const fs = require('fs'); // Import the file system module
const getCategory = require(__dirname+'/get-category.js');
const categoriesFilePath = 'MLModel/data/categories.txt';
const numOfReviews = 10;
let reviewCount = 2;
(async () => {

  // Check if the user provided a URL and output file path as command-line arguments
  if (process.argv.length !== 4) {
    console.error('Usage: node web-scraper.js <URL> <outputFilePath>');
    return 'Usage: node web-scraper.js <URL> <outputFilePath>';
  }

  const url = process.argv[2]; // Get the URL from the command-line argument
  const outputFilePath = process.argv[3]; // Get the output file path from the command-line argument


  // Launch a headless browser
  const browser = await puppeteer.launch({
    args: ['--no-sandbox']
  });

  // Create a new page
  const page = await browser.newPage();

  const scrapedData = []; // Create an array to store scraped data

  let category = '';

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
          if (translatedContent)
            content = translatedContent.textContent;
          else {
            const innerSpans = reviewBody.querySelectorAll('span:not([data-hook])'); // Select all inner spans without attributes
            const lastInnerSpan = innerSpans ? innerSpans[innerSpans.length - 1] : null; // Select the last inner span
            content = lastInnerSpan ? lastInnerSpan.textContent : '';
          }
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


  async function findCategory() {
    try {
      // Wait for the product overview div to be present
      await page.waitForSelector('#productOverview_feature_div');

      // Extract information from spans inside spans with class 'a-span3'
      const tds = await page.$$('#productOverview_feature_div .a-span3');

      if (!tds || tds.length === 0) {
        console.error('No elements found with selector #productOverview_feature_div .a-span3');
        return null; // or handle this case accordingly
      }

      console.log('Number of elements found:', tds.length);

      let catText = ''; // Initialize catText outside the loop

      for (const td of tds) {
        const spanContent = await td.$('.a-size-base'); // Use .$
        const text = spanContent ? await spanContent.evaluate(node => node.textContent.trim()) : '';

        catText += text + ' '; // Concatenate text from each td
      }
      
      // Perform getCategory operation outside of page.$$eval
      const result = await getCategory.getCategory(categoriesFilePath, catText.trim());

      return result;
    } catch (error) {
      console.error('Error in findCategory:', error);
      throw error;
    }
  }

  // Navigate to the webpage
  await page.goto(url);

  // Get category name
  category = await findCategory();
  console.log("Category: " + category);
  scrapedData.push(category);
  // Find and click the link with data-hook="see-all-reviews-link-foot"
  const seeAllReviewsLink = await page.$('a[data-hook="see-all-reviews-link-foot"]');
  if (seeAllReviewsLink) {
    await seeAllReviewsLink.click();
    //await page.waitForNavigation();
    await page.waitForTimeout(5000);
  } else {
    console.error('See all reviews link not found');
    browser.close();
    return;
  }

  // Start scraping
  await scrapePage();


  // Close the browser
  await browser.close();

  try {
    // Save the scraped data to a text file
    fs.writeFileSync(outputFilePath, scrapedData.join('\n'), 'utf-8');

    console.log(`Scraped data saved to ${outputFilePath}`);
  } catch (err) {
    console.error('Error writing to file:', err);
    return "Error writing to file" + err;
  }



})();

