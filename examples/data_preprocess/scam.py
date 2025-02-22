import os
import pandas as pd
import argparse
from datasets import Dataset
from sklearn.model_selection import train_test_split

def load_csv_data(csv_path):
    """Loads data from a CSV file with columns 'label' and 'message'."""
    df = pd.read_csv(csv_path)
    return df[['label', 'message']]

def generate_scam_dataset(df, split_ratio=0.8):
    """Generates a dataset from CSV file data and splits into train/test sets using stratified sampling."""
    dataset = []
    for _, row in df.iterrows():
        label = row['label'].strip().upper()
        message_content = row['message'].strip()
        
        prompt = f"""<|im_start|>system
You are an expert in scam and spam detection with strong critical reasoning skills.
Before providing a classification, you carefully analyze the provided information, structuring your reasoning process step by step.

### **Classification Process:**

1. **Hypothesis Planning**  
   - Formulate a structured approach based on message content.  
   - Define an **evaluation hypothesis** using common scam/spam indicators (e.g., sender verification, urgency, financial solicitations, impersonation, deceptive intent, suspicious URLs).  
   - Tailor the hypothesis based on the message type:  
     - **Financial Advice:** Should have a valid source, balanced risk/reward, and avoid pressure tactics.  
     - **Urgency Alerts:** Should not pressure immediate action and should come from an official source.  
     - **Promotional Messages:** Should be from a verified sender, include an opt-out option, and avoid excessive repetition.  
     - **Unknown Messages:** Should contain enough identifiable details to determine legitimacy.  

2. **Validation with Data**  
   - Collect and analyze **key evidence** that supports or contradicts the hypothesis.  
   - Identify **observable indicators** (message patterns, language, links, sender details) that **validate or refute** a scam/spam classification.  

3. **Decision**  
   - Based on the validated data, assign one of the following labels:  
     - **SCAM:** Fraudulent intent, deception, impersonation, or clear malicious elements.  
     - **SPAM:** Unsolicited promotional content, excessive marketing, or irrelevant bulk messaging.  
     - **NOT_ENOUGH_INFORMATION:** Insufficient evidence to determine scam or spam.  

<|im_end|>

<|im_start|>user  
Analyze the following text (message content or description extracted via an Image-to-Text AI model) and classify it as **SCAM, SPAM, or NOT_ENOUGH_INFORMATION**.  

### **Analysis Steps:**  
1. **Hypothesis Planning**: Define an approach based on message content and general scam/spam detection strategies.  
2. **Validation with Data**: Identify key indicators that support or refute classification.  
3. **Decision**: Provide a final classification based on the strongest available evidence.  

### **Response Format:**  

<think>  
  <plan> (Structured hypothesis for analyzing the message) </plan>  
  <validation> (Key data that validates or contradicts the hypothesis) </validation>  
</think>  
<answer> (Final label: SCAM, SPAM, or NOT_ENOUGH_INFORMATION) </answer>  

Message Content:  
{message_content}  

<|im_end|>  
<|im_start|>assistant example  
<think>  
  <plan> (Structured hypothesis for decision-making) </plan>  
  <validation> (Critical data points correlated with the hypothesis and message content) </validation>  
</think>  
<answer> (SCAM, SPAM, or NOT_ENOUGH_INFORMATION) </answer>  
(end of assistant example)
<|im_end|>
"""

    
        dataset.append({
            "message": message_content,
            "label": label,
            "data_source": "scam",
            "prompt": [{"role": "user", "content": prompt}],
            "ability": "text_classification",
            "reward_model": {"style": "rule", "ground_truth": {"label": label}},
            "extra_info": {"category": "scam_detection"}
        })
    
    df_dataset = pd.DataFrame(dataset)
    train_dataset, test_dataset = train_test_split(df_dataset, test_size=(1 - split_ratio), stratify=df_dataset['reward_model'].apply(lambda x: x['ground_truth']['label']))
    
    return train_dataset.to_dict(orient='records'), test_dataset.to_dict(orient='records')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_path', required=True, help='Path to input CSV file')
    parser.add_argument('--local_dir', default='./data/scam')
    parser.add_argument('--split_ratio', type=float, default=0.8, help='Train-test split ratio')
    args = parser.parse_args()
    
    df = load_csv_data(args.csv_path)
    print(df.head())
    train_dataset, test_dataset = generate_scam_dataset(df, args.split_ratio)
    
    df_train = pd.DataFrame(train_dataset)
    df_test = pd.DataFrame(test_dataset)
    
    # Ensure local directory exists
    local_dir = os.path.expanduser(args.local_dir)
    os.makedirs(local_dir, exist_ok=True)
    
    # Save datasets as Parquet
    df_train.to_parquet(os.path.join(local_dir, 'train.parquet'), index=False)
    df_test.to_parquet(os.path.join(local_dir, 'test.parquet'), index=False)
    print(f"Train dataset saved to {local_dir}/train.parquet")
    print(f"Test dataset saved to {local_dir}/test.parquet")
