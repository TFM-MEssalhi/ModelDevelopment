import torch
from transformers import AutoModelForCausalLM, AutoProcessor, AutoModel, AutoImageProcessor

model_name = "DAMO-NLP-SG/VideoLLaMA3-7B"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    #attn_implementation="flash_attention_2",
    attn_implementation="eager",
)
processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
video_path = "Cases/Case1.mp4"
question = "In this medical consultation, is the doctor conducting an exploratory analysis on the patient? If so, please provide the time range (start time - end time) of the exploration. If no exploration is conducted, respond with 'no exploration.'"

# Video conversation
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": [
            {"type": "video", "video": {"video_path": video_path, "fps": 1, "max_frames": 128}},
            {"type": "text", "text": question},
        ]
    },
]

inputs = processor(conversation=conversation, return_tensors="pt")
inputs = {k: v.cuda() if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
if "pixel_values" in inputs:
    inputs["pixel_values"] = inputs["pixel_values"].to(torch.bfloat16)
output_ids = model.generate(**inputs, max_new_tokens=128)
response = processor.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
print(response)
