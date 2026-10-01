from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms with an example."
)

parser = StrOutputParser()

chain = prompt | llm | parser

topic = input("Enter a topic: ")

response = chain.invoke({
    "topic": topic
})

print("\nAnswer:\n")
print(response)

# v4
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash-lite"
# )

# prompt = PromptTemplate(
#     input_variables=["topic"],
#     template="Explain {topic} in simple terms with an example."
# )

# chain = prompt | llm

# topic = input("Enter a topic: ")

# response = chain.invoke({
#     "topic": topic
# })

# print("\nAnswer:\n")
# print(response.text)

# v3
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash-lite"
# )

# prompt = PromptTemplate(
#     input_variables=["topic"],
#     template="Explain {topic} in simple terms with an example."
# )

# topic = input("Enter a topic: ")

# final_prompt = prompt.format(topic=topic)

# response = llm.invoke(final_prompt)

# print("\nAnswer:\n")
# print(response.text)

# v2 
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash-lite"
# )

# prompt = PromptTemplate(
#     input_variables=["topic"],
#     template="Explain {topic} in simple terms with an example."
# )

# final_prompt = prompt.format(topic="RAG")

# response = llm.invoke(final_prompt)

# print(response.text)

# v1 
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash-lite"
# )

# response = llm.invoke("What is RAG?")

# print(response.text)