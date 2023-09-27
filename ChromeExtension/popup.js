import { isAmazonProductPage } from './common.js';

document.addEventListener("DOMContentLoaded", function () {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0];
    if (currentTab.url && isAmazonProductPage(currentTab.url)) {
      // Show the Analyze button and hide the error message
      document.getElementById("analyze-button").style.display = "block";
      document.getElementById("analysis-result").style.display = "block";
      document.getElementById("errorMessage").style.display = "none";

      // Get the image source from the current page
      chrome.scripting.executeScript({
        target: { tabId: currentTab.id },
        function: (isAmazonProductPage) => {
          if (isAmazonProductPage) {
            const productImage = document.querySelector("img#landingImage");
            const productTitle = document.getElementById("productTitle").textContent.trim();

            if (productImage || productTitle) {
              chrome.runtime.sendMessage({ imageSource: productImage.src, productTitle: productTitle });
            }
          }
        },
        args: [isAmazonProductPage(currentTab.url)],
      });

      chrome.runtime.onMessage.addListener(function (message) {
        if (message.imageSource) {
          // Set the image source in the popup's DOM
          document.getElementById('product-image').src = message.imageSource;
        }
        if (message.productTitle) {
          document.getElementById('product-name').textContent = message.productTitle;
        }
      });
    } else {
      // Hide the Analyze button and show the error message
      document.getElementById("analyze-button").style.display = "none";
      document.getElementById("analysis-result").style.display = "none";
      document.getElementById("errorMessage").style.display = "block";
    }

    //TODO: Handle "Analyze" button click

  });
});
