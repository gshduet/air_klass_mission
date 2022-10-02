# 프로젝트 개요

* 큐리어슬리에서 서비스 중인 에어클레스의 일부 서비스를 구현합니다.

* 에어클레스는 수강생이 강의를 구매하는 기능, 강의에 질문을 남기는 기능, 질문에 답변을 남기는 기능 등이 있습니다.
<br><br>

# 요구사항

* 수강생, 강사, 강의, 질문, 답변 모델 간의 관계를 구현해야 합니다.

* 강의 생성
  * 강의(Klass)는 강사(Master)만 생성할 수 있습니다.

* 질문 생성
  * 유저는 모든 강의에 질문을 남길 수 있습니다.
  * 작성한 질문은 삭제할 수 있습니다.
  * 답변이 달린 질문은 삭제할 수 없습니다.

* 답변 생성
  * 강사는 자신이 개설한 모든 강의에 달린 질문에 답변을 할 수 있습니다.

* 질문, 답변 확인
  * 모든 사용자는 모든 질문과 답변을 확인할 수 있습니다.

# 제약 사항

* Language : Python3
* Framework : Django, DjangoRestFramework
* SQL

***
# 기술스택

* `python 3.8`, `Django 3.1`,`DRF 3.13`
* `SQLite`
* `DRF simplejwt`

# ERD
<img src="./Airklass.png">  


# 실행 방법

* 본 프로젝트는 Python 3.8 버전에서 작성되었습니다. 해당 버전 이상의 환경에서 실행하는 것을 권장합니다.


1. Github에서 해당 프로젝트를 내려 받습니다.
> git clone https://github.com/gshduet/air_klass_mission.git

2. 서버 구동에 필요한 패키지를 내려받기 위해 디렉토리를 이동합니다.
> cd air_klass_mission/djangomission

3. `requirements.txt`을 통해 패키지를 내려 받습니다.
> pip3 install -r requirements.txt`

4. 서버를 구동합니다.
> python manage.py runserver 0:8000

# 최종 구현범위

## 구현완료
* 유저, 강사, 강의, 질문, 답변 모델 정의
* 회원가입, 로그인 기능
* 강사 지정/해제 기능


## 구현 중
* 강의 개설, 조회, 수정, 삭제
* 질문 생성, 조회, 수정, 삭제
  * 질문 리스트 조회
* 답변 생성, 조회, 수정, 삭제
  * 답변 리스트 조회

