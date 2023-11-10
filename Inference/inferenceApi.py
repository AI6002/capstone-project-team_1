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
from MLModel.PyABSA.extract_aspects import extract_aspects_and_sentiments

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

    return await extract_aspects_and_sentiments("MLModel/data/scraped_data.txt","MLModel/PyABSA/checkpoints/finetuned_model")
    

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



