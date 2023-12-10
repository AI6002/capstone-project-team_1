// Description: This file contains the code to read the categories.txt file 
//and return the category name for a given search string.

const { Module } = require('module');

const fs = require('fs').promises;

async function getCategory(filePath, searchString) {
  try {
    let isPreviousLineMatched = false;
    let result = 'Not supported category. Please add it to categories.txt file.';
    let searchWords = searchString.toLowerCase().split(' ');
    const splitCount = 6;
    if (searchWords.length < splitCount)
      return result;

    const data = await fs.readFile(filePath, 'utf-8');
    const lines = data.split('\n')


    for (let i = 0; i < lines.length; i += 2) {
      const lineWords8first = lines[i].trim().toLowerCase().split(' ').slice(0, splitCount);
      const searchWords8first = searchWords.slice(0, splitCount);

      if (compareArrays(lineWords8first, searchWords8first)) {
        isPreviousLineMatched = true;
        result = lines[i + 1].trim();
        break; // Break the loop once a match is found
      } else if (isPreviousLineMatched) {
        // Reset the flag to avoid invoking the callback multiple times for the same match
        isPreviousLineMatched = false;
      }
    }

    return result;
  } catch (error) {
    console.error('Error reading file:', error.message);
    throw new Error('Error reading file');
  }
}

function compareArrays(arr1, arr2) {
  if (arr1.length !== arr2.length) {
    return false;
  }

  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) {
      return false;
    }
  }

  return true;
}

async function getCategory_by_whole_line(filePath, searchString) {
  try {
    const data = await fs.readFile(filePath, 'utf-8');
    const lines = data.split('\n')

    let isPreviousLineMatched = false;
    let result = 'Not supported category. Please add it to categories.txt';

    for (let i = 0; i < lines.length; i += 2) {
      const line = lines[i].trim().toLowerCase();

      if (line === searchString.toLowerCase()) {
        isPreviousLineMatched = true;
        result = lines[i + 1].trim();
        break; // Break the loop once a match is found
      } else if (isPreviousLineMatched) {
        // Reset the flag to avoid invoking the callback multiple times for the same match
        isPreviousLineMatched = false;
      }
    }

    return result;
  } catch (error) {
    console.error('Error reading file:', error.message);
    throw new Error('Error reading file');
  }
}

module.exports = { getCategory };
