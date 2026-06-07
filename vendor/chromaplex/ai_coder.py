"""AI-assisteret CPL kodegenerering."""

import sys
import os

def generate_cpl_from_prompt(prompt: str) -> str:
    """Generer CPL kode fra en naturlig-sprog beskrivelse."""
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY ikke sat")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "Du er en CPL (ChromaPlex Language) ekspert. "
                    "Generer KUN gyldig CPL kode. Brug: potens, tal, streng, "
                    "skriv_voxel, kanal, rød, grøn, blå, violet."
                )},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except ImportError:
        return (
            f"// Auto-genereret CPL (AI ikke tilgængelig)\n"
            f"// Prompt: {prompt}\n"
            f"potens e = 100;\n"
            f"skriv_voxel(0,0,0) {{\n"
            f"    kanal rød = e;\n"
            f"}}\n"
        )
    except Exception as e:
        return f"// Fejl ved AI-generering: {e}\n"


def main():
    if len(sys.argv) < 2:
        print("Brug: chromaplex-ai 'beskrivelse af problem'")
        return
    prompt = " ".join(sys.argv[1:])
    cpl_code = generate_cpl_from_prompt(prompt)
    print(cpl_code)


if __name__ == "__main__":
    main()
