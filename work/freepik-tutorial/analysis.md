# Freepik 영상 생성 튜토리얼 분석 (tutorial.mp4, 3분 47초, 화면만 분석 / 음성 미분석)

## 화면 흐름
- 0:00–0:21 Video 탭 → Model 선택(Auto, 목록에 Kling 2.1/2.1 Master/2.5/2.6/O1, Google Veo 3.1, Seedance 1.5 Pro 등) → **Kling O1** 선택
- References: Start image / End image / Video, 그 아래 Image 칸. 프롬프트 칸 안내문 "Reference your video or images using @image 1"
- 설정: 해상도 720/1080, 길이 5"/10", 비율 16:9
- 예시 1 (0:36–1:45): Start image 1장(빈 거실) + 긴 프롬프트 → 10초 생성 → 여자가 걸어 들어와 소파에 앉아 잡지를 읽는 영상
- 예시 2 (2:15–3:30): Start image(빈 거실) + End image(남자가 소파에 앉아 잔 들고 있음) + 프롬프트 → 남자가 뒤에서 걸어 들어와 돌아 앉는 영상. 재생바에 Start image → Prompt → End image 구간 표시
- 3:36 이후: Kling 2.6 Motion Control(Start image + Video 참조로 동작 복사) 소개

## 프롬프트 예시 1 (Start image만)
A woman enters from the left, sits on the sofa, and opens a magazine.
A refined, modern woman in a cream suit walks in with calm confidence, her hair moving softly. She crosses the minimalist interior and sits on the leather sofa. Her gestures are composed — she adjusts her posture, crosses one leg, and opens a fashion magazine, reading it with natural ease.

Slow dolly-in, eye-level framing, smooth motion, natural pacing. The camera starts low, rising slowly as it moves forward through the architectural space. The motion is smooth and controlled, capturing the elegant geometry of concrete, glass, and light. It stabilizes at eye level, framing her calmly seated in a cinematic, balanced composition.

Keep the same living room layout, lighting, and furniture. No new objects. No style change. The brutalist-modern interior remains unchanged: concrete ceilings, glass railings, leather sofa, and warm neutral daylight. Soft natural light fills the space evenly, maintaining a serene, architectural, and luxurious atmosphere.

## 프롬프트 예시 2 (Start + End image)
The camera starts close behind the man as he walks toward the sofa. It follows him with a smooth, steady movement. He wears a dark tailored suit, carrying a pale golden drink with calm confidence. When he reaches the sofa, he turns naturally and sits facing the camera. The shot ends showing him seated, relaxed, holding the drink — matching the End Image composition.

Same living room, same lighting, same time of day, consistent realism. Maintain the brutalist-modern interior with the leather sofa, soft daylight, and warm neutral tones. No new objects, no style changes. Realistic lighting, natural depth, and cinematic continuity throughout.

## 핵심 패턴
1. 첫 줄 = 한 문장 요약(누가 / 어디서 / 무엇을 하고 끝나는가)
2. 문단 1 = 인물 외형 + 동작을 시간 순서로, 감정·태도 형용사(calm confidence, natural ease)
3. 문단 2 = 카메라(무브 이름, 시작→끝 위치, 속도), 끝 프레임 구도
4. 문단 3 = 유지 문단(Keep the same …, No new objects, No style change, 조명·시간대)
5. End image를 쓸 때 마지막 동작 문장에 "— matching the End Image composition."
6. Avoid 목록 없이 긍정문 + 짧은 금지(No …)만 사용
