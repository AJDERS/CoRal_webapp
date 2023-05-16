import torch
import re
from pathlib import Path
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load the Danish subset of the Wikipedia dataset from Hugging Face
dataset = load_dataset("olm/wikipedia", language="da", date="20230320", split="train")
tokenizer = AutoTokenizer.from_pretrained("juliensimon/xlm-v-base-language-id")
model = AutoModelForSequenceClassification.from_pretrained("juliensimon/xlm-v-base-language-id")

def check_sent(text):
    # Check if chunk contains two whitespace characters in a row, which indicates a new paragraph or section in the text
    if "  " in text:
        return False

    # Check if the chunk is more than 6 tokens long and less than 25 words long
    if len(text.split()) < 6 or len(text.split()) > 25:
        return False

    # Check if the chunk contains a URL
    if "http" in text:
        return False

    # Check if the chunk contains non-alphanumeric characters
    no_space_text = text.replace(" ", "")
    if not no_space_text.isalnum():
        return False
    
    return True

def chunk_text(text):
    speaking_rate = 120  # average speaking rate in words per minute
    max_duration = 10  # maximum duration of each chunk in seconds
    chunk_texts = []
    text = text.replace("\n", " ")
    # Split the text into sentences

    for sent in re.split("[.](?=\s[A-ZÆØÅ])", text):
        duration = len(sent.split()) / speaking_rate * 60
        if duration > max_duration:
            continue
        else:
            if check_sent(sent):
                chunk_texts.append(sent.strip())
    return chunk_texts

def main():
    
    # Check if processed_articles.csv exists
    if not Path("processed_articles.csv").exists():
        # Create the file and set the article count to 0
        processed_articles = pd.DataFrame(columns=["article_id", "url", "title", "text"]).to_csv("processed_articles.csv", index=False)
        processed_article_ids = []
    else:
        # Read the file and get the article ids of the articles that have already been processed
        processed_articles = pd.read_csv("processed_articles.csv")
        processed_article_ids = processed_articles["article_id"].tolist()
    
    for article in tqdm(dataset):

        # Check if the article has already been processed
        if article["id"] in processed_article_ids:
            continue

        # Chunk the text
        chunks = chunk_text(article["text"])

        # Check if the article is in Danish
        with torch.no_grad():
            n_chunks = 5 if len(chunks) >= 5 else len(chunks)
            if n_chunks == 0:
                continue
            logits = model(**tokenizer(chunks[0:n_chunks], padding=True, truncation=True, max_length=512, return_tensors="pt")).logits
            predicted_class_ids = torch.argmax(logits, dim=-1).tolist()
            predicted_classes = [model.config.id2label[predicted_class_ids] for predicted_class_ids in predicted_class_ids]
            if any([predicted_class != "Danish" for predicted_class in predicted_classes]):
                continue

        # Create records of the text chunks
        records = []
        for chunk in chunks:
            records.append({"article_id": article["id"], "url": article["url"], "title": article["title"], "text": chunk})

        # Save the records to a csv file
        pd.DataFrame(records).to_csv("processed_articles.csv", mode="a", header=False, index=False)


if __name__ == '__main__':
    main()