from flask import Flask, request, jsonify
from pyabsa import ATEPCCheckpointManager

app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def predict():
    
    # Load the model
    aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
    checkpoint="MLModel/PyABSA/checkpoints/finetuned_model",
    auto_device=True,  # False means load model on CPU
    cal_perplexity=True,
    )
    
    

    # Get the text from the request
    data = request.get_json(force=True)
    text = data["text"]
    print(text)
    
    # Predict
    atepc_result = aspect_extractor.extract_aspect(
    inference_source=text,  #
    save_result=True,
    print_result=True,  # print the result
    pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
    )
    
    result=[]
    for example in atepc_result:
        #aspect_sentiment_pairs = (example['aspect'],example['sentiment'])
        aspect_sentiment_pairs = {
        'aspects': example['aspect'],
        'sentiments': example['sentiment']
        }
        result.append(aspect_sentiment_pairs)

    return jsonify(result)


app.run(port=5000, debug=True)