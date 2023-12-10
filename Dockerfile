# Start your image with a node base image
#FROM python:3.11
FROM python:3.11
#FROM pytorch/pytorch:latest

# The /app directory should act as the main application directory
WORKDIR /code


# Copy local directories to the current local directory of our docker image (/app)
# Copy only the necessary files and directories
COPY requirements.txt .
COPY ./Inference/inferenceApi.py .
COPY ./MLModel/preprocessing.py ./MLModel/
COPY ./MLModel/aspect_mapping.py ./MLModel/
COPY ./MLModel/main.py ./MLModel/
COPY ./MLModel/data/categories.txt ./MLModel/data/
COPY ./MLModel/feature_sentiment_analysis.py ./MLModel/
COPY ./MLModel/PyABSA/finetuned_models/best_model ./MLModel/PyABSA/finetuned_models/best_model
COPY ./MLModel/PyABSA/extract_aspects.py ./MLModel/PyABSA/
COPY ./WebScraper/web-scraper.js ./WebScraper/
COPY ./WebScraper/get-category.js ./WebScraper/
COPY ./WebScraper/package-lock.json .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update \
    && apt-get install -y nodejs npm \
    #&& apt-get install -y libnss3-dev
    && npm install puppeteer \
    # Install necessary dependencies for puppeteer
    && apt-get install -y libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev libasound2 
    #&& mkdir -p ./MLModel/data
    #&& pip install torch torchvision torchaudio
    #&& npm install -g yarn \
    #&& yarn install --immutable


EXPOSE 5000

# Start the app using serve command
#CMD [ "gunicorn", "inferenceApi:app" ]\
# Start the FastAPI application using uvicorn
CMD ["uvicorn", "inferenceApi:app", "--host", "0.0.0.0", "--port", "5000"]