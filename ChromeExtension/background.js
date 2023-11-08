// background.js
import { isAmazonProductPage } from './common.js';

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    debugger;
    if (tab.url && isAmazonProductPage(tab.url)) {
        chrome.action.setIcon({ path: 'icons/green.png', tabId: tabId });
    } else {
        chrome.action.setIcon({ path: 'icons/red.png', tabId: tabId });
    }
});




