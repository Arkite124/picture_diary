from pathlib import Path

import fal_client

from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-26" / "scene_01.png"
# 여기에 image_path를 fal.ai 임시 URL로 업로드하는 코드를 채워요.
# 힌트: fal_client.upload_file(str(IMAGE_PATH))는 fal.ai 임시 URL을 반환.

PROMPT = ("slow zoom in, gentle sway, soft light, calm cinematic motion")  # 여기에 day4-s2에서 본 카메라 워크 어휘를 채워요.

# 여기에 submit_kling 호출 + task_id를 kling_task_id.txt에 저장하는 코드를 채워요.
# fal.ai 임시 URL로 업로드
image_url = fal_client.upload_file(str(IMAGE_PATH))
# task_id 생성 및 저장
task_id = submit_kling(
    image_url=image_url,
    prompt=PROMPT,
    duration=5
)
with open("kling_task_id.txt", "w", encoding="utf-8") as f:
    f.write(task_id)

print("Kling 작업이 제출되었습니다")
print("task_id:", task_id)