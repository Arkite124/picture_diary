import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def build_prompt_variants() -> list[tuple[str, str]]:
    """(filename, prompt) 튜플 3개를 반환합니다. WS / CU / low angle 변형 순서."""

    variants: list[tuple[str, str]] = [
        (
            "scene01_ws.png",
            "Wide shot of a quiet twilight seaside after gentle drizzle, a lone figure standing on rain-washed sand and watching a double rainbow under drifting clouds, soft ocean breeze, swaying tree leaves, calm sea waves, glowing horizon, cinematic emotional atmosphere."
        ),
        (
            "scene01_cu.png",
            "Close-up cinematic view of a lone person quietly gazing at a double rainbow after rain on a twilight beach, soft blush of sunset light, reflective eyes, nostalgic memories, peaceful shoreline, dreamy post-rain ambience, melancholic beauty."
        ),
        (
            "scene01_low.png",
            "Low angle cinematic shot from the wet sandy beach, a lone figure silhouetted against a glowing twilight sky with a double rainbow after drizzle, drifting clouds, gentle ocean breeze, swaying tree leaves, serene evening light, poetic emotional storytelling."
        ),
    ]

    return variants


def call_dalle(client: OpenAI, prompt: str) -> str:
    """gpt-image-1-mini로 이미지 1장 생성, base64를 반환합니다."""

    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
    )

    return response.data[0].b64_json


def save_image(image_b64: str, out_path: Path) -> None:
    """base64 문자열을 디코딩하여 PNG 바이트를 out_path에 저장합니다."""

    image_bytes = base64.b64decode(image_b64)
    out_path.write_bytes(image_bytes)


if __name__ == "__main__":
    load_dotenv()

    client = OpenAI()

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    variants = build_prompt_variants()

    for filename, prompt in variants:
        print(f"[호출 시작] {filename} ...")

        try:
            image_b64 = call_dalle(client, prompt)
            save_image(image_b64, output_dir / filename)
            print(f"[저장 완료] {output_dir / filename}")

        except Exception as e:
            print(f"[실패] {filename}: {e}")
            continue

    print("\n끝. outputs/ 폴더에서 3장을 비교해 보세요.")