import openai
import os

from langchain.embeddings import HuggingFaceEmbeddings

limit = 3750

def get_prompt(query, contexts, flag):
    prompt = ""
    if flag == 1:
        prompt = query
    elif flag == 2:
        prompt = f"From all the csv file,some patient information is as follows:{contexts}.Let's think step by step like a medical expert:{query}"
    elif flag == 3:
        prompt = f"From all the csv file,some patient information is as follows:{contexts}. Could you brainstorm three distinct solutions? Please consider a variety of factors.three different experts are answering this question. All experts will write down 1 step of their thinking,then share it with the group. Then all experts will go on to the next step, etc. If any expert realizes they're wrong at any point then they leave. The question is {query}"
    elif flag == 4:
        prompt = f"From all the csv file,some patient information is as follows:{contexts}. I have a problem related to {query}. Could you brainstorm three distinct solutions? Please consider a variety of factors such as ADMITTIME, DIAGNOSIS and DISCHTIME.For each of the three proposed solutions, evaluate their potential. Consider their pros and cons, initial effort needed, implementation difficulty, potential challenges, and the expected outcomes. Assign a probability of success and a confidence level to each option based on these factors.Based on the evaluations and scenarios, rank the solutions in order of promise. Provide a justification for each ranking and offer any final thoughts or considerations for each solution."
    return prompt

# 输入询问内容和pinecone.index，返回prompt
def retrieve(query, index, flag):

    # get relevant contexts
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    res = index.query(queries=[embeddings.embed_documents([query])], top_k=15, include_metadata=True)
    # print(res)
    contexts = [
        x['metadata']['text'] for x in res['results'][0]['matches']
    ]
    return get_prompt(query, contexts, flag)


# 返回聊天结果
def chat_complete(prompt):
    # query gpt-3.5-turbo， 这个模型更便宜
    openai.api_key = os.getenv('OPENAI_API_KEY')
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a medical expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    return res['choices'][0].message
