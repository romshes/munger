import openai
import time

# Step 1: Set your API key
api_key = 'sk-proj'


# Step 2: Initialize the OpenAI client with the API key
client = openai.OpenAI(api_key=api_key)

# Step 3: Upload the training dataset
file_path = "qa_dataset2.jsonl"
file_response = client.files.create(file=open(file_path, "rb"), purpose='fine-tune')

training_file_id = file_response.id
print(f"Training file uploaded: {training_file_id}")

# Step 4: Fine-tune the model using a supported model, such as gpt-3.5-turbo
fine_tune_response = client.fine_tuning.jobs.create(training_file=training_file_id, model="gpt-4o-2024-08-06")
fine_tune_id = fine_tune_response.id
print(f"Fine-tune job created: {fine_tune_id}")

# Step 5: Polling until the fine-tuning job is complete
while True:
    status = client.fine_tuning.jobs.retrieve(fine_tune_id)
    print(f"Fine-tune status: {status.status}")
    if status.status == 'succeeded':
        fine_tuned_model = status.fine_tuned_model
        print(f"Fine-tuning completed. Model: {fine_tuned_model}")
        break
    elif status.status == 'failed':
        raise Exception("Fine-tuning failed")
    time.sleep(60)  # Wait 60 seconds before checking the status again

# Step 5: Use the fine-tuned model with the chat completion endpoint


completion = client.chat.completions.create(
  model=fine_tuned_model,
  messages=[
      {"role": "system", "content": "Charlie Munger jr. is a factual chatbot, that shares words of wisdom from seasoned financial advisor."},
      {"role": "user", "content": "What should i do to become successful investor?"}
  ]
)
print(completion.choices[0].message)

