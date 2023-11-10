from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import subprocess
import json
import os, sys
from pyabsa import ATEPCCheckpointManager

# Navigate to the root directory by going up one level (../)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root directory to the Python path
sys.path.append(root_dir)
from MLModel.preprocessing import Preprocess

class Data(BaseModel):
    url: str

app = FastAPI()


@app.post("/analyze/")
async def analyze(data: Data):
    result =await scrape(data.url)
    if "success" not in result or not result["success"]:
        return "File saving or scraping operation failed"

    # Extract sentences from the scraped data
    await extract_sentences()

    # load data from a text file line by line in a list
    data_to_analyze = []
    with open("mlmodel/data/scraped_data.txt", 'r', encoding='utf-8') as f:
        for line in f:
            data_to_analyze.append(line)

    inference_source = data_to_analyze

    # Load the model
    aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
    checkpoint="MLModel/PyABSA/checkpoints/finetuned_model",
    auto_device=True,  # False means load model on CPU
    cal_perplexity=True,
    )
    
    # Predict
    atepc_result = aspect_extractor.extract_aspect(
    inference_source=inference_source, 
    save_result=True,
    print_result=True,  # print the result
    pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
    )
    
    result=[]
    for example in atepc_result:
        aspect_sentiment_pairs = {
        'aspects': example['aspect'],
        'sentiments': example['sentiment']
        }
        result.append(aspect_sentiment_pairs)

    #return jsonify(result)
    return result

async def scrape(url: str):
    # Define the command to run the Node.js script
    nodejs_script = "node WebScraper/web-scraper.js "+url

    # Execute the Node.js script and capture the output
    process = subprocess.Popen(nodejs_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return {"success": True}
    else:
        return {"error": f"Node.js script execution failed with error: {stderr.decode()}"} 

async def extract_sentences():
    prep=Preprocess()
    prep.extract_sentences("WebScraper/scraped_data.txt", "MLModel/data/scraped_data.txt")  

if __name__ == "__main__":
    uvicorn.run(app, port=5000, log_level="info")



