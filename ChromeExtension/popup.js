import { isAmazonProductPage } from './common.js';

document.addEventListener("DOMContentLoaded", function () {
  const analysisResultElement = document.getElementById("analysis-result");
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0];
    if (currentTab.url && isAmazonProductPage(currentTab.url)) {
      // Show the Analyze button and hide the error message
      document.getElementById("analyze-button").style.display = "block";
      document.getElementById("errorMessage").style.display = "none";
      analysisResultElement.style.display = "none";

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
          const truncatedTitle = message.productTitle.length > 150 ?
            message.productTitle.substring(0, 147) + '...' :
            message.productTitle;
          document.getElementById('product-name').textContent = truncatedTitle;
        }
      });
    } else {
      // Hide the Analyze button and show the error message
      document.getElementById("analyze-button").style.display = "none";
      document.getElementById("errorMessage").style.display = "block";
      analysisResultElement.style.display = "none";
    }

    //Handle "Analyze" button click
    document.getElementById("analyze-button").addEventListener("click", function () {

      const loadingIndicator = document.getElementById("loading-indicator");
      const errorMessageElement = document.getElementById("fetch-error-message");

      analysisResultElement.style.display = "none";
      // Show loading indicator while fetching results
      loadingIndicator.style.display = "block";


      // Get the full product URL from the current tab's URL
      const fullProductUrl = currentTab.url;

      // Use a regular expression to extract the desired part of the URL
      const match = fullProductUrl.match(/^(https:\/\/www.amazon.com\/[^/]+\/dp\/[^/]+)/);
      const productUrl = match ? match[1] : null;

      // Make a POST request to the web API
      fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: productUrl }),
      })
        .then((response) => response.json())
        .then((data) => {
          // Hide loading indicator after fetching results
          loadingIndicator.style.display = "none";

          // Show best-feature and worst-feature elements
          document.getElementById("best-feature").textContent = data.bestFeature;
          document.getElementById("worst-feature").textContent = data.worstFeature;
          analysisResultElement.style.display = "block";

        })
        .catch((error) => {
          console.error("Error analyzing the product:", error);
          // Display error message
          errorMessageElement.textContent = "Error analyzing the product.";
          errorMessageElement.style.display = "block";

          // Hide loading indicator in case of an error
          loadingIndicator.style.display = "none";
        });
    });
  });
});
