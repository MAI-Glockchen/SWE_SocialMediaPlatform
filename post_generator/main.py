from generator import PERSONAS, TextGenerator


def main():
    text_generator = TextGenerator()

    additional_prompt = "About the new movie Wicked:For Good"

    print("=== Testing text generation with all personas ===\n")

    for persona in PERSONAS.keys():
        print(f"[{persona.upper()}]")
        text = text_generator.generate_text(
            additional_prompt=additional_prompt, persona=persona
        )
        print(text)
        print("-" * 60)


if __name__ == "__main__":
    main()
