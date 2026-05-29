# 글로 쓰는 그림일기 — Picture Diary
일기 텍스트를 4장면 이미지+영상으로 변환하는 멀티 LLM 파이프라인

## 빠른 시작
```bash
uv venv && uv pip install -r requirements.txt
# .env에 OPENAI_API_KEY와 FAL_KEY 추가 후 실행
python pipeline.py
```

## 결과 미리보기
![scene_01](sample_readme\scene_01.png)

## 운영 지표

| Day | 모델 | 호출 수 | 합계 |
|---|---|---:|---:|
| Day 1 | gpt-image-1-mini | 4 | ~$0.08 |
| Day 2 | FLUX-schnell | 1 | ~$0.003 |
| Day 3 | GPT-4o-mini + gpt-image-1-mini | 5 | ~$0.04 |
| Day 4 | GPT-4o-mini + FLUX + Kling | 6 | ~$0.51 |
| Day 5 | FLUX A/B (seed 42 vs 137) | 6 | 모델/요금표 기준 확인 필요 |

자세한 내용은 [cost_report.md](cost_report.md) 참고

## A/B 테스트 요약

| 항목 | A 그룹 | B 그룹 |
|---|---:|---:|
| Seed | 42 | 137 |
| P95 지연 시간 | 2.43초 | 2.31초 |

- 도메인: **travel** / 프롬프트: 버스 좌석에 앉아 창가에 기대어 졸면서 갔다.
- B 그룹(seed 137)이 P95 기준으로 약 5% 더 빠름

## 도메인 응용

`domains/travel_prompts.json` — 여행 일기 도메인 적용 결과

| 장면       | 설명                          | 프롬프트 어휘                                                                     |
| -------- | --------------------------- | --------------------------------------------------------------------------- |
| scene_01 | 버스 좌석에 앉아 창가에 기대어 졸면서 갔다.   | `medium shot`<br>`eye-level`<br>`soft window light`                         |
| scene_02 | 창밖의 따뜻한 빛이 조용히 얼굴 위로 스며들었다. | `50mm lens`<br>`warm sunset light`<br>`dreamy watercolor travel diary mood` |

`domains/outputs.json` - 생성 결과
| scene_id | scene_kr | prompt_en | shot | angle | lighting | lens |
|---:|---|---|---|---|---|---|
| 1 | 버스 좌석에 앉아 졸고 있는 사람. | A person dozing off while sitting on a bus seat. | medium shot | eye-level | golden hour | 35mm |
| 2 | 버스 창 밖으로 보이는 노을. | A sunset view seen through the bus window. | wide shot | eye-level | golden hour | 24mm |
| 3 | 사람이 벽에 기대고 있는 모습. | A person leaning against the wall of the bus. | bust shot | eye-level | fill light | 50mm |
| 4 | 버스 내부의 평화로운 분위기. | The peaceful atmosphere inside the bus. | wide shot | high angle | key light | 85mm |


## 파일 구조

```
picture_diary/
├── agents/
│   ├── scene.py          # GPT-4o-mini로 일기 → 장면 JSON 추출
│   ├── image.py          # gpt-image-1-mini / FLUX 이미지 생성
│   └── video.py          # fal.ai Kling 영상 생성
├── domains/
│   └── travel_prompts.json
├── outputs/              # 생성된 이미지·영상
├── pipeline.py           # 일기 → 장면 → 이미지 → 영상 통합 파이프라인
├── ab_test.py            # A/B 레이턴시 측정
├── guardrails.py         # 반복·타임아웃·예산 가드
├── day1_self1.py ~ day5_self1.py
├── cost_report.md
├── diary.md
├── requirements.txt
└── .env                  # API 키 (git 제외)
```

