from dataset.generator import generate_dataset

summary = generate_dataset(
    num_examples=100,
    output_path="dataset/datasets/train/sample_v1.jsonl",
    seed=1,
)
print(summary)