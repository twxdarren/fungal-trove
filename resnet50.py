#!/usr/bin/env python3
"""
ResNet-50 Embedding Feature Extraction
--------------------------------------
This script:
1. Loads fungal images from a local directory
2. Extracts ResNet-50 embeddings
3. Saves each embedding as a .pt tensor file

Dependencies: torch, torchvision, opencv-python
Prerequisite: aggregate all .jpg files into INPUT_IMAGE_DIR

Author: Darren Ten
"""

import logging
from pathlib import Path

import cv2
import torch
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# User Configuration
INPUT_IMAGE_DIR = Path("/path/to/images")
OUTPUT_TENSOR_DIR = Path("/path/to/tensors")


def load_feature_extractor() -> torch.nn.Module:
    """
    Loads a pretrained ResNet-50 model without its classification head,
    returning a feature extractor that outputs the final pooling embeddings.
    """
    base = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    extractor = torch.nn.Sequential(*list(base.children())[:-1])
    extractor.eval()
    return extractor


def get_transform_pipeline() -> transforms.Compose:
    """
    Returns the image preprocessing pipeline matching ResNet-50 expectations.
    """
    return transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])


def extract_and_save_embedding(
    img_path: Path,
    model: torch.nn.Module,
    transform: transforms.Compose,
) -> None:
    """
    Reads an image, applies the transform, extracts the embedding,
    and saves it as a .pt file in OUTPUT_TENSOR_DIR.
    """
    image = cv2.imread(str(img_path))
    if image is None:
        raise RuntimeError(f"Failed to load image: {img_path.name}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tensor = transform(image_rgb).unsqueeze(0)  # shape: (1, 3, 224, 224)

    with torch.no_grad():
        embedding = model(tensor).squeeze()  # shape: (2048, 1, 1) → (2048,)

    out_path = OUTPUT_TENSOR_DIR / f"{img_path.stem}.pt"
    torch.save(embedding, out_path)
    logging.info(f"Saved embedding: {out_path.name}")


def main() -> None:
    """
    Main workflow: prepare directories, load model and transform,
    then process each .jpg in INPUT_IMAGE_DIR.
    """
    OUTPUT_TENSOR_DIR.mkdir(parents=True, exist_ok=True)

    model = load_feature_extractor()
    transform = get_transform_pipeline()

    image_files = sorted(INPUT_IMAGE_DIR.glob("*.jpg"))
    if not image_files:
        logging.warning(f"No .jpg files found in {INPUT_IMAGE_DIR}")
        return

    for img_path in image_files:
        try:
            extract_and_save_embedding(img_path, model, transform)
        except Exception as e:
            logging.warning(f"Failed to process {img_path.name}: {e}")

    logging.info("Embedding extraction completed.")


if __name__ == "__main__":
    main()