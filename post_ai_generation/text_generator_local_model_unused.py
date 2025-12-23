from transformers import pipeline

print("[post-generator] Transformers imported")


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
    _generator = None

    def __init__(self):
        self.generator = None

    def _init_generator(self):
        if TextGenerator._generator is None:
            print("[post-generator] Loading text-generation model .", flush=True)
            TextGenerator._generator = pipeline(
                "text-generation",
                model="/hf_models/gpt2",
                device=-1,
            )
            print("[post-generator] Loaded text-generation model", flush=True)

        self.generator = TextGenerator._generator

    def generate_text(self, additional_prompt, persona="neutral", max_new_tokens=60):
        if self.generator is None:
            self._init_generator()
        persona_instruction = PERSONAS.get(persona, PERSONAS["neutral"])
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
        if "Post:" in generated:
            generated = generated.split("Post:", 1)[1]
        return generated.strip()
