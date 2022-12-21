# payhere_assignment
+ Python Backend (신입) 전형
+ 지원자 명 : 김영빈

<br/>

## 모델
---
모델들간의 관계(1:~)


<br/>

## API
---
총 ~개의 api를 구현하였습니다
swagger


<br/>

## 유저 
---
커스텀 유저모델을 사용 
+ 장고의 기본 유저모델은 username을 유니크한 값으로 사용하고 있고 추후에 유저모델을 변경할 경우, 커스텀 유저모델을 사용하는 것이 훨씬 더 편하다고 생각합니다

회원가입
+ 회원가입에 성공할 경우 바로 로그인상태가 될 수 있도록, 회원가입에 성공하면 바로 jwt 토큰을 반환하도록 하였습니다.
+ genericview를 사용할 경우 코드의 양이 오히려 커진다고 생각해 APIView를 사용하였습니다.

<br/>

## 인증
---

로그인
+ 로그인에 성공하면, 서버측에서 access_token과 refresh_token을 응답에 담아서 보냅니다
+ 또한 로그인에 성공한 유저의 email과 id를 함께 담아서 응답합니다

인증
+ 인증이 필요한 api를 호출할 경우, 프론트측에서 header에 access_token을 함께 보내어 인증을 진행합니다

access_token 만료
+ 만약 access_token이 만료될 경우, 서버는 정해진 status_code를 반환합니다
+ 클라이언트는 약속된 status_code를 받으면, refresh_token을 제공하여 access_token을 재발급받을 수 있는 api를 호출합니다
+ 서버는 refresh_token이 유효하면 새 access_token을 새로 발급하여 응답합니다.

로그아웃
+ 프론트측에서는 access_token과 refresh_token을 제거합니다.

<br/>

## 가계부
---

3-g
+ 고객은 원하는 레코드들의 원하는 데이터만 제시하고 싶을 것이므로, 고객이 원할 수 있는 다양한 경우의 수를  쿼리파라미터를 통해 대처하고자 했습니다
+ filtering을 통해 고객이 원하는 다양한 경우의 수를, 동적 필터링을 통해 고객이 보여주기 원하는 필드를 받아 표현하였습니다
+ 고객이 원하는유효시간을 설정할 수 있도록 하였습니다.
+ 단축url은 외부api를 사용하는 방식을 고민했으나, 의존성을 낮추고 싶어 내부적으로 구현하였습니다


## 추가여부
+ 