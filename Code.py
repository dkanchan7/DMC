from flask import Flask, flash, redirect,render_template, request,jsonify
import os
from together import Together
import re
import json
from transformers import pipeline


app = Flask(__name__)  
  

client = Together(api_key="09cbbbbd5c5096e7f7fb35bbcbea9efdf4cb47a611337bcc166b7edd6046a8cb")

url = "https://api.together.xyz/inference"

Model="meta-llama/Llama-3-70b-chat-hf"

 
model_ckpt = "abhyast/minilm-finetuned-emotion-class-model"
pipe = pipeline("text-classification", model=model_ckpt)


def detect_emotion(text):
    results = pipe(text)
    # Assuming we always get at least one result, extract the first one
    return results[0] if results else None


 


@app.route('/')  
def index():  
    return render_template('index.html')  

def create_ad_slogan(pd,emotion):
    prompt = '''You are an creative Advertisement generator given the user emotions and product details.
    You have to generate very creative and attractive advertisement slogan so that it can market well and also you have to generate interesting Advertisement content/description
    
    '''
   
    
    fewshots = ''' Only respond in below mention output format
             {"ad_slogan": "Generated Ad slogan", "ad_description": "Generated Ad description"}
    
    Product details and user review based emotion given below:
         '''
    inputs="Product details :" + pd + " User emotion: "+ emotion
    prompt = prompt +   fewshots + inputs
    response = client.chat.completions.create(
    model=Model,
    messages=[{"role": "user", "content": prompt}],
    )
    print("response :\n",response.choices[0].message.content)
    res = response.choices[0].message.content
    res_dict = extract_json(res)  
    
    
    # Extract individual response values  
    adSlogan = res_dict["ad_slogan"]  
    ad_description = res_dict["ad_description"]
   
    return  adSlogan,ad_description



def extract_json(response):  
    json_match = re.search(r'\{.*\}', response, re.DOTALL)  
    if json_match:  
        json_string = json_match.group(0)  
        json_data = json.loads(json_string)  
        return json_data  
    else:  
        return None 

@app.route('/generate', methods=['POST'])
def generate():
    if request.method =="POST":
 
        user_review = request.form['user_review']
        prod_details =request.form['product_details']
        emotion = detect_emotion(user_review)
        emotion = emotion['label']
        print("emotion",emotion)
        adSlogan,ad_description = create_ad_slogan(prod_details,emotion)
          
    return render_template("prod.html", adSlogan=adSlogan,ad_description=ad_description,emotion=emotion)



# def create_product_title_desc(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#     Generate a catchy marketing product headline, killer product slogan for marketing highlight brand awareness and product description for the product details given below. Generate the output in proper json format in which first key value pair contains the headline and its generated headline, second key value pair contains description. As shown below
# {"headline" : "generated headline1, "slogan": generated slogan"} \n
#     '''
#     content = prompt + " " + "product: "+ text
#     return generate_text(project_id, model_name, temperature,max_decode_steps,top_p,top_k, content,location)
    
# def create_product_feats(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#     Generate 3 killer features for the product given below numbered from 1 to 3. Generate the whole content in less than 200 words only. \n
#     '''
#     content = prompt + " " + "product: "+ text
#     return generate_text(project_id, model_name, temperature,max_decode_steps,top_p,top_k, content,location)

# def create_insta_tags(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#     Generate three hashtags in one line for the below product in instagram for young generation. :\n
#     '''
#     content = prompt + " " + text
#     return generate_text(project_id, model_name, 0.6,max_decode_steps,top_p,top_k, content,location)

# def create_twitter_tags(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#     Generate three hashtags in one line for the below product in twitter for young generation. :\n
#     '''
#     content = prompt + " " + text
#     return generate_text(project_id, model_name, 0.6,max_decode_steps,top_p,top_k, content,location)

# def create_facebook_tags(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#     Generate three hashtags in one line for the below product in facebook for young generation. :\n
#     '''
#     content = prompt + " " + text
#     return generate_text(project_id, model_name, 0.6,max_decode_steps,top_p,top_k, content,location)

# def create_insta_posts(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#     Generate Short product slogan in 10 words to attract young generation for marketing below mentioned product in instagram. Dont explain the slogan.\n
#     '''
#     content = prompt + " " + text
#     return generate_text(project_id, model_name, 0.6,max_decode_steps,top_p,top_k, content,location)

# def create_fb_posts(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#         Generate Short product slogan in 10 words to attract young generation for marketing below mentioned product in facebook.Dont explain the slogan. :\n
#         '''
#     content = prompt + " " + text
#     return generate_text(project_id, model_name, 0.6,max_decode_steps,top_p,top_k, content,location)

# def create_twitter_posts(text):  
#     # prompt = f"Please provide clear, concise, and informative summary of the following news article in no more than {sumwordcount} words. Include the main points, key details, and any relevant context to ensure a comprehensive understanding of the content. Please ensure the generated summary should not be more than {sumwordcount} words ."  
#     prompt ='''
#     Generate Short product slogan in 10 words to attract young generation for marketing below mentioned product in twitter.Dont explain the slogan.\n
#     '''
#     content = prompt + " " + text
#     return generate_text(project_id, model_name, 0.6,max_decode_steps,top_p,top_k, content,location)




  
if __name__ == '__main__':  
    app.run(host='localhost', port='8888', debug=True)  
