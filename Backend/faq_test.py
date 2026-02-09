import os
import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv

# Ragas Evaluation Imports
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# Import the core logic from your main app file (assuming it's named faq_app.py)
from faq import get_relevant_qa, generate_answer, ingest_faq_data, faqs_path

load_dotenv()

def test_chain(query):
    """
    A modified version of your faq_chain() that returns BOTH the generated answer
    and the raw context chunks. Ragas needs the contexts to check for hallucinations.
    """
    result = get_relevant_qa(query)
    
    # Ragas expects contexts as a list of strings
    contexts_list = [r.get('answer') for r in result['metadatas'][0]]
    
    # Combine just like your original code does for the LLM prompt
    context_str = "\n".join(contexts_list) 
    
    # Generate the actual answer using your Groq function
    answer = generate_answer(query, context_str)
    
    return answer, contexts_list

def run_evaluation():
    # 1. Ensure the database is populated before testing
    ingest_faq_data(faqs_path)

    # 2. Our "Golden Dataset" based on your FAQ_Relaxdash.csv
    # We ask slightly rephrased questions to test semantic search, 
    # and provide the exact Ground Truth from your CSV.
    test_cases = [
        {
            "question": "How can I pay for my order?",
            "ground_truth": "We accept Credit/Debit cards, Digital Wallets, Net Banking, and Cash on Delivery."
        },
        {
            "question": "My food hasn't arrived and it's past the time. What now?",
            "ground_truth": "If your order is delayed beyond the estimated time, please contact customer support for assistance."
        },
        {
            "question": "Can I order lunch now for delivery at dinner time?",
            "ground_truth": "Yes, you can select a specific delivery time slot during the checkout process."
        },
        {
            "question": "I was charged but the app said payment failed.",
            "ground_truth": "The amount will be automatically refunded to your source account within 5-7 business days."
        },
        {
            "question": "Can I get pizza from Place A and sushi from Place B in one order?",
            "ground_truth": "No, you must place separate orders for each restaurant."
        },
        {
            "question": "I'm sick and don't want to meet the driver. Can they leave it outside?",
            "ground_truth": "Yes, you can request the driver to leave the package at your door."
        },
        {
            "question": "Is it possible to tip the delivery person?",
            "ground_truth": "Yes, tipping is available during checkout or after delivery to appreciate the service."
        },
        {
            "question": "The food arrived crushed and cold.",
            "ground_truth": "Please report quality issues with a photo to our support team for compensation."
        },
        {
            "question": "How much is the delivery charge?",
            "ground_truth": "Fees vary based on the distance between you and the restaurant."
        },
        {
            "question": "I have a peanut allergy. Where do I say that?",
            "ground_truth": "Please clearly specify any allergies in the 'Note to Chef' section for each item."
        }
    ]

    # Lists to hold the structured dataset for Ragas
    questions = []
    answers = []
    contexts = []
    ground_truths = []

    print("\n--- Running Inference on Test Cases ---")
    for case in test_cases:
        q = case["question"]
        print(f"Testing Question: {q}")
        
        # Run through your RAG pipeline
        ans, ctx = test_chain(q)
        
        questions.append(q)
        answers.append(ans)
        contexts.append(ctx)
        ground_truths.append(case["ground_truth"])

    # 3. Create the HuggingFace Dataset
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)

    # 4. Set up the Evaluator Models (Using your existing Groq and MiniLM stack)
    # Ragas uses Langchain under the hood, so we wrap your models.
    print("\n--- Initializing Evaluator Models ---")
    eval_llm = ChatGroq(model_name=os.environ['GROQ_MODEL'])
    eval_embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # 5. Run the Evaluation
    print("\n--- Running Ragas Evaluation ---")
    results = evaluate(
        dataset=dataset,
        metrics=[
            context_precision, # Did Chroma retrieve the right FAQ rows?
            faithfulness,      # Did the LLM make anything up?
            answer_relevancy   # Does the answer actually address the question?
        ],
        llm=eval_llm,
        embeddings=eval_embeddings,
        raise_exceptions=False # Prevents the script from crashing if a metric fails to calculate
    )

    # 6. Display the Results
    print("\n--- Final Evaluation Scores ---")
    print(results)
    
    # Save the detailed results (including row-by-row scores) to a CSV so you can inspect it
    df = results.to_pandas()
    df.to_csv("faq_evaluation_results.csv", index=False)
    print("\nDetailed results saved to 'faq_evaluation_results.csv'")

if __name__ == '__main__':
    run_evaluation()