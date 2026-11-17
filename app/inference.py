"""Zero-shot moderation with CLIP: the image is compared with a set of text prompts per category.

The similarities are turned into probabilities the way CLIP itself does it (scaled by the model's
logit scale, then softmax over all prompts), and the probabilities of a category's prompts are added up.
Raw cosine similarities between CLIP image and text embeddings sit around 0.15-0.35 for every image,
so they cannot be compared with a fixed threshold directly (the first version did, with 0.70, and
never flagged anything).
"""
import torch
import clip

from .model_loader import model, preprocess, device
from .prompt_words import PROMPT_DICT

THRESHOLD = 0.6  # a sensitive category needs at least this share of the probability to be flagged

_labels = list(PROMPT_DICT)
_prompts, _owner = [], []
for _i, _label in enumerate(_labels):
    _prompts.extend(PROMPT_DICT[_label])
    _owner.extend([_i] * len(PROMPT_DICT[_label]))
_owner = torch.tensor(_owner, device=device)

with torch.no_grad():  # the prompts never change: encode them once, not on every request
    _text = model.encode_text(clip.tokenize(_prompts).to(device)).float()
    _text /= _text.norm(dim=-1, keepdim=True)


def predict(image):
    with torch.no_grad():
        feats = model.encode_image(preprocess(image).unsqueeze(0).to(device)).float()
        feats /= feats.norm(dim=-1, keepdim=True)
        probs = (model.logit_scale.exp() * feats @ _text.T).softmax(dim=-1).squeeze(0)
        per_label = torch.zeros(len(_labels), device=device).index_add_(0, _owner, probs)

    best = int(per_label.argmax())
    label, prob = _labels[best], float(per_label[best])
    return {
        "result": 1 if label != "Normal" and prob >= THRESHOLD else 0,
        "score": round(prob * 100),
        "label": label,
        "scores": {name: round(float(p) * 100, 1) for name, p in zip(_labels, per_label)},
    }
