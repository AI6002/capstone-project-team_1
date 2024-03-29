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
    
class Feedback(BaseModel):
    productUrl: str
    satisfaction: int
    feedback: str
    responseTime: float

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
    print(data.url)
    try:
        result =await scrape(data.url)
        if "success" not in result or not result["success"]:
            return "File saving or scraping operation failed. "+result["error"]
            print("File saving or scraping operation failed. "+result["error"])

        
        print("Scraping completed successfully.")
        print("Analyzing the scraped data...")
    
        return await sentiment_analysis(scraped_data_path)
       
    except Exception as e:
        return "An error occurred: "+str(e)
  
async def save_feedback_to_csv(feedback: Feedback):
    import csv
    filename = "feedback.csv"
    fieldnames = ["Name", "Value"]

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty and write headers if needed
        if file.tell() == 0:
            writer.writeheader()

        # Write feedback data to CSV
        writer.writerow({"Name": "Product URL", "Value": feedback.productUrl})
        writer.writerow({"Name": "Satisfaction", "Value": feedback.satisfaction})
        writer.writerow({"Name": "Feedback", "Value": feedback.feedback})
        writer.writerow({"Name": "ResponseTime", "Value": feedback.responseTime})
        writer.writerow({})  # Add an empty row to separate entries
  
@app.post("/feedback/")
async def feedback(feedback: Feedback):
    try:
        await save_feedback_to_csv(feedback)
        return "Feedback saved successfully!"

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    

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

if __name__ == "__main__":
    uvicorn.run('inferenceApi:app', host='0.0.0.0', port=5000)



