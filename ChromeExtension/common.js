// common.js

function isAmazonProductPage(url) {
  return url.includes('amazon.com') && url.includes('/dp/');
}

// Export the function for use in other scripts
export { isAmazonProductPage };