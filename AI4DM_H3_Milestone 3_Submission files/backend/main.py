from dotenv import load_dotenv
load_dotenv()

from PIL import Image
from flask import Flask, abort, request
from flask_cors import CORS
import importlib
import base64
import io


server = Flask(__name__)
CORS(server, resources={
    r"/run/*": {
        "origins": "http://localhost:5173",  # Only allow requests from example.com
        "methods": ["POST"]  # Allow only GET and POST methods
    }
})

_models = dict(
    img_desc=dict(
        image=Image
    ),
    sdxl=dict(
        prompt=str,
        image=Image
    ),
    vqa=dict(
        prompt=str,
        image=Image
    )
)

_models = {i: {"runner": getattr(importlib.import_module(i), "run_model"), "inputs": _models[i]} for i in _models}

@server.post("/run/<model>")
def _handle_model(model):
  if model not in _models:
    abort(404, f"Model {model} not found.")
  args = {}
  data = request.get_json()
  for inp in _models[model]["inputs"]:
    if inp not in data:
      abort(501, f"Missing {inp} for model {model}.")
    if _models[model]["inputs"][inp] == Image:
      if data[inp].startswith("data:image"):
        args[inp] = Image.open(io.BytesIO(base64.b64decode(data[inp].split(",")[1])))
        args[inp].save("debug.png")
      else:
          abort(501, description="Invalid image: Not Base64.")
    if _models[model]["inputs"][inp] == str:
      args[inp] = str(data[inp])
  return _models[model]["runner"](**args)
         



if __name__ == '__main__':
    server.run(host="0.0.0.0", port=8000)