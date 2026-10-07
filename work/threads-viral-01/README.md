# threads-viral-01: 정장 동물 버전 (원본 실존 인물 사용 금지)

- 원본: analysis/source.mp4 (9.3s, 528x544). 실존 정치인 얼굴의 AI 영상 → 인물은 반드시 가상 동물 캐릭터로 교체.
- 원본 흐름(0.3초 고해상도 재확인, analysis/hires/K1-fox-arm.png): 셋이 나무 아래 의자 → 왼쪽 인물이 팔꿈치를 굽혀 생수병을 얼굴 앞(턱 높이)에 들고 있다가 0.6-1.2s에 자기 이마에 병을 가로로 댐 → 1.8-2.1s 병 입구에서 물줄기가 옆으로 뿜어져 오른쪽 인물 얼굴에 맞음(머리 위로 붓는 것 아님) → 맞은 쪽 얼굴 감싸고 셋째가 벌떡 도망(2-4.8s) → 남은 둘이 엎치락뒤치락, 의자 걷어참(4.8-7s) → 한 명이 끈에 묶여 버둥, 다른 쪽 황당(7-9s). 컷: 4.83s, 5.80s.
- 원본 관계: 작은 체구의 인물(물 붓는 쪽)이 큰 체구의 인물(정장·빨간 넥타이)을 놀리고, 가운데 인물은 물 맞고 도망가는 구경꾼 역할.
- 확정 컨셉: 정장 입은 동물 셋, **작은 동물이 큰 동물들을 놀려먹는다.**
  - 장난꾼(물 붓기): 작은 동물 여우 (다람쥐에서 변경: 장난꾼 이미지·Motion Control 상반신 인식에 유리)
  - 물 맞고 놀라 도망(원본 가운데 인물): 큰 곰
  - 끝까지 당하는 쪽(원본 놀림 대상, 오른쪽 큰 인물): 고릴라 (마지막에 장난꾼을 잡으려다 끈에 엉켜 묶임, 여우는 옆에서 깔깔)
  - 장소: 원본과 같은 나무 아래 공터 (Motion Control 구도 일치)
- 다음 단계: 캐릭터 확정 컨펌 → 2단계 스토리보드(씬별 모델: 동작 씬은 Kling 2.6 Motion Control)

## 현재 진행 상황 (세션 이동용)
- 2026-10-07: C1-Start(다람쥐, 꽉 찬 구도) → Freepik 상반신 감지 실패. C1-Start-v2(여우, 넓은 구도) → 팔을 곧게 높이 든 포즈가 원본(굽힌 팔, 얼굴 앞)과 달라 불합격. Freepik 미리보기 clips/K1-preview.mp4(3.2s)는 C1-Start(다람쥐) 기반으로, 원본 동작을 따르지 않음. 다음: C1-Start-v3.
- 완료: 1단계 분석, 컨셉 확정, 스토리보드 v1(analysis/storyboard.md), 참조 영상 ref/Motion-K1~K3.mp4, 원본 컷 첫 프레임 ref/Shot1~3-first.png
- 사용자에게 이미 보낸 파일: ref/Shot1-first.png, ref/Motion-K1.mp4 (다시 보내지 않아도 됨)
- 지금: **C1-Start 이미지(GPT) 생성 대기** — 첨부: Shot1-first. 프롬프트:

```
Use the attached image only for the composition, camera angle, framing, lighting and background. Recreate this exact scene as a photorealistic photo, keeping every position, pose, gesture and the background identical (the tree, the stone wall, the grass and dirt ground, the white plastic chairs), but replace the three people with three anthropomorphic animals wearing the same clothes, in the same seats and the same poses:
- Left (sitting, holding up a plastic water bottle over the right character's head with a mischievous grin): a small red squirrel, clearly the smallest of the three, child-sized, upright like a person, fluffy tail, wearing a black buttoned tunic suit.
- Middle (sitting, looking on): a large brown bear wearing a dark puffer jacket over a blue hoodie and jeans.
- Right (sitting, the biggest, calm and unaware): a huge silverback gorilla in a navy suit, white shirt and long red tie.
Realistic fur, realistic lighting, natural outdoor daylight, same 1:1 square framing. No humans, no text, no logo, no watermark.
```
- 다음: C1-Start 검수 → K1 Motion Control(Start image=C1-Start, Video=Motion-K1.mp4, 짧은 프롬프트) 시험 → 결과 보고 K2·K3.
