# day3_self2.py
from pathlib import Path
from datetime import date
import json
from agents.image import batch_generate

# 여기에 scene_prompts.json 또는 agents/scene.py 결과를 로드하고
# outputs/{오늘 날짜}/ 폴더에 4장 일괄 생성하는 코드를 채워요.
# 힌트: today = date.today().isoformat() → out_dir = Path("outputs") / today.
today = date.today().isoformat()

scenes_path = Path("scene_extracted.json")
out_dir = Path("outputs") / today

with scenes_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data["scenes"]

saved_paths = batch_generate(
    scenes=scenes,
    model="gpt-image-1-mini",
    out_dir=out_dir
)

print("저장된 이미지 경로:")
for path in saved_paths:
    print(path)
