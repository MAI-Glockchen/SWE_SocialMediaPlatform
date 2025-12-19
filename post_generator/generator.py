from transformers import pipeline

# -----------------------------
# Personas (prompt templates)
# -----------------------------
PERSONAS = {
    "neutral": "Write a short social media post.",
    "positive": "Write a positive and supportive social media post.",
    "negative": "Write a negative and critical social media post.",
}


# -----------------------------
# Text Generator
# -----------------------------
class TextGenerator:
    # singleton pattern: model initialized only once
    _generator = None

    def __init__(self):
        if TextGenerator._generator is None:
            # hosted API model
            TextGenerator._generator = pipeline(
                "text-generation",
                model="bigscience/bloomz-560m",  # free-tier instruction-tuned
                device=-1,
            )
        self.generator = TextGenerator._generator

    def generate_text(self, additional_prompt, persona="neutral", max_new_tokens=60):
        persona_instruction = PERSONAS.get(persona, PERSONAS["neutral"])

        # structured prompt for consistent output
        prompt = f"{persona_instruction}\nTopic: {additional_prompt}\nPost:"

        result = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
        )

        generated = result[0]["generated_text"]

        # only keep the model’s response after "Post:"
        if "Post:" in generated:
            generated = generated.split("Post:", 1)[1]

        return generated.strip()
