# agents/image.py — gpt-image-1-mini 또는 FLUX 분기 이미지 생성
import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import fal_client


load_dotenv()


COMMON_STYLE = (
    "emotional diary illustration, soft light, dreamy pastel palette, quiet nostalgic mood"
)


def call_dalle(prompt: str, seed: int | None = None) -> bytes:
    """gpt-image-1-mini로 1장 생성, 이미지 bytes 반환."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    client = OpenAI(api_key=api_key)

    # gpt-image-1-mini는 seed 파라미터를 직접 받지 않음
    # 필요하면 프롬프트에 seed 느낌의 고정 문구를 추가
    if seed is not None:
        prompt = f"{prompt}, consistent visual seed {seed}"

    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        quality="low",
        n=1,
        output_format="png",
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return image_bytes


def call_flux(prompt: str, seed: int = 42) -> str:
    """FLUX로 1장 생성, URL 반환. seed로 일관성 강화."""

    fal_key = os.getenv("FAL_KEY")

    if not fal_key:
        raise EnvironmentError("FAL_KEY가 설정되어 있지 않습니다.")

    result = fal_client.run(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": "square_hd",
            "num_images": 1,
            "seed": seed,
        },
    )

    image_url = result["images"][0]["url"]

    return image_url


def generate_image(prompt: str, model: str = "dalle", seed: int = 42) -> bytes:
    """모델 분기 함수. gpt-image-1-mini 또는 FLUX 호출 후 이미지 bytes 반환."""

    model = model.lower()

    if model == "dalle":
        return call_dalle(prompt, seed)

    if model == "gpt-image":
        return call_dalle(prompt, seed)

    if model == "gpt-image-1-mini":
        return call_dalle(prompt, seed)

    if model == "flux":
        image_url = call_flux(prompt, seed)
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content

    raise ValueError(f"지원하지 않는 model입니다: {model}")


def save_image(image_bytes: bytes, out_path: Path) -> None:
    """이미지 bytes를 파일로 저장합니다."""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)


def batch_generate(scenes: list[dict], model: str, out_dir: Path) -> list[Path]:
    """scenes 리스트를 받아 4장 일괄 생성 후 저장 경로 반환.
    한 장 실패 시 try/except로 격리합니다.
    """

    saved: list[Path] = []

    out_dir.mkdir(parents=True, exist_ok=True)

    for scene in scenes:
        try:
            scene_id = scene["scene_id"]
            prompt_en = scene["prompt_en"]

            final_prompt = f"{prompt_en}, {COMMON_STYLE}"

            image_bytes = generate_image(
                prompt=final_prompt,
                model=model,
                seed=scene_id,
            )

            out_path = out_dir / f"scene_{scene_id:02d}.png"

            save_image(image_bytes, out_path)

            saved.append(out_path)

            print(f"[OK] scene {scene_id} 저장 완료: {out_path}")

        except Exception as e:
            scene_id = scene.get("scene_id", "unknown")
            print(f"[ERROR] scene {scene_id} 생성 실패: {e}")

    return saved