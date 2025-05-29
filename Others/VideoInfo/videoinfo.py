from transformers import BitsAndBytesConfig, LlavaNextVideoForConditionalGeneration, LlavaNextVideoProcessor
import torch



import av
import numpy as np

def read_video_pyav(container, indices):
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)
    return np.stack([x.to_ndarray(format="rgb24") for x in frames])


def get_video(video_path, num_frames=8):
    container = av.open(video_path)
    total_frames = container.streams.video[0].frames
    indices = np.linspace(0, total_frames-1, num_frames).astype(int)
    clip_doctor = read_video_pyav(container, indices)
    return clip_doctor

def query_model(clip, processor, model):
    conversation = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "In this medical consultation, is the doctor conducting an exploratory analysis on the patient? If so, please provide the time range (start time - end time) of the exploration. If no exploration is conducted, respond with 'no exploration.'"},
            {"type": "video"},
        ],
    },
    ]
    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(videos=[clip], text=[prompt], padding=True, return_tensors="pt").to(model.device)
    generate_kwargs = {"max_new_tokens": 100, "do_sample": True, "top_p": 0.9}
    output = model.generate(**inputs, **generate_kwargs)
    generated_text = processor.batch_decode(output, skip_special_tokens=True)
    print(generated_text)

if __name__ == "__main__":
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    processor = LlavaNextVideoProcessor.from_pretrained("llava-hf/LLaVA-NeXT-Video-7B-hf", use_fast=False)
    model = LlavaNextVideoForConditionalGeneration.from_pretrained(
        "llava-hf/LLaVA-NeXT-Video-7B-hf",
        quantization_config=quantization_config,
        device_map='auto'
    )

    #video_paths = ["Cases/Case1.mp4", "Cases/Case2.mp4", "Cases/Case3.mp4", "Caso1_InfeccionRespiratoria.mp4", "Caso2_Lunares.mp4", "Caso3_Quemaduras.mp4"]
    video_paths = ["Cases/Case1.mp4", "Cases/Case1.mp4", "Cases/Case1.mp4", "Cases/Case1.mp4", "Cases/Case1.mp4"]
    for video_path in video_paths:
        clip = get_video(video_path)
        query_model(clip, processor, model)