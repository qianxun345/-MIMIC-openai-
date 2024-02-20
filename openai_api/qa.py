import openai
import os

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
limit = 3750


def get_prompt(query, contexts, flag):
    prompt = ""
    if flag == 1:
        prompt = query + "Please consider a variety of factors. Finally, give the best answer you predict."
    elif flag == 2:
        prompt = f"some patient information is as follows:{contexts}.Let's think step by step like a medical expert:{query}. Please consider a variety of factors. Finally, give the best answer you predict."
    elif flag == 3:
        prompt = f"some patient information is as follows:{contexts}. You Could brainstorm three distinct solutions. Please consider a variety of factors.three different experts are answering this question. All experts will write down 1 step of their thinking,then share it with the group. Then all experts will go on to the next step, etc. If any expert realizes they're wrong at any point then they leave. The question is {query}. Finally, give the best answer you predict."
    elif flag == 4:
        prompt = f"some patient information is as follows:{contexts}. I have a problem related to {query}. you Could brainstorm three distinct solutions. Please consider a variety of factors , for each of the three proposed solutions, evaluate their potential. Assign a probability of success and a confidence level to each option based on these factors.Based on the evaluations and scenarios, rank the solutions in order of promise. Provide a justification for each ranking and offer any final thoughts or considerations for each solution. Finally, give the best answer you predict."
    return prompt

# 输入询问内容和pinecone.index，返回prompt
def retrieve(query, persist_directory, flag):
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    docs = db.similarity_search(query, k=10)
    contexts = [docs[i].page_content for i in range(len(docs))]
    print(contexts[0])
    # contexts = [
    #     x['metadata']['text'] for x in docs['matches']
    # ]
    #
    return get_prompt(query, contexts, flag)


# 返回聊天结果
def chat_complete(prompt):
    # query gpt-3.5-turbo， 这个模型更便宜
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a medical expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return res['choices'][0].message

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv('../openai.env')
    print(retrieve("What is the diagnosis of the patient?", "../ADMISSIONS_chroma", 2))