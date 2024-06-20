import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from typing import List

def load_clip(model_card="openai/clip-vit-base-patch32"):
    model = CLIPModel.from_pretrained(model_card)
    processor = CLIPProcessor.from_pretrained(model_card)

    return model, processor

def embed_text(model, processor, texts: List[str]):
    inputs = processor(text=texts, return_tensors="pt", padding=True)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)

    return text_features

def embed_image(model, processor, image_paths: List[str]):
    images = [Image.open(image_path) for image_path in image_paths]
    inputs = processor(images=images, return_tensors="pt")
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    return image_features

def cosine_similarity(emb1, emb2):
    emb1_norm = emb1 / emb1.norm(dim=-1, keepdim=True)
    emb2_norm = emb2 / emb2.norm(dim=-1, keepdim=True)
    return torch.mm(emb1_norm, emb2_norm.t())

if __name__ == '__main__':
    model, processor = load_clip()
    text_embed = ['two cats']
    image_paths = ["E:\mori\SearchEngine\SearchEngine\\test\\000000039769.jpg"]
    embed_t = embed_text(model=model, processor=processor, texts=text_embed)
    embed_i = embed_image(model=model, processor=processor, image_paths=image_paths)
    res = cosine_similarity(embed_t, embed_i)
    print(res)
