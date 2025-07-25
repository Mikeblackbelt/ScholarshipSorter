# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
prompt = "Hey, are you conscious? Can you talk to me?"
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    device_map="auto",
    torch_dtype="auto"
)
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

generation_config = GenerationConfig(
    max_time=30,
)


# Generate
generate_ids = model.generate(inputs.input_ids, generation_config=generation_config)
tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])


generate_ids = model.generate(
    inputs.input_ids,
    generation_config=generation_config
)