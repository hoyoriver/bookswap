# 교환독서 — 서비스 구조 가이드북

> 클로드 코드로 만든 교환독서 앱의 코드 구조를 기획자 관점에서 정리한 학습 문서입니다.

---

## 목차

1. [서비스 개요](#1-서비스-개요)
2. [기술 스택](#2-기술-스택)
3. [파일 구조](#3-파일-구조)
4. [index.html 구조](#4-indexhtml-구조)
   - [head — 설정 영역](#41-head--설정-영역)
   - [body — 화면 영역](#42-body--화면-영역)
   - [script — 동작 영역](#43-script--동작-영역)
5. [데이터 흐름](#5-데이터-흐름)
6. [로컬 실행 방법](#6-로컬-실행-방법)

---

## 1. 서비스 개요

교환독서는 책을 돌려 읽는 소규모 모임을 관리하는 웹 앱입니다.

**핵심 기능**
- 모임 만들기 / 초대 코드로 합류
- 멤버별 책 소지 현황 관리
- 교환 이력 기록 및 자동 순환 처리
- 내 기록 (참여 중인 모임의 책 목록)
- 통계 (모임별 교환 횟수)

---

## 2. 기술 스택

| 역할 | 기술 | 설명 |
|---|---|---|
| 화면 | HTML / CSS / JavaScript | 프레임워크 없이 순수 웹 기술만 사용 |
| 데이터베이스 | Supabase | 클라우드 DB. 직접 서버를 운영하지 않아도 됨 |
| 책 검색 | 네이버 책 검색 API | 책 제목·저자·표지 이미지 제공 |
| 배포 | Vercel | GitHub에 push하면 자동 배포 |
| 설치형 웹 | PWA | 앱스토어 없이 홈화면에 설치 가능 |

---

## 3. 파일 구조

```
bookswap/
│
├── index.html          ← 앱의 전부 (화면 + 디자인 + 로직)
│
├── api/
│   └── books.js        ← 책 검색 API (Vercel 배포용)
│
├── server.js           ← 로컬 개발용 서버 (Node.js)
├── server.py           ← 로컬 개발용 서버 (Python 대안)
│
├── manifest.json       ← PWA 앱 명세 (이름·아이콘·테마색)
├── sw.js               ← Service Worker (오프라인 캐싱)
├── icon-192.png        ← 앱 아이콘 (Android)
├── icon-512.png        ← 앱 아이콘 (Android 대형)
├── apple-touch-icon.png← 앱 아이콘 (iPhone 홈화면)
│
├── package.json        ← Node.js 프로젝트 설정
├── vercel.json         ← Vercel 배포 설정
├── .env                ← API 키 보관 (GitHub 비공개)
├── .env.example        ← .env 작성 가이드 (GitHub 공개)
├── .gitignore          ← GitHub에 올리지 않을 파일 목록
│
├── datamodel.html      ← 데이터 구조 설계 문서
├── deck.html           ← 서비스 발표용 슬라이드
└── figma-deck.md       ← Figma 기획 문서
```

### 파일 역할 요약

**사용자에게 보이는 파일**

| 파일 | 역할 |
|---|---|
| `index.html` | 앱 화면 전체 |
| `datamodel.html` | 데이터 구조 설계 문서 (내부용) |
| `deck.html` | 서비스 소개 슬라이드 |

**서버 / API**

| 파일 | 역할 |
|---|---|
| `server.js` | 로컬 개발 서버. 네이버 API를 브라우저 대신 중계 |
| `server.py` | 같은 역할의 Python 버전 |
| `api/books.js` | Vercel 배포 환경에서 동작하는 API |

> **왜 서버가 필요한가?** 네이버 API는 보안 정책상 브라우저에서 직접 호출하면 차단됩니다. 서버가 중간에서 대신 요청을 보내줘야 합니다.

**PWA (앱처럼 설치 가능)**

| 파일 | 역할 |
|---|---|
| `manifest.json` | "이 웹사이트는 앱입니다"라고 브라우저에 알려주는 명세서 |
| `sw.js` | 앱 파일을 기기에 저장해 오프라인에서도 열리게 함 |
| `icon-*.png` | 홈화면에 표시되는 앱 아이콘 |

**설정 / 보안**

| 파일 | 역할 |
|---|---|
| `.env` | API 키·비밀번호. **절대 GitHub에 올리면 안 됨** |
| `.env.example` | .env 작성법 안내용 샘플 (공개해도 되는 버전) |
| `.gitignore` | GitHub에 올리지 않을 파일 목록 |

---

## 4. index.html 구조

파일 하나가 크게 3개 영역으로 나뉩니다.

```
index.html
├── <head>    (line 1–297)    → 설정 (폰트, 색상, 레이아웃 규칙)
├── <body>    (line 299–557)  → 화면 (HTML 구조)
└── <script>  (line 560–1405) → 동작 (JavaScript 로직)
```

---

### 4.1 `<head>` — 설정 영역

#### 디자인 토큰 (CSS 변수)

색상·폰트를 변수로 선언해 디자인을 일관되게 유지합니다.  
색을 바꾸고 싶을 때 이 한 곳만 수정하면 전체에 반영됩니다.

```css
:root {
  --bg: #f7f5f2;       /* 배경색 */
  --surface: #ffffff;  /* 카드·모달 배경 */
  --accent: #3d3530;   /* 포인트색 (버튼, 사이드바) */
  --muted: #6b6460;    /* 흐린 텍스트 */
}
```

#### 컴포넌트별 CSS

| CSS 블록 | 담당 UI |
|---|---|
| `.app`, `.sidebar`, `.main-wrapper` | 전체 레이아웃 (2단 그리드) |
| `.nav-item`, `.logo` | 사이드바 메뉴 |
| `.topbar` | 상단 바 |
| `.moim-card` | 홈 화면 카드 |
| `.moim-list-item` | 모임 목록 행 |
| `.filter-chip` | 전체·진행중·완료 필터 버튼 |
| `.cycle-node`, `.holder-table` | 모임 상세 (순환 시각화, 현황 테이블) |
| `.my-books-grid` | 내 기록 책 그리드 |
| `.stats-grid`, `.stat-card` | 통계 숫자 카드 |
| `.modal-backdrop`, `.modal` | 모달 공통 스타일 |
| `.book-search-results` | 책 검색 드롭다운 |
| `.mobile-tabbar` | 모바일 하단 탭바 |
| `@media (max-width: 768px)` | 모바일 반응형 처리 |

---

### 4.2 `<body>` — 화면 영역

#### 전체 레이아웃 구조

```
body
├── .app (2단 그리드)
│   ├── .sidebar                   ← 좌측 사이드바 (PC)
│   │   ├── .logo                  → "교환독서"
│   │   └── .nav-section           → 홈 / 모임 / 내기록 / 통계 / 코드참여
│   │
│   └── .main-wrapper
│       ├── .topbar                ← 상단 바 (제목 + 버튼)
│       └── .main                  ← 페이지 컨테이너
│           ├── #page-home         → 홈
│           ├── #page-moim         → 모임 목록
│           ├── #page-detail       → 모임 상세
│           ├── #page-mybooks      → 내 기록
│           └── #page-stats        → 통계
│
├── .mobile-tabbar                 ← 하단 탭바 (모바일 전용)
│
└── 모달 7개
    ├── #modal-create-moim         → 모임 만들기
    ├── #modal-exchange            → 교환 기록하기
    ├── #modal-add-book            → 책 추가
    ├── #modal-join                → 모임 합류
    ├── #modal-order               → 순환 순서 수정
    ├── #modal-edit-book           → 책 수정
    └── #modal-enter-code          → 초대 코드 입력
```

#### 페이지 전환 방식

페이지 5개가 **동시에 HTML에 존재**하지만, `.active` 클래스가 붙은 것만 화면에 표시됩니다.  
실제로 다른 주소로 이동하는 게 아니라 보였다·숨겼다 하는 구조입니다.

```css
.page        { display: none; }   /* 기본: 숨김 */
.page.active { display: block; }  /* active일 때만 표시 */
```

이런 구조를 **SPA(Single Page Application)** 라고 합니다.

---

### 4.3 `<script>` — 동작 영역

#### Supabase 연결

```js
const sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

클라우드 DB에 접속하는 연결선입니다. 이 한 줄로 DB 읽기·쓰기가 가능해집니다.

#### 데이터 CRUD 함수

> CRUD = Create(생성) · Read(읽기) · Update(수정) · Delete(삭제)

| 함수 | 역할 |
|---|---|
| `loadMoims()` | DB에서 내 모임 목록 불러오기 |
| `upsertMoim(moim)` | 모임 저장/수정 (생성과 수정을 하나로 통합) |
| `findMoimByCode(code)` | 초대 코드로 모임 찾기 |
| `deleteMoimById(id)` | 모임 삭제 |

#### 네비게이션

```js
function navigate(page, moimId) { ... }
```

페이지 전환 + 탑바 제목 변경 + 탭바 활성화를 한 번에 처리합니다.

#### 페이지 렌더 함수

화면을 그리는 함수들입니다. DB에서 데이터를 받아 HTML 문자열로 만들어 화면에 끼워 넣습니다.

| 함수 | 역할 |
|---|---|
| `renderHome()` | 진행 중인 모임 카드 그리기 |
| `renderMoimList()` | 모임 목록 + 필터 처리 |
| `renderDetail(moimId)` | 모임 상세 (순환 현황·책 현황·교환 이력) |
| `renderMyBooks()` | 전체 책 그리드 + 모임별 필터 |
| `renderStats()` | 숫자 통계 카드 그리기 |

#### 모달 + 액션 함수

| 함수 | 역할 |
|---|---|
| `saveMoim()` | 모임 생성 저장 |
| `confirmExchange()` | 교환 이력 기록 |
| `saveAddBook()` | 책 추가 |
| `triggerAutoRotate()` | 전체 자동 순환 처리 |
| `saveOrder()` | 순환 순서 저장 |
| `saveEditBook()` | 책·소지자 수정 |
| `closeMoim()` | 모임 종료 |
| `confirmJoin()` | 초대 코드로 모임 합류 |

#### 책 검색 흐름

```
사용자 타이핑
    ↓
debounceSearch()    → 400ms 대기 (타이핑 중에는 API 호출 안 함)
    ↓
searchBooks()       → /api/books 호출 → 네이버 API 결과 반환
    ↓
드롭다운 표시
    ↓
selectBook() 클릭   → 책 선택 완료
```

> **debounce란?** 사용자가 타이핑할 때마다 API를 호출하면 서버에 과부하가 걸립니다. 마지막 입력 후 일정 시간(400ms)이 지나야 호출하는 기법입니다.

#### 유틸 함수

| 함수 | 역할 |
|---|---|
| `nextExchangeDday(m)` | 다음 교환까지 D-day 계산 |
| `uid()` | 고유 ID 생성 |
| `esc(s)` | 보안 처리 (사용자 입력이 코드로 실행되지 않게 차단) |
| `fmtDate(str)` | 날짜 포맷 변환 (2025-05-14 → 2025.05.14) |

#### 초기 실행 흐름

앱이 열리면 `initApp()`이 자동 실행됩니다.

```
페이지 열림
    ↓
URL에 ?join=CODE 있는지 확인   → 있으면 초대 합류 모달 열기
    ↓
DB에서 내 모임 불러오기 (loadMoims)
    ↓
홈 화면 렌더링 (renderHome)
```

---

## 5. 데이터 흐름

```
[사용자 액션]
  버튼 클릭 / 폼 입력
        ↓
[JavaScript 함수]
  save* / confirm* / trigger*
        ↓
[Supabase DB]
  upsertMoim() → 클라우드에 저장
        ↓
[화면 갱신]
  render*() → 새 데이터로 HTML 다시 그리기
```

데이터는 항상 **JS 변수 `moims`** 에 올라와 있고, DB와 동기화됩니다.  
화면은 `moims` 배열을 읽어서 HTML로 변환해 표시합니다.

---

## 6. 로컬 실행 방법

### 사전 준비

1. [네이버 개발자 센터](https://developers.naver.com)에서 책 검색 API 키 발급
2. `.env.example`을 복사해 `.env` 파일 생성 후 키 입력

```
NAVER_CLIENT_ID=발급받은_클라이언트_ID
NAVER_CLIENT_SECRET=발급받은_클라이언트_SECRET
```

### Node.js로 실행

```bash
npm install
npm start
# → http://localhost:3000 에서 확인
```

### Python으로 실행

```bash
pip install -r requirements.txt
python server.py
```

---

## 참고: 기획자가 알아두면 좋은 개념

| 개념 | 이 앱에서의 예시 |
|---|---|
| **SPA** (단일 페이지 앱) | 페이지 이동 없이 `.active` 클래스로 화면 전환 |
| **CRUD** | 모임 만들기(C) / 목록 보기(R) / 책 수정(U) / 모임 삭제(D) |
| **API** | 네이버 책 검색 — 외부 서비스의 데이터를 가져다 씀 |
| **BaaS** | Supabase — 서버 없이 쓰는 클라우드 DB |
| **PWA** | manifest.json + sw.js — 웹을 앱처럼 설치 가능하게 |
| **debounce** | 책 검색 — 타이핑마다 API 호출 방지 |
| **환경변수** | .env — API 키를 코드에 직접 쓰지 않고 외부에서 주입 |
| **CSP / XSS 방지** | `esc()` 함수 — 사용자 입력이 코드로 실행되지 않게 처리 |
