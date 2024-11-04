from transformers import pipeline
from openai import OpenAI

def img2text(url):
    img_to_text_pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    text = img_to_text_pipe(url)[0]["generated_text"]
    return text

def textGeneration(msg):
    """
    msg should be a dict of the form - {"role": "user", "content": scenario}
    """
    client = OpenAI()

    msg_list = [{"role": "system", "content": "You are an expert short story teller. Using a simple narrative you generate story in less than 100 words based on the given scenario."}]
    msg_list.append(msg)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        max_completion_tokens= 200,
        messages= msg_list
    )
    # print(response)
    out_message = response.choices[0].message.content
    return out_message

def runModels(url):
    scenario = img2text(url)
    message = {"role": "user", "content": scenario}
    story = textGeneration(message)
    return([scenario,story])