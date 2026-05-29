import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client

REQUIRED_FIELDS = ["scene_id", "scene_kr", "shot", "angle", "lighting", "lens", "prompt_en"]
# 여기에 scene_prompts.json을 json.load로 읽는 코드를 채워요
data = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
scenes = data.get("scenes", [])
print(f"장면 수: {len(scenes)}")

for i, scene in enumerate(scenes, 1):
    missing = [f for f in REQUIRED_FIELDS if f not in scene]
    if missing:
        print(f"장면 {i} 누락 필드: {missing}")
    else:
        print(f"장면 {i} OK — shot={scene['shot']}, angle={scene['angle']}")
        
def load_keys() -> None:
    """.env에서 FAL_KEY와 OPENAI_API_KEY를 로드합니다."""
    # 여기에 load_dotenv() 호출 + os.getenv("FAL_KEY") 가져오기 + 첫 5자 마스킹 출력을 채워요.
    # 힌트: FAL_KEY가 없으면 fal-client가 작동하지 않아요.
    # 힌트: print(f"FAL_KEY: {key[:5]}...") 형태로 마스킹 출력해요.
    load_dotenv()
    fal_key = os.getenv("FAL_KEY")
    if fal_key:
        print(f"FAL_KEY: {fal_key[:5]}...")
    else:
        print("FAL_KEY가 설정되지 않았습니다.")


def load_first_prompt() -> str:
    """scene_prompts.json에서 첫 번째 장면의 prompt_en을 반환합니다."""
    # 여기에 scene_prompts.json을 json.load로 읽고 scenes[0]["prompt_en"]을 반환하는 코드를 채워요.
    # 힌트: Path("scene_prompts.json").read_text(encoding="utf-8")로 파일을 읽어요.
    with Path("scene_prompts.json").open(encoding="utf-8") as f:
        data = json.load(f)
    scenes = data.get("scenes", [])
    if scenes and "prompt_en" in scenes[0]:
        return scenes[0]["prompt_en"]
    print("scene_prompts.json에서 prompt_en을 찾을 수 없습니다.")
    return ""

def call_flux_schnell(prompt: str) -> str:
    """FLUX-schnell로 이미지 1장 생성, URL을 반환합니다."""
    # 여기에 fal_client.subscribe("fal-ai/flux/schnell", arguments={"prompt": prompt, "num_images": 1})를 호출하고
    #   result["images"][0]["url"]을 반환하는 코드를 채워요.
    # 힌트: 응답 구조는 DALL-E와 다릅니다.
    #   OpenAI = response.data[0].url
    #   fal.ai = result["images"][0]["url"]
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={"prompt": prompt, "num_images": 1})
    return result["images"][0]["url"]


def save_image(url: str, out_path: Path) -> None:
    """URL의 PNG 바이트를 내려받아 out_path에 저장합니다."""
    # 여기에 requests.get(url) + out_path.write_bytes(response.content) 코드를 채워요.
    # 힌트: day1_self1.py에서 작성한 패턴을 재사용해요.
    response = requests.get(url)
    if response.status_code == 200:
        out_path.write_bytes(response.content)
    else:
        print(f"이미지를 다운로드하는 데 실패했습니다: {url}")


if __name__ == "__main__":
    load_keys()
    prompt = load_first_prompt()
    print(f"[프롬프트] {prompt[:60]}...")
    url = call_flux_schnell(prompt)
    print(f"[FLUX URL] {url[:60]}...")
    out_path = Path("outputs") / "scene01_fal.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(url, out_path)
    print(f"[저장 완료] {out_path}")