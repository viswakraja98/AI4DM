import base64
from transformers import pipeline
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import HumanMessagePromptTemplate

def img2text(url):
    img_to_text_pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    text = img_to_text_pipe(url)[0]["generated_text"]
    return text


def getRetriever(dir):
    """
    dir is the directory of the vector DB
    """
    embeddings_used = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorDB = Chroma(persist_directory=dir,embedding_function=embeddings_used)
    retriever = vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever


def textGeneration_langChain_RAG(msg,type,retrieverDir, image_data):
    """
    msg is the scenario for the story from the pic (hugging face model output);
    type is the emotion of the description- Surprise, Anger, Fear, Joy, Sad, Love
    retriever is the vector DB with relevant stories from txt version of 
        Emotions dataset from Kaggle - https://www.kaggle.com/datasets/parulpandey/emotion-dataset
    """
    llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.4,
            max_tokens=200,
            timeout=None,
            max_retries=2
        )

    prmpt = f'You are an expert at describing images in four quadrants for Blind and Low Vision users. Describe this image as if the emotion setting in image is {type}'
    out_message =  HumanMessagePromptTemplate.from_template(
        template=[
            {"type": "text", "text": prmpt},
            {
                "type": "image_url",
                "image_url": "{image_data}",
            },
        ]
    )

    prompt = ChatPromptTemplate.from_messages([out_message])

    
    rag_chain = prompt | llm | StrOutputParser()

    retriever = getRetriever(retrieverDir)

    out_message = rag_chain.invoke({
        "story_type" : type,
        "context":retriever,
        "image_data": image_data
        # "scenario_lang" : msg,
    })
    
    return out_message

def runModels_langchain_RAG(url, type, retrieverDir):
    image_data = local_image_to_data_url(url)
    scenario = img2text(url)
    story = textGeneration_langChain_RAG(scenario,type,retrieverDir, image_data)
    return([scenario,story])

import base64
from mimetypes import guess_type

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    # Default to png
    if mime_type is None:
        mime_type = 'image/png'

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"
