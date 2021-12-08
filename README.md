# [Assignment 7] Wanted-cardoc-Preonboarding

원티드x위코드 백엔드 프리온보딩 과제 7

- 과제 제출 정보

  - 기업명 : 카닥
  - 제출자 : 문승준

  <br>

## 1. 과제 안내

####  사용자 생성 API

- ID/Password로 사용자를 생성하는 API.
- 인증 토큰을 발급하고 이후의 API는 인증된 사용자만 호출할 수 있다.

#### 사용자가 소유한 트림과 타이어 정보를 저장하는 API

- 자동차 차종 ID(trimID)를 이용하여 사용자가 소유한 자동차 정보를 저장한다.

- 한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있도록 해야한다.

  즉 사용자 정보와 trimId 5쌍을 요청데이터로 하여금 API를 호출할 수 있다는 의미이다.

#### 사용자가 소유한 타이어 정보 조회 API

- 사용자 ID를 통해서 2번 API에서 저장한 타이어 정보를 조회할 수 있어야 한다.

  <br>

## 2. 사용 기술 및 tools

> - Back-End : Python, Django, SQLite
> - Deploy : AWS EC2, Docker
> - ETC : GIT, GITHUB, POSTMAN

<br>

## 3. 모델링

![스크린샷 2021-11-29 오전 3 53 57](https://user-images.githubusercontent.com/72376931/143784776-42ed0054-90b3-4c22-b4a1-a0711f375ed9.png)


<br>

## 4. 프로젝트 구조와 구현 방법

### 프로젝트 구조

```
.
├── cardoc
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── cars
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── Dockerfile
```

<br>

### 사용자 생성 및 로그인 기능

- users app 
- 정규 표현식으로 username과 password의 validation
- password는 bcrpyt 라이브러리로 암호화
- 로그인 성공시 jwt 라이브러리를 활용해 access token 발급
- 인증 인가를 위한 로그인 데코레이터 구현

### 사용자별 자동차 정보 저장 기능

- cars app
- 사용자와 트림 정보, 타이어 정보를 최대 5개까지 저장
- 타이어의 value는 {width}/{profile}R{diameter} 형태로 각 값마다 DB에 따로 저장

### 사용자별 자동차 정보 조회 기능

- cars app
- header의 토큰값에 따라 사용자 정보를 가져오고 등록된 자동차 정보를 조회

### 트림별 상세 정보 조회 기능

- cars app
- path parameter로 trim id를 받아서 해당하는 정보를 조회

### 유닛 테스트

- 각 앱별 test.py를 작성하여 유닛 테스트를 진행하였습니다.

<img width="432" alt="스크린샷 2021-11-29 오전 5 04 43" src="https://user-images.githubusercontent.com/72376931/143784786-75d2e06d-6d8f-4e4d-a23f-c7c94376216d.png">


### Docker로 AWS 배포

- 로컬에서 도커 이미지를 빌드하여 도커 허브를 이용해 EC2 서버에서 배포하였습니다.
- 컨테이너 실행시 환경변수를 세팅하여 중요 정보들은 볼 수 없게끔 나타내었습니다.
- 배포 주소는 `13.125.65.20:8000` 입니다.

<br>

## 5. API Document & API Test

1. [API 명세서 링크](https://documenter.getpostman.com/view/17676214/UVJckGPS) 로 접속해 우측 상단의 `Run in Postman` 버튼을 클릭합니다.

2. 개인 Workspace로 Import(fork) 합니다.

3. Environment를 Deploy로 바꾸고 hostname이 올바른지 확인 합니다.

4. API 예시를 참고해 요청을 보냅니다.

5. 에러 핸들링은 아래 사진과 같이 확인 할 수 있습니다.

  ![스크린샷 2021-11-29 오전 5 11 38](https://user-images.githubusercontent.com/72376931/143784803-aefc23e5-c7a6-4216-b4f9-24331eb952d1.png)


<br>

## 6. 도커를 활용한 배포 과정

### 로컬 도커 이미지 빌드

1. 로컬에서 gunicorn 설치 및 `Dockerfile` 작성
2. cardoc 프로젝트 이미지 파일 빌드
3. 이미지를 도커 허브로 push

### EC2 서버 배포

1. cardoc 프로젝트 가상 환경 생성
2. 도커 허브에 push 했던 cardoc 프로젝트 이미지를 pull
3. 컨테이너 실행하며 환경변수(시크릿키)를 설정


<br>

## 7. Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 카닥에서 출제한 과제를 기반으로 만들었습니다.
