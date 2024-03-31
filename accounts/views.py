from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.shortcuts import render
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "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"


def Chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        print(user_input)
        bot_response = ""
        if user_input.strip().lower() in ["hi", "hello", "hey","hy","hi ruby","hello ruby","hey ruby","hy ruby"]:
            bot_response = "Hello! How can I assist you today!"
        elif user_input.strip().lower() in ["bye","by","bye ruby","by ruby","thank you","thanks"]:
            bot_response = "Good bye and take care."
        else:
            question = user_input.strip()
            if len(question) < 4:
                bot_response = "Please enter a valid question!"
            else:
                try:
                    # Read PDF
                    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "D:\Internship Luminar\Parkingson's\parkinson\P5_Parkinson\Parkinson_pdf.pdf")
                    pdfreader = PdfReader(pdf_path)
                    raw_text = ''
                    for page in pdfreader.pages:
                        raw_text += page.extract_text()

                    # Split text
                    text_splitter = CharacterTextSplitter(
                        separator="\n",
                        chunk_size=800,
                        chunk_overlap=200,
                        length_function=len,
                    )
                    texts = text_splitter.split_text(raw_text)

                    # Embeddings
                    embeddings = OpenAIEmbeddings()

                    # FAISS
                    document_search = FAISS.from_texts(texts, embeddings)

                    # Load QA Chain
                    chain = load_qa_chain(OpenAI(), chain_type="stuff")

                    docs = document_search.similarity_search(user_input)
                    bot_response = chain.run(input_documents=docs, question=question)
                except Exception as e:
                    print(f"Error processing question: {e}")
                    bot_response = "I'm sorry, I couldn't process your question at the moment."

        return render(request, 'chatbot.html', {'user_input': user_input, 'bot_response': bot_response})
    else:
        return render(request, 'chatbot.html')



class Home(TemplateView):
    template_name='home.html'