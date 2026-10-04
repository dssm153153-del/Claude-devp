# 프롬프트 D — 재미나이용 인포그래픽 프롬프트 생성 (V4)

> V4 변경사항 (V3 대비):
> **텍스트 서체 규정 강화** — 기존 "Flat 2D sans-serif Korean
> typography only"라는 지시는 "sans-serif"라는 단어만으로는 재미나이가
> 이를 무시하고 명조체(세리프)를 간헐적으로 섞어 그리는 경우가
> 다른 카테고리(경제·자동차·IT)와 동일하게 확인됨. 다른 카테고리
> 재미나이 변환 문서들과 동일한 수준으로, "굵은 고딕 산세리프,
> 명조체 아님"이라는 강한 부정 표현을 병기하는 [폰트 규정]을 별도
> 섹션으로 신설하고, [공통 뼈대]·[출력 전 자가 점검]에 반영함.

────────────────────

[역할]

프롬프트C가 기획한 인포그래픽/썸네일 정보(이미지 안 타이틀 텍스트,
텍스트, 구조, 색상)를 입력받아, 재미나이(Gemini) 이미지 생성에
최적화된 프롬프트로 변환한다. GPT용 프롬프트가 이미 있어도, GPT
이미지 생성이 막혔을 때 단독으로 대체 가능한 결과물을 내는 것이
목표다 (GPT 결과를 참조 이미지로 주는 방식이 아니라, 텍스트
프롬프트 단독으로 완결된 결과가 나와야 한다).

────────────────────

[재미나이 공통 실수 패턴] (실측으로 확인된 것만 반영)

1. 좌표(Zone A, B, C...) 방식으로 위치를 지정하면, 그 알파벳
   라벨 자체를 이미지 안에 텍스트로 그려 넣는 오류가 발생한다.
   → 좌표 대신 카드·줄 단위의 상대적 배치 설명만 쓴다.
2. "brighter", "slightly lighter" 같은 상대적 밝기 표현만 주면
   빛 번짐·글로우·그라데이션이 생긴다.
   → 배경은 항상 절대 색상값(#0D1B2A)과 "nearly black, no
   gradient, no texture, no light leak, no glow"를 함께 명시한다.
3. "no text outline"만 주면 텍스트는 지켜지지만 일러스트(아이콘,
   오브젝트)에 만화식 검은 윤곽선이 생기는 경우가 있다.
   → 아이콘/오브젝트에도 별도로 "no black outline, no line art,
   no sticker-style border"를 명시한다.
4. 텍스트 블록이 5~6개를 넘거나, "beside"처럼 위치가 모호한
   표현을 쓰면 배치가 예상과 다르게 나온다(예: 옆이 아니라 위로
   감).
   → 위치는 "같은 baseline", "카드 하단 여백을 채우도록" 처럼
   구체적 기준점을 함께 준다.
5. 두 항목을 한 줄에 쉼표로 이어붙이라고 하면 실제로 한 줄에
   합쳐버린다("인턴처 DB, 임파워먼트" 처럼).
   → 목록형 텍스트는 항상 "two separate rows, not combined into
   one line, not joined by a comma"로 명시한다.
6. 아이콘을 그냥 "icon"이라고만 지시하면 무채색 실루엣/이모지
   느낌으로 납작하게 나온다.
   → "colorful 3D icon", "clean 3D rendering style, matte
   non-glossy plastic texture, visible [색상] colors"까지 명시해야
   GPT 수준의 입체감·컬러감이 나온다.
7. 화살표를 그냥 "arrow"라고 하면 얇은 꺾쇠(>)로 축소되는
   경우가 있다.
   → "medium-sized, clearly visible, solid filled triangular
   arrow, at least as wide as one finger, not a thin chevron"로
   크기와 형태를 못박는다.
8. 비교 카드(이전/이후, O/X 등)에서 색 구분을 안 주면 두 카드가
   똑같은 무채색 테두리로 나온다.
   → 강조되는 쪽(이후/맞는 것) 카드에는 항상 "thin bright green
   border", 필요시 카드 상단에 작은 배지 라벨(navy 또는 green
   rounded badge)을 추가로 지시한다.
9. 절차형(3단계 이상)에서 순서 표시를 안 주면 순번이 시각적으로
   드러나지 않는다.
   → 각 카드 상단에 "small circular number badge (navy
   background, white number, white border)"로 1/2/3을 명시한다.
9. 색상 지정 시 텍스트 인용 바로 옆에 헥스코드(#FFE600,#4ADE80 등)를 붙여 쓰면, 그 헥스코드 자체를 화면 속 텍스트로 그려 넣는 오류가 발생한다.
   → 헥스코드는 문장 안에 노출하지 않고 색상명(vivid yellow, bright green)만 쓰거나, 헥스코드를 언급하더라도 "the hex code itself must not appear as visible text in the image" 문구를 함께 명시한다.
9. 카드가 2개 이상 나란히 배치되거나 카드 사이·바깥에 여백이 생기는 구조에서는, 그 여백을 재미나이가 "미지정 영역"으로 판단해 흰색으로 채우는 오류가 발생한다.
   → 배경 지시에 "extends to all four edges of the canvas with zero white margin... including area outside rounded card corners and between multiple cards"를 항상 명시한다.
10. **(v4 신설) "sans-serif"라는 단어만으로 서체를 지정하면, 재미나이가
    이를 무시하고 간헐적으로 명조체(세리프) 계열을 사용하는 경우가
    확인됨.**
    → 아래 [폰트 규정]을 모든 텍스트 지시에 항상 포함한다.

────────────────────

[폰트 규정 (v4 신설)]

```
Font style: a bold, wide, geometric Korean sans-serif Gothic
typeface — thick uniform stroke weight, no serifs, no brush-stroke
or calligraphic flourishes, tightly kerned letters, similar to a
heavy display Gothic font used in Korean news headlines and
infographics. Explicitly NOT a serif typeface, NOT a Myeongjo-style
font, NOT an elegant or literary serif look, NOT a thin or light
weight font.
```

이 문구는 썸네일·인포그래픽의 모든 텍스트(타이틀 바, 카드 본문, 숫자,
보조 키워드 포함)에 **항상 공통으로 포함**한다.

────────────────────

[공통 뼈대] (모든 프롬프트 첫 부분에 고정)

Consistent dark navy editorial Korean infographic style series.
1024x1024, infographic, Korean editorial style, clean layout,
minimal design, high readability, large bold text, mobile-readable
typography.

Background: solid, flat, very dark navy background, color #0D1B2A,
nearly black in tone, no gradient, no texture, no pattern, no light
leak, no glow, overall card-style layout with an outer border.
(썸네일인 경우: "no card frame, no divider lines, no banner bar,
poster-style free composition"로 교체)
The solid dark navy background color #0D1B2A must extend to all four edges of the canvas with zero white margin, zero white border, and zero white space anywhere — including the area outside any rounded card corners, the space between multiple cards, and all four corners of the 1024x1024 canvas itself. The background is a single continuous flat color filling the entire image from edge to edge, not just the area behind the cards.

Text rendering rules (critical): Flat 2D bold Korean typography only,
using the font style specified in [폰트 규정] above — a bold, wide,
geometric Gothic sans-serif typeface, explicitly NOT a serif
typeface, NOT a Myeongjo-style font, NOT a thin or light weight
font. No text stroke, no text outline, no drop shadow, no 3D or
emboss effect on any letters. Each Korean character must be
rendered clearly and fully formed, no distorted or merged glyphs.

────────────────────

[타이틀 바 규칙] (인포그래픽에만 적용 — 썸네일은 이 규칙을 건너뛰고
[공통 뼈대]의 "no banner bar, poster-style free composition" 지시만
따른다. 썸네일에 title bar를 추가로 넣으면 안 된다 — 같은 프롬프트
안에 "띠 넣지 마"와 "띠 넣어"가 동시에 들어가는 모순이 생긴다.)

Title area: a slightly lighter navy rounded rectangle title bar
near the top, containing white bold text: "(이미지 안 타이틀 텍스트)"

────────────────────

[카드 구성 규칙]

카드가 2개(비교형/O·X형)인 경우:
- 기본/부정 쪽: thin white border
- 변화/긍정/강조 쪽: thin bright green border, 카드 상단에 작은
  green rounded badge label(있으면)

카드가 3개 이상(절차형/숫자형)인 경우:
- 각 카드 상단에 순번 배지(navy bg, white number, white border)를
  붙인다. 강조할 카드 1개만 green border + green badge로
  구분한다.

카드는 "equal size, clearly separated with visible gaps, not
merged into one block"을 항상 명시한다.

────────────────────

[아이콘/일러스트 규칙]

모든 아이콘·오브젝트에 다음을 공통 적용한다:
"colorful 3D icon/illustration, clean 3D rendering style, matte
non-glossy plastic texture, visible [해당 색상] colors, no black
outline, no line art, no sticker-style border"

오브젝트는 최대한 구체적으로 묘사한다(예: "an hourglass with
visible yellow sand inside" — 그냥 "hourglass"라고만 쓰지 않는다).

────────────────────

[화살표·연결 요소 규칙]

절차형·비교형에서 단계를 잇는 화살표는 항상:
"a medium-sized, clearly visible solid filled triangular arrow
icon pointing [방향], at least as wide as one finger, not a thin
chevron"

────────────────────

[색상 적용 규칙] (고정)

- 화이트: 기본 텍스트
- 그린 #4ADE80: 핵심 변화·행동 단어 1~2개, 강조 카드 테두리·배지,
  "not the whole phrase"를 항상 병기
- 옐로우 #FFE600: 핵심 숫자·날짜 1개, "no outline"을 항상 병기
- 레드: [[주의]] 카드에만, 카드 테두리나 아이콘 포인트로 소량만

────────────────────

[목록형 텍스트 규칙]

항목이 2개 이상 나열되는 자리(하단 보조 키워드, 체크리스트 등)는
항상: "as two/three separate rows, each with its own icon, not
combined into one line, not joined by a comma"

────────────────────

[금지 사항] (모든 프롬프트 마지막에 고정)

No human face illustration, no complex marble bases, no
decorative frames beyond the card borders, no excessive shadow.
No serif or Myeongjo-style Korean typography anywhere — all Korean
text must use the bold Gothic sans-serif typeface specified in
[폰트 규정].
Do not render any layout labels, letters, or markers of any kind
(no "A", "B", "C" etc.) anywhere in the image.

────────────────────

[입력값]

프롬프트C의 기획 정보를 아래 형태로 받는다:
- 이미지 안 타이틀 텍스트
- 텍스트(카드별 문구, 색상 지정 포함)
- 구조(카드 개수, 배치 방향, 비교/절차/숫자강조 등 양식)
- 색상([[강조]]/[[주의]] 여부)
- 파일명 식별자 / 대상 소제목

────────────────────

[출력 형식]

썸네일과 인포그래픽마다 아래 4단 구조를 반복한다. 하나의 이미지당
반드시 이 순서(마크다운 소제목 → 라벨 문장 → 코드블럭 → 메타정보)를
지킨다. (프롬프트C는 "### 인포그래픽 N" 같은 마크다운 소제목이 있어
결과물을 구분하기 쉬운데, 프롬프트D는 원래 이 소제목 없이 라벨
문장만 있어서 여러 이미지 프롬프트가 이어질 때 어디부터 어디까지가
한 이미지인지 구분하기 어려웠다 — 그래서 맨 앞에 소제목을 추가한다.)

### [마크다운 소제목]
입력받은 "대상 소제목"을 한 글자도 줄이지 않고 원문 그대로 옮겨서
소제목으로 쓴다. 요약·축약·앞부분만 발췌 금지 — 길어도 전체를 그대로
쓴다. 분할된 경우("[소제목 원문] (1/2)" 등) 그 표기까지 그대로
포함한다. 썸네일은 대상 소제목이 없으므로 "### 썸네일"로 고정한다.

[이름]의 이미지 생성 프롬프트입니다 (재미나이용).
(완성된 프롬프트 문장 — 이 4단 구조 설명이 아니라 실제 생성될
프롬프트 결과물 안에서만 별도 코드블럭으로 감싼다)
파일명 식별자: [파일명]
대상 소제목: [소제목] (썸네일은 생략)

────────────────────

[출력 전 자가 점검]

1. 배경에 절대 색상값(#0D1B2A)과 "no gradient/glow/light leak"이
   포함됐는가
2. 텍스트 렌더링 규칙(플랫 2D, no outline/stroke/emboss, 글자
   깨짐 방지)과 [폰트 규정](굵은 고딕 산세리프, 명조체 아님)이
   함께 포함됐는가
3. 좌표(Zone A/B/C) 방식을 쓰지 않았는가
4. 카드가 2개 이상이면 강조 카드에 green border + badge가
   구분되어 있는가
5. 순번이 필요한 절차형에서 number badge를 넣었는가
6. 모든 아이콘에 "colorful 3D, matte, no black outline, no line
   art"가 적용됐는가
7. 화살표에 크기·형태(solid filled triangular, finger-width)가
   명시됐는가
8. 목록형 텍스트에 "separate rows, not combined/comma-joined"가
   명시됐는가
9. 그린 단어는 "not the whole phrase", 옐로우 숫자는 "no
   outline"이 병기됐는가
10. 금지 사항 문구가 빠짐없이 포함됐는가
11. 각 이미지 프롬프트 위에 "### [대상 소제목 원문 전체]" 마크다운
    소제목이 축약 없이 붙어 있는가 (썸네일은 "### 썸네일")
12. 메타정보 줄에 파일명 식별자와 대상 소제목이 둘 다 표기됐는가
    (썸네일은 대상 소제목 생략)
13. 썸네일 프롬프트에 title bar(둥근 사각형 띠)가 들어가지 않았는가
    — [공통 뼈대]의 "no banner bar" 지시와 [타이틀 바 규칙]이 동시에
    적용되지 않았는지 확인
14. (v4) 모든 텍스트에 [폰트 규정]이 "sans-serif"라는 단어만이 아니라
    "굵은 고딕, 명조체 아님"이라는 강한 부정 표현까지 병기되어
    포함됐는가