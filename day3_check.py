import json
from pathlib import Path

data = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
scenes = data.get("scenes", [])

required = ["scene_id", "scene_kr", "shot", "angle", "lighting", "lens", "prompt_en"]
all_ok = True

for scene in scenes:
    missing = [f for f in required if not scene.get(f)]
    if missing:
        print(f"scene {scene.get('scene_id', '?')} 미완성 필드: {missing}")
        all_ok = False

if all_ok and len(scenes) == 4:
    print("✅ Day 3 self1 연결 준비 완료 — 4장면 × 7필드 모두 채워짐")
else:
    print("⚠️ 미완성 항목이 있어요. 위 결과를 확인해 채워요.")
