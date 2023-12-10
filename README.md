# Aspect-Based Product Reviews Analysis


Aspect-Based Product Reviews Analysis is a project that analyzes reviews and identifies sentiments (positive, negative) and specific aspects mentioned in the text. Given these results and some calculation, it can detect the best and worst features of a specific Amazon product.
This project is designed to help businesses to focus on areas that need improvement and emphasize their product's strengths in marketing and advertising campaigns. It also helps customers to make more informed purchasing decisions by knowing the strengths and weaknesses of a product and prioritize product features based on their preferences and needs.

![Screenshot from 2023-12-10 18-49-29](https://github.com/AI6002/capstone-project-team_1/assets/49075210/737dc546-0c57-4cd7-b67f-a0c5897d4f16)

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Evaluation](#evaluation)
- [Contributing](#contributing)

## Introduction

Our approach to sentiment analysis and aspect extraction leverages the PyABSA framework, a powerful tool for natural language processing. Utilizing the pretrained model deberta-v3-base-absa-v1.1, which is based on Microsoft's BERT architecture, we fine-tuned our model with a dataset comprising approximately 3100 rows of diverse reviews. The resulting model is adept at identifying sentiments and extracting aspects from textual data. To determine the best and worst features, we employ a post-processing step. Extracted aspects are compared against a product-category-specific dictionary, allowing us to replace them with contextually suitable words or phrases. Assigning positive and negative points to each feature enables us to calculate the highest and lowest scoring aspects, ultimately revealing the best and worst features within the analyzed reviews.


## Installation

To install the project, follow these steps:

1. Clone the repository:

```bash
https://github.com/AI6002/capstone-project-team_1
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the project
```bash
python .\Inference\inferenceApi.py
```
4. Call the api using postman
```bash
POST: http://127.0.0.1:5000/analyze
Body:
{"url":"[productUrl]"}
Headers:
{"Content-type":"application/json"}
```
## Evaluation
In evaluating our model, we employ key metrics such as accuracy, precision, recall, and f1-score, providing a holistic assessment of its performance.
To facilitate user interaction, the main module includes an optional 'evaluate' flag. By toggling this flag, users can choose between running the code and conducting a comprehensive evaluation.
We have curated specific evaluation datasets for various product categories, located in the 'Data/Evaluation' path. Users can leverage these datasets by replacing the input data with reviews from the corresponding file, enabling a straightforward evaluation process.

## Contributing 
Contributions are welcome! If you find a bug or have a suggestion, please open an issue or submit a pull request. Follow the guidelines in the CONTRIBUTING.md file.
