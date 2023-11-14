from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from MLModel.main import sentiment_analysis

class Data(BaseModel):
    url: str

app = FastAPI()
# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
scraped_data_path="./MLModel/data/scraped_data.txt"
@app.post("/analyze/")
async def analyze(data: Data):
    result =await scrape(data.url)
    if "success" not in result or not result["success"]:
        return "File saving or scraping operation failed. "+result["error"]

    
    
    # Extract sentences from the scraped data
    #await extract_sentences()
   
    return await sentiment_analysis(scraped_data_path)
    
    

async def scrape(url: str):
    # Define the command to run the Node.js script
    nodejs_script = "node WebScraper/web-scraper.js "+url+" "+scraped_data_path

    # Execute the Node.js script and capture the output
    process = subprocess.Popen(nodejs_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return {"success": True}
    else:
        return {"error": f"Node.js script execution failed with error: {stderr.decode()}"} 

# async def extract_sentences():
#     prep=Preprocess()
#     prep.extract_sentences("WebScraper/scraped_data.txt", "MLModel/data/scraped_data.txt")  

if __name__ == "__main__":
    uvicorn.run('inferenceApi:app', host='0.0.0.0', port=5000)



