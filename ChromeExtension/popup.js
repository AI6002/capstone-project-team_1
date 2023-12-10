import { isAmazonProductPage } from './common.js';

document.addEventListener("DOMContentLoaded", function () {
  const analysisResultElement = document.getElementById("analysis-result");
  const server="http://vahidkh.me:5000"
  //const server="http://127.0.0.1:5000"
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

    //Feedback section
    function showFeedbackForm(productUrl,responseTime) {
      const feedbackForm = document.getElementById("feedback-form");
      feedbackForm.style.display = "block";
    
      const feedbackTextarea = document.getElementById("feedback-textarea");
      const satisfactionStars = document.getElementById("satisfaction-stars");
    
      document.getElementById("submit-feedback").addEventListener("click", function () {
        const feedback = feedbackTextarea.value.trim();
        const satisfaction = satisfactionStars.value;
    
        // Send feedback to the specified endpoint
        sendFeedback(productUrl, satisfaction, feedback,responseTime);
      });
    }
    
    function sendFeedback(productUrl, satisfaction, feedback,responseTime) {
      const feedbackEndpoint = server+"/feedback"; // Replace with your actual endpoint
    
      fetch(feedbackEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          productUrl,
          satisfaction,
          feedback,
          responseTime
        }),
      })
        .then((response) => {
          if (response.ok) {
            // Show "Thank you" message after successfully sending feedback
            document.getElementById("thank-you-message").style.display = "block";
            document.getElementById("feedback-form").style.display = "none";
          } else {
            console.error("Failed to send feedback:", response.statusText);
          }
        })
        .catch((error) => {
          console.error("Error sending feedback:", error);
        });
    }
    
    //Feedback section finished
    //Handle "Analyze" button click
    document.getElementById("analyze-button").addEventListener("click", function () {

      const loadingIndicator = document.getElementById("loading-indicator");
      const errorMessageElement = document.getElementById("fetch-error-message");

      document.getElementById("feedback-textarea").textContent = "";
      document.getElementById("satisfaction-stars").value = 5;
      document.getElementById("thank-you-message").style.display = "none";
      analysisResultElement.style.display = "none";
      errorMessageElement.style.display = "none";
      // Show loading indicator while fetching results
      loadingIndicator.style.display = "block";

      // Get the full product URL from the current tab's URL
      const fullProductUrl = currentTab.url;
      // Use a regular expression to extract the desired part of the URL
      const match = fullProductUrl.match(/^(https:\/\/www.amazon.com\/(?:[^/]+\/)?(?:dp\/)?[^/?]+)/);
      const productUrl = match ? match[1] : null;
      
      document.getElementById("best-feature").textContent =productUrl
      // Make a POST request to the web API
      const startTime = performance.now();
      fetch(server+"/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: productUrl }),
      })
        .then((response) => response.json())
        .then((data) => {
          // Calculate elapsed time
          const elapsedTime = performance.now() - startTime;
          // Hide loading indicator after fetching results
          loadingIndicator.style.display = "none";

          // Show best-feature and worst-feature elements
          document.getElementById("best-feature").textContent = data.bestFeature;
          document.getElementById("worst-feature").textContent = data.worstFeature;
          analysisResultElement.style.display = "block";
          
          // Show feedback form after successful POST request
          showFeedbackForm(productUrl,elapsedTime);

        })
        .catch((error) => {
          console.error("Error analyzing the product:", error);
          // Display error message
          errorMessageElement.textContent = "Error analyzing the product."+error;
          errorMessageElement.style.display = "block";

          // Hide loading indicator in case of an error
          loadingIndicator.style.display = "none";
        });
    });
  });
});
