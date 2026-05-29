# Day 1 self1 개발 기록

- 배운 점: .env에 API 키를 넣고 load_dotenv()로 읽으면 코드에 키를 직접 쓰지 않아도 된다. base64는 다시 디코딩하여 이미지화 하는 작업이 필요하다.
- 막힌 점: 반환 형식이 base64로 바뀌어서, 반환값을 받는 것과 다시 디코딩해서 저장하는 것에 생성형AI의 힘을 빌렸다.
- 내일 시도할 것: 같은 일기 장면을 샷, 앵글, 조명만 바꿔서 비교해 본다.
- 강사 비유 연결: 오늘 b64_json으로 보내져 온 결과물은, 다시 해독하여 png이미지를 저장하기 위한 형식이다.

## Day 1 self2 시작 전 관찰

- 마음에 든 부분: 자고 있는 사람
- 바꾸고 싶은 부분: 버스같지 않은 모습, 의자의 종류

## Day 2 self2 — scene_prompts.json + fal.ai 첫 호출

- 완료 시각: 17:15
- 생성 파일: scene_prompts.json, day2_self1.py, day2_self2.py, outputs/scene01_fal.png
- FLUX vs DALL-E 차이: URL,dict형식 / b64_json,base64 형식
- 막힌 부분: checkfield 함수에서 missing 객체가 기록된 걸 인식하지 못하는 현상

## Day3 self3-1
항목               scene_prompts.json (사람)      scene_extracted.json (GPT)
장면 1 scene_kr    버스 좌석에 앉아 벽에 기대어 졸면서 갔다./버스 좌석에 앉아 졸고 있는 모습.
장면 1 prompt_en   A sleepy person leaning against the wall on a bus seat, quiet ride, soft daylight, realistic mood / A person intensely playing a game at a computer desk.
샷·앵글·조명 어휘        "shot": "WS",            "shot": "medium shot",
                        "angle": "eye-level",    "angle": "eye-level",
                        "lighting": "backlit",   "lighting": "fill light",
                        "lens": "50mm",          "lens": "35mm"          

더 풍부한 쪽            표현은 사람이 풍부하게 했지만, 샷, 조명, 앵글 등은 GPT가 더 잘 잡아 낸 거 같습니다.

## 공통 어휘-화풍 
emotional diary illustration, soft light, dreamy pastel palette, quiet nostalgic mood
## Day 4 self1
- 동기 호출은 결과를 바로 기다리고, 비동기 호출은 task_id를 받아 나중에 status/result로 확인한다.
- 가드레일 4종은 반복 횟수, 대기 시간, 완료 조건, 비용 상한을 제한해 무한 대기와 비용 초과를 막는다.
## Day 5 self1

- 선택 도메인: travel
- seed A/B: 42 / 123
- A 호출 수: ___
- B 호출 수: ___
- p95_latency_s: ___
- cost_per_image: ___
- total_cost_usd: ___





