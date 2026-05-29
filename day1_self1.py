import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv



def load_api_key() -> str:
    """`.env`에서 OPENAI_API_KEY를 로드하고 마스킹한 키 첫 5자를 출력합니다."""
    # 여기에 load_dotenv() 호출 + os.getenv("OPENAI_API_KEY") 가져오기 + 첫 5자 마스킹 출력을 채워요.
    load_dotenv()
    api_key : str | None = os.getenv("OPENAI_API_KEY")
    print(f"[API 키] {api_key[:5]}...")
    return api_key

def build_scene_prompt() -> str:
    """본인 일기 첫 문장을 영문으로 묘사한 프롬프트를 반환합니다."""
    # 여기에 일기 첫 장면을 영문 묘사로 작성해요.
    # 여기에 본인 프롬프트 문장을 채워요.
    # 힌트: shot · time of day · lighting · style을 1~2 단어로 표현
    # 예: "wide shot, early morning, soft sunlight, watercolor diary illustration"
    My_prompt = "저녁 노을이 질때 즈음 이슬비가 내리고 그친 뒤에" \
    " 구름이 조금 지나가는 하늘이 있는 바닷가에서 한 사람이 서서 " \
    "비가 내린 뒤에 생긴 쌍무지개를 조용히 감상하고 있었다. " \
    "바람은 은은하게 불었고, 모래사장 뒤에 심겨진 나무들에 있는 " \
    "나뭇잎이 살짝씩 흔들렸다. 오랜만에 본 무지개는 그 사람을 설레게 했다. " \
    "여기에서 그는 지난 날의 추억들을 되새김하고 있었다."
    short_eng_prompt = "twilight seaside, double rainbow after rain, gentle drizzle, reflective mood, cinematic sky"
    english_prompt = "A sleepy person leaning against the wall on a bus seat, quiet ride, soft daylight, realistic mood"
    return english_prompt

def generate_image(client: OpenAI, prompt: str) -> str:
    """DALL-E 3로 이미지 1장 생성, URL을 반환합니다."""
    # 여기에 client.images.generate(...)를 호출하고 response.data[0].url을 반환하는 코드를 채워요.
    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        n=1
    )
    return response.data[0].b64_json


def save_image(b64_data: str, out_path: Path) -> None:
    """base64 이미지 데이터를 디코딩해 out_path에 저장합니다."""
    # 강의 내용에서 base64형식으로 응답받은 이미지를 디코딩해서
    # 저장하는 내용으로 바꿨기 때문에 맞춰서 바꿨어요.
    return out_path.write_bytes(base64.b64decode(b64_data))


if __name__ == "__main__":
    load_api_key()
    client = OpenAI()              # 키 자동 탐지
    prompt = build_scene_prompt()
    print(f"[프롬프트] {prompt}")
    b64_data = generate_image(client, prompt)
    print(f"[응답 base64] {b64_data[:60]}...")
    out_path = Path("outputs") / "scene01_dalle.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(b64_data, out_path)
    print(f"[저장 완료] {out_path}")

