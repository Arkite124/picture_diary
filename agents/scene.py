# agents/scene.py — OpenAI Chat JSON 모드로 일기→scenes JSON 추출

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


SCENE_SYSTEM_PROMPT = """당신은 일기 문장을 이미지 장면 데이터로 분해하는 AI입니다.
입력 텍스트에서 반드시 4개의 핵심 장면을 추출하세요.
반드시 다음 JSON 형식으로 응답하세요. JSON이외의 텍스트는 절대 포함하지 마세요.
prompt_en은 반드시 영어로 작성하세요 :
{
  "scenes": [
    {
      "scene_id": 1,
      "scene_kr": "장면 설명 (한국어 1문장)",
      "prompt_en": "영어 이미지 prompt",
      "shot": "bust shot | medium shot | wide shot",
      "angle": "eye-level | low angle | high angle",
      "lighting": "key light | fill light | back light | golden hour",
      "lens": "24mm | 35mm | 50mm | 85mm"
    }
  ]
}"""


def extract_scenes(diary_text: str) -> list[dict]:
    """일기 텍스트를 받아 scenes 리스트를 반환합니다."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SCENE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": diary_text
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1500,
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("OpenAI 응답 content가 비어 있습니다.")

    data = json.loads(content)

    scenes = data.get("scenes", [])

    return scenes


def validate_scenes(scenes: list[dict]) -> list[str]:
    """scenes 리스트가 4장면 × 필수 3필드(scene_id, scene_kr, prompt_en) 충족하는지 검증합니다."""

    errors: list[str] = []

    required_fields = ["scene_id", "scene_kr", "prompt_en"]

    if len(scenes) != 4:
        errors.append(f"scenes는 반드시 4개여야 합니다. 현재 개수: {len(scenes)}")

    for index, scene in enumerate(scenes, start=1):
        for field in required_fields:
            if field not in scene:
                errors.append(f"{index}번째 scene에 '{field}' 필드가 없습니다.")
            elif scene[field] is None or scene[field] == "":
                errors.append(f"{index}번째 scene의 '{field}' 값이 비어 있습니다.")

        if "scene_id" in scene and scene["scene_id"] != index:
            errors.append(
                f"{index}번째 scene의 scene_id가 올바르지 않습니다. "
                f"현재 값: {scene['scene_id']}, 기대 값: {index}"
            )

    return errors


def save_scenes(scenes: list[dict], out_path: str) -> None:
    """scenes 리스트를 JSON 파일로 저장합니다."""

    output_path = Path(out_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"scenes": scenes},
            f,
            ensure_ascii=False,
            indent=2
        )