# 예지보전 실습판 — learn-pdm-lite-jyp

설비 두 대의 진동 그래프 한 장으로 노이즈와 추세를 가르는 10분 실습(블록 3개). 수업은 Claude Code 스킬 `/learn-pdm-lite-jyp`가 진행한다 (Skills as Curriculum). 이 강의는 jyp가 course-forge로 직접 만들었다.

- **결과 대시보드**: https://ypjungg88-netizen.github.io/learn-pdm-lite-jyp/
- 처음이면 [GUIDE.md](GUIDE.md)부터. 기본 환경은 Claude 데스크톱 앱(Code 탭). VS Code는 GUIDE 부록 B

![결과 대시보드](.claude/skills/learn-pdm-lite-jyp/assets/answers/preview.png)

## 설치 — 한 줄

Claude Code 입력칸에 붙여 넣는다.

```
npx skills add ypjungg88-netizen/learn-pdm-lite-jyp --agent claude-code --global --yes 를 실행해 줘
```

새 세션에서 `/learn-pdm-lite-jyp`를 입력하면 수업이 시작된다. zip을 받았다면 GUIDE.md 2단계대로 설치한다.

## 블록

| Block | 주제 | 끝나면 생기는 것 |
|---|---|---|
| 0 | 준비 (2분) | `pdm-lite-work/env_check.txt` |
| 1 | 노이즈 vs 추세 (6분 · 퀴즈 1) | 그래프 한 장 `index.html` · 추세 시작 13:00 |
| 2 | 공개 (2분) | 공개 점검 결과 · 짝에게 보낼 메시지 |

## 수업 방식

| 구분 | 내용 |
|---|---|
| 목표 — AI Native | AI에게 맡기는 것이 기본인 방식으로 일한다 |
| 방법 — Skills as Curriculum | 스킬이 블록마다 설명 → 실습 → STOP → 확인·퀴즈를 진행한다 |
| 형식 — 자율학습 | 강사 없이 자기 속도로, 퀴즈로 스스로 점검한다 |

## 원본 강의와 데이터 출처

| 자료 | 출처 | 구분 |
|---|---|---|
| 본 강의 덱 | keerhee/kma-auto-genai-3-1 · `Day5_예지보전/Day5_3_Main_자동차예지보전AI활용.pdf` (14·19·20·27장) | 원본 강의 |
| 실습판 흐름 | 같은 저장소 · `보충교재/Day6_최종프로젝트/06_커리큘럼만드는스킬/최종패키지/1_Day5_Course_Forge/` | 원본 강의 |
| 설비센서 50건 | 같은 저장소 · `data/Day5/Day5_설비센서_50건_가상.csv` → `assets/lab/day5_sensor_50_synthetic.csv` | **가상 데이터** |

추세 시작 규칙(진동이 세 번 연속 오르기 시작한 시각)은 이 실습판이 정한 가정이다.

## 개정 이력

| 날짜 | 바뀐 점 |
|---|---|
| 2026-10-31 | 첫 판 — 블록 3개, 퀴즈 1문항 |

## 만든 방법

- `/course-forge`로 만들었다. 제작 기록(원본 요약·커리큘럼·검수 결과)은 `forge/`에 있다.
- 출처: 원본 강의 저장소 https://github.com/keerhee/kma-auto-genai-3-1
