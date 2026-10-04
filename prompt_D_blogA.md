# 프롬프트 D — 재미나이용 인포그래픽 프롬프트 생성 (블로그 A용 V4.2)

> **[참고 메모 — 실행 규칙 아님]** 이 블록은 사람이 프롬프트를 검토·변경할 때만 보는 메모다. 프로그램(Ver10.02 이후)은 복사할 때 이 블록을 빼고 "# 제목" 줄과 아래 `---` 이후 본문만 보낸다. 직접 붙여넣어 이 블록이 함께 들어오더라도 규칙으로 적용하지 않는다. 메모 표시("[참고 메모")와 `---` 줄은 프로그램이 메모를 찾는 기준이므로 지우거나 바꾸지 않는다. 본문의 "(V4.2)" 같은 표기는 이 메모에서 근거를 찾기 위한 꼬리표다.
>
> **블로그 A용이다. 프롬프트 C 블로그 A용 V4.2와 짝으로 쓴다.** 이미지를 블로그별로 차별화하려고 C·D를 둘로 나눴다 — 블로그 A용("여백 있는 평면 미니멀", V4 계열)과 블로그 B용("꽉 찬 세미플랫", D V7·C V12). 정책뉴스 프로그램 설정에는 D 파일도 하나만 들어가므로, 블로그를 바꿔 발행할 때 C와 D 파일 이름을 함께 바꾼다.
>
> D는 C가 정한 문구·구조를 재미나이용 문장으로 옮기는 변환 단계다. 문구 판단(제목 기준, 정부 용어, 본문 표현 범위, 결론 카드)은 C가 하고 D는 바꾸지 않는다.
>
> **1. 검증 대기 중인 가설** — 재미나이 실측 결과를 보고 유지·수정을 정한다.
> - V4.2 블로그 A 화풍·배치를 재미나이용으로 옮김(flat 2D 벡터, 단색 네이비, 텍스트 위 1/2 · 오브젝트 그 아래 약 1/3(최대 2개) · 보조 키워드 맨 아래 한 줄, 인물 실루엣 없음) — C 블로그 A용 V4.1·V4.2 규정을 옮긴 것이며 재미나이 실측 전.
> - V4.2 아이콘을 "colorful 3D"에서 "colorful flat 2D vector"로 바꿈 — 블로그 A 화풍에 맞추려는 조정이다. 실수 패턴 6번(그냥 "icon"이면 무채색 실루엣·이모지처럼 납작하게 나옴)이 다시 생기는지 실측으로 확인한다. 생기면 "solid fills, visible colors" 쪽을 더 세게 쓴다.
> - V4.2 실수 패턴 13·14번(세로 배분, 비율 수치가 글자로 찍힘)과 [C 문구 보존]은 블로그 B 계열 D V5·V6에서 옮긴 예방 규정이다.
>
> **2. 유지 근거** — 재미나이 실측에서 확인된 문제로 생긴 규칙. 완화·삭제 전에 확인한다.
> - 실수 패턴 1~12번: 좌표 라벨(Zone A/B/C)을 그림, 상대 밝기 표현이 빛 번짐을 만듦, 아이콘에 검은 윤곽선, 위치가 모호하면 배치가 틀어짐, 쉼표 목록을 한 줄로 합침, "icon"만 쓰면 납작한 이모지, "arrow"만 쓰면 얇은 꺾쇠, 비교 카드 색 구분 없음, 절차형 순번 없음, 헥스코드를 글자로 그림, 카드 사이 여백을 흰색으로 채움, "sans-serif"만으로는 명조체가 섞임.
> - [폰트 규정]의 강한 부정 표현("NOT a Myeongjo-style font")(V4).
> - 썸네일에 title bar 금지: "띠 넣지 마"와 "띠 넣어"가 한 프롬프트에 함께 들어가는 모순.
> - 이미지마다 "### 대상 소제목 원문" 머리줄: 여러 이미지 프롬프트가 이어질 때 경계가 보이지 않았음.
> - 블로그 A 화풍 고정과 세로 비율, 보조 키워드 구분선 금지, 인물은 픽토그램만, 레드는 경고에만: C 블로그 A용 V4.1의 근거(실사 풍경으로 흐름, 상단이 빔, 보조 키워드 사이 "|", 인물 포함 여부가 생성마다 달라짐, 달력에 빨간 동그라미).
>
> **3. 폐기된 규칙**
> - 아이콘 "colorful 3D icon, clean 3D rendering style, matte plastic"(V4): 블로그 A의 평면 화풍과 맞지 않아 V4.2에서 flat 2D 지시로 교체. 블로그 B용 D에는 3D 지시가 그대로 있다.
> - 실수 패턴 번호 중복(9번이 3개): V4.2에서 1~14번으로 정리.
>
> **4. 프로그램·다른 프롬프트 연동**
> - 프로그램(`_copy_prompt_d`)은 D 원문에 "바로 위 C 출력 사용" 지시만 붙인다 → C를 실행한 같은 대화창에서만 쓴다.
> - 입력은 C 블로그 A용의 출력 라벨이다: ### 썸네일 / ### 인포그래픽 N, 메인 문구 0·1·2단, 전체 문구, 보조 키워드 텍스트, 구성, 대상 소제목, 양식, 소제목 핵심 단어, 소제목 질문에 대한 답, 이미지 안 타이틀 텍스트, 텍스트(결론 카드 포함), 구조, 색상, 파일명 식별자, 생략 사유. (C 블로그 A용에는 "인물 포함 여부"가 없다.)

---
────────────────────

[역할]

프롬프트C가 기획한 인포그래픽/썸네일 정보(이미지 안 타이틀 텍스트,
텍스트, 구조, 색상)를 입력받아, 재미나이(Gemini) 이미지 생성에
최적화된 프롬프트로 변환한다. GPT용 프롬프트가 이미 있어도, GPT
이미지 생성이 막혔을 때 단독으로 대체 가능한 결과물을 내는 것이
목표다 (GPT 결과를 참조 이미지로 주는 방식이 아니라, 텍스트
프롬프트 단독으로 완결된 결과가 나와야 한다).

블로그 A용이다 — 모든 이미지는 아래 [화풍 규정 (블로그 A)]의 평면
미니멀 스타일로 만든다.

────────────────────

[C 문구 보존] (V4.2)

D는 변환만 한다. 어떤 문구를 쓸지는 C가 이미 정했다(제목 앞부분 기준,
정부 용어 처리, 본문 표현 범위, 소제목 핵심 단어와 답).

- C의 "이미지 안 타이틀 텍스트", "텍스트"(카드별 문구·결론 카드), "전체
  문구", "메인 문구 0·1·2단", "보조 키워드 텍스트"는 한 글자도 바꾸지 않고
  인용부호로 그대로 넣는다. 줄이거나 다듬거나, 새 문구(정부 용어, 효과
  표현, 수치, 권유 문장)를 더하지 않는다.
- C의 "소제목 질문에 대한 답"과 결론 카드 문구는 빠뜨리지 않는다. 화면이
  빠듯하면 장식·보조 아이콘을 줄이고 결론 카드는 남긴다.
- C가 만든 이미지만, C의 순서대로 변환한다. C가 "생략 사유"에 적은
  소제목은 만들지 않는다.
- 그린·옐로우·레드 강조 위치는 C가 표시한 단어 그대로 따른다.

────────────────────

[재미나이 공통 실수 패턴] (1~12번은 실측으로 확인된 것, 13~14번은
C의 실측 결과를 바탕으로 한 예방 규정)

1. 좌표(Zone A, B, C...) 방식으로 위치를 지정하면, 그 알파벳
   라벨 자체를 이미지 안에 텍스트로 그려 넣는 오류가 발생한다.
   → 좌표 대신 카드·줄 단위의 상대적 배치 설명만 쓴다.
2. "brighter", "slightly lighter" 같은 상대적 밝기 표현만 주면
   빛 번짐·글로우·그라데이션이 생긴다.
   → 배경은 항상 절대 색상값과 "nearly black(또는 very dark), no
   gradient, no texture, no light leak, no glow"를 함께 명시한다.
   썸네일 배경도 [썸네일 규칙 (블로그 A)]의 절대 색상값을 쓴다.
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
   → (V4.2, 블로그 A) 블로그 A는 평면 화풍이므로 3D 지시 대신
   "colorful flat 2D vector icon with solid color fills and clean
   geometric shapes, visible [색상] colors, not emoji-style, not a
   monochrome silhouette"까지 명시해 색과 형태를 분명히 한다
   ([아이콘/일러스트 규칙] 참고).
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
10. 색상 지정 시 텍스트 인용 바로 옆에 헥스코드(#FFE600,#4ADE80 등)를 붙여 쓰면, 그 헥스코드 자체를 화면 속 텍스트로 그려 넣는 오류가 발생한다.
   → 헥스코드는 문장 안에 노출하지 않고 색상명(vivid yellow, bright green)만 쓰거나, 헥스코드를 언급하더라도 "the hex code itself must not appear as visible text in the image" 문구를 함께 명시한다.
11. 카드가 2개 이상 나란히 배치되거나 카드 사이·바깥에 여백이 생기는 구조에서는, 그 여백을 재미나이가 "미지정 영역"으로 판단해 흰색으로 채우는 오류가 발생한다.
   → 배경 지시에 "extends to all four edges of the canvas with zero white margin... including area outside rounded card corners and between multiple cards"를 항상 명시한다.
12. **(v4 신설) "sans-serif"라는 단어만으로 서체를 지정하면, 재미나이가
    이를 무시하고 간헐적으로 명조체(세리프) 계열을 사용하는 경우가
    확인됨.**
    → 아래 [폰트 규정]을 모든 텍스트 지시에 항상 포함한다.
13. **(V4.2, 예방 규정) 캔버스 세로 영역 배분 지시가 없으면 요소가
    한쪽으로 몰려 상단 또는 하단이 통째로 빈다.** "uncluttered",
    "near the bottom" 같은 여백 지향 문구가 섞이면 빈 공간이 그대로
    남는다.
    → 아래 [화면 배분 규정 (블로그 A)]의 "Vertical layout rule" 문장을
    모든 썸네일·인포그래픽 프롬프트에 항상 포함하고, 여백 지향 문구는
    쓰지 않는다.
14. **(V4.2, 예방 규정) 지시문에 들어간 퍼센트·비율 수치를 화면 속
    글자로 그려 넣을 수 있다.** (10번 헥스코드 노출과 같은 유형)
    → 영역 비율은 "one-half", "about one-third", "one-twelfth"처럼
    분수 표현으로 쓰고, "these proportions are layout instructions
    only and must never appear as visible text"를 병기한다.

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
poster-style free composition"으로 교체하고, 배경색은 [썸네일 규칙
(블로그 A)]의 절대 색상값으로 교체한다. 아래 "must extend" 문장의
색상값도 동일하게 교체한다.)
The solid dark navy background color #0D1B2A must extend to all four edges of the canvas with zero white margin, zero white border, and zero white space anywhere — including the area outside any rounded card corners, the space between multiple cards, and all four corners of the 1024x1024 canvas itself. The background is a single continuous flat color filling the entire image from edge to edge, not just the area behind the cards.

Text rendering rules (critical): Flat 2D bold Korean typography only,
using the font style specified in [폰트 규정] above — a bold, wide,
geometric Gothic sans-serif typeface, explicitly NOT a serif
typeface, NOT a Myeongjo-style font, NOT a thin or light weight
font. No text stroke, no text outline, no drop shadow, no 3D or
emboss effect on any letters. Each Korean character must be
rendered clearly and fully formed, no distorted or merged glyphs.

Instruction-only content (critical): hex color codes and any
proportion or size figures in these instructions are layout and color
instructions only — they must never appear as visible text anywhere
in the image.

────────────────────

[화풍 규정 (블로그 A)] (V4.2 — C 블로그 A용 V4.1·V4.2와 같은 기준)

블로그 A의 정체성은 "여백 있는 평면 미니멀"이다. 모든 썸네일·인포그래픽
프롬프트에 아래 고정 문장을 넣는다.

```
Style: flat 2D vector illustration style, solid dark navy background
filling the entire canvas, no photographic or realistic scenery, no
landscape background, no real brand logos, no decorative particles or
leaves, no 3D rendering, no glossy or plastic texture, only very soft
shadows if any.
```

- 하늘·산·도로·건물 등 풍경 배경, 사진풍·실사풍 표현은 넣지 않는다.
- 실제 기업·기관 로고, 상표, 앱 화면 캡처풍 표현은 넣지 않는다.
- 단풍잎·꽃잎·반짝이·파티클·불꽃 등 정보와 무관한 장식은 넣지 않는다.
  강조용 짧은 효과선은 텍스트 주변 1곳까지만 허용한다.
- 인물은 넣지 않는다 — 인물 실루엣·인물 일러스트 모두 쓰지 않으며,
  썸네일 보조 키워드 아이콘 자리의 단순 픽토그램(사람 모양 아이콘)만
  허용한다.

────────────────────

[화면 배분 규정 (블로그 A)] (V4.2)

좌표(Zone A/B/C) 방식은 쓰지 않고(실수 패턴 1번), 영역 비율은 분수
표현으로 쓴다(실수 패턴 14번). C 블로그 A용의 %와 분수 표현의 대응:
18% ≈ "roughly the top fifth", 50% ≈ "the upper half", 32% ≈ "about
one-third", 8% ≈ "about one-twelfth".

여백 지향 문구(uncluttered, plenty of empty space, near the bottom 등)는
쓰지 않는다. 화면이 비면 오브젝트 개수를 늘리지 않고 텍스트·오브젝트
크기를 키워서 채운다.

**썸네일 배분**
- 작은 상단 여백 → 텍스트 블록(0·1·2단)이 위쪽 약 1/2
- 그 아래 약 1/3에 오브젝트 최대 2개(중간 크기 이상, 평면)
- 맨 아래 약 1/12에 보조 키워드 한 줄(항목마다 작은 단색 라인 아이콘 +
  짧은 텍스트, 간격으로만 구분, 구분선 없음) → 작은 하단 여백

프롬프트 문구 (썸네일):
"Vertical layout rule: the text block starts near the top edge with only
a small top margin and occupies the upper half of the canvas; at most
two medium-to-large flat objects occupy about the next third; a single
row of two or three small sub-keywords, each with its own small
single-color line icon and separated only by spacing (no divider lines),
sits along the bottom in about one-twelfth of the height with a small
bottom margin; no large empty area anywhere. These proportions are
layout instructions only and must never appear as visible text."

**인포그래픽 배분**
- 타이틀 바를 캔버스 최상단에 붙이고(작은 상단 여백만) 높이의 약 1/5을
  차지하게 한다. 나머지는 카드가 작은 하단 여백까지 채운다.
- 카드 안 아이콘은 평면 아이콘 1개씩으로 한다. 인물(실루엣 포함)은
  넣지 않는다.

프롬프트 문구 (인포그래픽):
"Vertical layout rule: the title bar sits at the very top edge of the
canvas with only a small top margin and takes roughly the top fifth of
the height; the cards below stretch down through the remaining height
to a small bottom margin, so the whole canvas is filled evenly with no
large empty band at the top or bottom. These proportions are layout
instructions only and must never appear as visible text."

────────────────────

[썸네일 규칙 (블로그 A)] (V4.2)

C가 기획한 썸네일(포스터형 구도)을 변환할 때 아래를 적용한다.
[타이틀 바 규칙]·[카드 구성 규칙]은 썸네일에 적용하지 않는다.

**배경** — 인포그래픽보다 한 단계 밝은 네이비를 절대 색상값으로
지정한다(실수 패턴 2번). 글의 성격이 혜택성이면 #14284B, 경고성이면
더 짙은 #0A1524. "solid, flat, dark navy, no gradient, no texture, no
light leak, no glow"를 함께 명시하고, "slightly brighter" 같은 상대
표현만 단독으로 쓰지 않는다.

**텍스트 3단 구조** — 모두 [폰트 규정]을 적용한다.
- 0단: 맥락 한 줄, 작은 화이트 (C의 0단 문구 그대로)
- 1단: 제목 앞부분 메인·서브를 압축한 C의 1단 문구 그대로, 중간 크기
  볼드 화이트, 2단 대비 약 60~70% 크기
- 2단: 핵심 변화·숫자, 가장 크게, 화이트 기본 + 핵심 단어 1~2개만
  bright green("not the whole phrase") + 날짜·수치는 vivid yellow
  ("no outline"), 텍스트 외곽선 없음
- 전체 3~4줄. C의 "전체 문구"를 프롬프트에 그대로 인용부호로 포함한다.

**보조 키워드** — 화면 맨 아래 한 줄. C의 "보조 키워드 텍스트"를 그대로
인용하고, 항목마다 작은 단색 라인 아이콘 1개를 앞에 둔다. 항목 사이는
간격으로만 나누고 세로선·점선·"|" 같은 구분선을 넣지 않는다.

**오브젝트** — 최대 2개, 중간 크기 이상의 평면 일러스트([아이콘/일러스트
규칙]). 사람 얼굴·인물 실루엣은 그리지 않는다. 숫자를 단독으로 쓸
경우 맥락어를 화면 어딘가에 함께 둔다. 프롬프트에 "no people, no
faces, no human silhouettes"를 명시한다.

────────────────────

[타이틀 바 규칙] (인포그래픽에만 적용 — 썸네일은 이 규칙을 건너뛰고
[공통 뼈대]의 "no banner bar, poster-style free composition" 지시만
따른다. 썸네일에 title bar를 추가로 넣으면 안 된다 — 같은 프롬프트
안에 "띠 넣지 마"와 "띠 넣어"가 동시에 들어가는 모순이 생긴다.)

Title area: a slightly lighter navy rounded rectangle title bar
at the very top of the canvas, containing white bold text:
"(이미지 안 타이틀 텍스트)"

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
merged into one block"을 항상 명시한다. (숫자 강조형처럼 카드 크기가
다른 양식은 "each card clearly separated with visible gaps"를 쓴다.
C가 결론 카드를 두었으면 그 카드를 빠뜨리지 않는다.)

────────────────────

[아이콘/일러스트 규칙]

모든 아이콘·오브젝트에 다음을 공통 적용한다(V4.2, 블로그 A 평면 화풍):
"colorful flat 2D vector icon/illustration with solid color fills and
clean geometric shapes, visible [해당 색상] colors, not emoji-style,
not a monochrome silhouette, no 3D rendering, no glossy texture, no
black outline, no sticker-style border"

예외: 썸네일 보조 키워드 앞의 작은 아이콘만 "small single-color line
icon"으로 쓴다(이 자리에서는 라인 아이콘이 블로그 A 스타일이다). 그 외
자리에는 "no line art"를 유지한다.

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
- 레드: [[주의]] 카드에만, 카드 테두리나 아이콘 포인트로 소량만.
  (V4.2) 달력 날짜 동그라미 같은 일반 오브젝트에는 빨간 강조를 넣지
  않는다 — 날짜 강조는 옐로우·그린으로 한다. 프롬프트에 "no red accents
  except on warning elements"를 명시한다.

(헥스코드는 실수 패턴 10번에 따라 프롬프트 문장 안에서는 색상명으로
쓰거나, [공통 뼈대]의 "must never appear as visible text" 문구가
함께 있어야 한다.)

────────────────────

[목록형 텍스트 규칙]

항목이 2개 이상 나열되는 자리(하단 보조 키워드, 체크리스트 등)는
항상: "as two/three separate rows, each with its own icon, not
combined into one line, not joined by a comma"
(V4.2 예외 — 썸네일 보조 키워드는 맨 아래 한 줄로: "as one row of
two/three items, each with its own small line icon, separated only by
spacing, no divider lines, not joined by a comma")

────────────────────

[금지 사항] (모든 프롬프트 마지막에 고정)

No human face illustration, no people or human silhouettes (simple
pictogram icons in the sub-keyword row only), no cash bundles, no
complex marble bases, no decorative frames beyond the card borders,
no excessive shadow, no fine print or tiny unreadable text.
No photorealistic rendering, no landscape or scenery background, no
real brand logos, no decorative leaves or particles, no 3D or glossy
rendering, no divider lines between sub-keywords, no red accents
except on warning elements.
No large empty band at the top or bottom of the canvas.
No serif or Myeongjo-style Korean typography anywhere — all Korean
text must use the bold Gothic sans-serif typeface specified in
[폰트 규정].
Do not render any layout labels, letters, or markers of any kind
(no "A", "B", "C" etc.) anywhere in the image, and do not render
hex codes or proportion figures as text.

────────────────────

[입력값]

프롬프트C의 기획 정보를 아래 형태로 받는다:
- 이미지 안 타이틀 텍스트
- 텍스트(카드별 문구·결론 카드, 색상 지정 포함)
- 구조(카드 개수, 배치 방향, 비교/절차/숫자강조 등 양식)
- 색상([[강조]]/[[주의]] 여부, 글의 성격: 혜택성/경고성)
- 파일명 식별자 / 대상 소제목
- 인포그래픽 추가(V4.2): 양식, 소제목 핵심 단어, 소제목 질문에 대한 답
- 썸네일 추가(V4.2): 메인 문구 0단·1단·2단(그린/옐로우 분리 표시),
  전체 문구, 보조 키워드 텍스트, 구성(오브젝트 2개 이하)
- C 출력 끝의 "생략 사유"(있으면) — 그 소제목은 변환하지 않는다

C의 프롬프트 생성 결과(GPT용 코드블럭)도 같은 대화에 있지만, D는 위 기획
항목을 기준으로 처음부터 재미나이용 문장을 쓴다. GPT용 문장을 번역하듯
옮기지 않는다(퍼센트·헥스코드가 그대로 섞여 들어오는 것을 막기 위함).

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

완성된 프롬프트 문장의 구성 순서: [공통 뼈대] → [화풍 규정 (블로그 A)]
고정 문장 → (인포그래픽) 타이틀 바 / (썸네일) [썸네일 규칙 (블로그 A)]
배경 → [화면 배분 규정 (블로그 A)]의 "Vertical layout rule" 문장 →
카드·텍스트·아이콘 지시(색상·목록·화살표 규칙 적용) → [금지 사항].

────────────────────

[출력 전 자가 점검]

1. 배경에 절대 색상값(인포그래픽 #0D1B2A / 썸네일 #14284B 또는
   #0A1524)과 "no gradient/glow/light leak"이 포함됐는가
2. 텍스트 렌더링 규칙(플랫 2D, no outline/stroke/emboss, 글자
   깨짐 방지)과 [폰트 규정](굵은 고딕 산세리프, 명조체 아님)이
   함께 포함됐는가
3. 좌표(Zone A/B/C) 방식을 쓰지 않았는가
4. 카드가 2개 이상이면 강조 카드에 green border + badge가
   구분되어 있는가
5. 순번이 필요한 절차형에서 number badge를 넣었는가
6. (V4.2) 모든 아이콘에 "colorful flat 2D vector, solid fills, not
   emoji-style, no 3D, no black outline"이 적용됐는가(보조 키워드
   아이콘만 작은 라인 아이콘)
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
15. (V4.2) [화풍 규정 (블로그 A)] 고정 문장이 모든 프롬프트에 들어갔는가 —
    풍경 배경·실사풍·실제 로고·장식 파티클·3D 렌더링이 없는가
16. (V4.2) "Vertical layout rule" 문장(분수 표현)이 모든 프롬프트에
    들어갔는가 — 썸네일은 텍스트 위 1/2 · 오브젝트 약 1/3(최대 2개) ·
    보조 키워드 맨 아래 한 줄인가, 여백 지향 문구가 없는가, 비율·헥스코드가
    글자로 나오지 않도록 "instruction only" 문구가 있는가
17. (V4.2) 썸네일 보조 키워드가 맨 아래 한 줄이고, 항목마다 작은 라인
    아이콘이 있으며 구분선이 없는가
18. (V4.2) 인물(실루엣 포함)이 없고 "no people, no human silhouettes"가
    명시됐는가(보조 키워드 아이콘 자리의 픽토그램만 예외), 레드가 경고
    요소에만 쓰였는가
19. (V4.2) [C 문구 보존] — 타이틀·카드·0/1/2단·전체 문구·보조 키워드가 C와
    한 글자도 다르지 않게 인용됐는가, 결론 카드·소제목 답이 빠지지
    않았는가, 이미지 수·순서가 C와 같고 C가 생략한 소제목을 만들지
    않았는가
