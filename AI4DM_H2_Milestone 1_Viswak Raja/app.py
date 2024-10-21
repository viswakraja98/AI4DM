from flask import Flask, render_template, request
from dotenv import load_dotenv
# from model import runModels
from my_model import text2img, generate_story
import os
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__, template_folder = 'templates', static_folder='static',static_url_path='/')

@app.route('/')
def index():
    return render_template('about.html', active='index')

# @app.route('/milestone1', methods=["GET","POST"])
# def interaction_1():
#     if request.method == 'POST':
#         f = request.files["imgFile"]
#         file_name = secure_filename(f.filename)
#         cwd = os.getcwd()
#         upld_path = cwd+'/static/imgs/'+file_name
#         img_path = 'imgs/'+file_name
#         f.save(upld_path)

#         (caption, story) = runModels(upld_path)
        

#         return render_template('milestone1.html', active='interaction_1', imgPath=img_path, story=story, caption=caption)
#     else:
#         return render_template('milestone1.html', active='interaction_1')

@app.route('/milestone1', methods=["GET","POST"])
def interaction_1():
        return render_template('milestone1.html', active='interaction_1')

@app.route('/milestoneapi', methods=["GET","POST"])
def interaction_txt():
    prompt = dict(request.form)
    # call to gen image
    path = text2img(prompt['imgDesc'])
    image_name = "generated_image.png"
    story = generate_story(image_name)

    if story:
    # Get the base64 string from the static folder
        return render_template('milestone1.html', active='interaction_1', imgPath=image_name, story=story, caption='')
    return render_template('milestone1.html', active='interaction_1')


if __name__ ==  '__main__':
    app.run(host='0.0.0.0')