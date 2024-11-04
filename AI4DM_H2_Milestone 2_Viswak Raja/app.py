from flask import Flask, render_template, request
from dotenv import load_dotenv
# from model import runModels
from my_model import text2img, generate_story
from my_model_llc import runModels_langchain_RAG
import os
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__, template_folder = 'templates', static_folder='static',static_url_path='/')

@app.route('/')
def index():
    return render_template('about.html', active='index')


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
        return render_template('milestone1.html', active='interaction_1', imgPath=image_name, story=story, caption='scenario')
    return render_template('milestone1.html', active='interaction_1')

@app.route('/milestone2', methods=["GET","POST"])
def interaction_2():
        return render_template('milestone2.html', active='interaction_2')

@app.route('/milestone2api', methods=["GET","POST"])
def interaction_2_txt():
    cwd = os.getcwd()
    db_dir = os.path.join(cwd,"chroma_db")

    prompt = dict(request.form)
    path = text2img(prompt['imgDesc'])
    image_name = "generated_image.png"

    upld_path = cwd+'\\static\\'+image_name

    genre = request.form.get('storyRadioOptions')
    # print(f"the story style selcted is {story_style}")

    # (caption, story) = runModels_langchain(upld_path,story_style)
    (caption, story) = runModels_langchain_RAG(upld_path,genre,db_dir)
    if story:
        return render_template('milestone2.html', active='interaction_2', imgPath=image_name, story=story, caption=caption, style=genre)
    return render_template('milestone2.html', active='interaction_2')
    

if __name__ ==  '__main__':
    app.run(host='0.0.0.0')