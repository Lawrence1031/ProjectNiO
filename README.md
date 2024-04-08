![logo](https://github.com/Lawrence1031/ProjectNiO/assets/144416099/15501d63-298d-418f-a142-4a1b6682a5db)
----
[다운로드](https://drive.google.com/file/d/1WrhfbnjKQoH-L85KAarEae_8lhXK5iUZ/view?usp=sharing)

2D 로그라이크 덱 빌딩 게임
----
<details>
  <summary>Sample Image</summary>
  
  <img width="696" alt="001" src="https://github.com/Lawrence1031/ProjectNiO/assets/144416099/f2621db0-4096-4759-84c6-63bdc9220d59">

  <img width="696" alt="002" src="https://github.com/Lawrence1031/ProjectNiO/assets/144416099/f8ee675b-1181-45a2-9d0e-6db04063242a">

  <img width="696" alt="003" src="https://github.com/Lawrence1031/ProjectNiO/assets/144416099/9b6b9bbb-3343-443c-b3a8-98eacb3725dc">

</details>

프로젝트 정보
----
- 제작기간 2023.07.03 ~ 2023.07.31
- 참여인원 3명
- 맡은 역할 - 게임 내 이벤트, 몬스터, 게임 세계관, 스토리, 카드 디자인

사용 기술
-----
- Python(pygame)
- OpenCanvas
- Stable Diffusion

Structure
----
<details>
<summary>Structure</summary>
<div markdown="1">

![Menu](https://github.com/Lawrence1031/ProjectNiO/assets/144416099/0c26b32d-6fbe-4f72-8ee6-5374543be009)

![InGame](https://github.com/Lawrence1031/ProjectNiO/assets/144416099/881d7302-214b-4210-b2f7-f7b880670da4)

![GameCycle](https://github.com/Lawrence1031/ProjectNiO/assets/144416099/ac392373-0497-450d-9398-b69f72f0a05d)


</div>
</details>


핵심 기능
----
### 1. 로그라이크
> 게임이 한 회차가 종료된 후, 해당 회차의 결과를 토대로 점수를 매겨 자원을 획득합니다.
> 
> 획득한 자원으로 다음 회차의 덱 선택 시에 카드를 추가로 가지고 시작할 수 있습니다.
> 
> [코드](https://github.com/Lawrence1031/ProjectNiO/blob/main/release_1009/scene/s12_result.py)

</br>

### 2. 덱 빌딩 시스템
> 이 게임에서 덱은 적과 전투하는 방법임과 동시에 플레이어의 체력을 나타냅니다.
>
> 몬스터와의 전투에서 일정 대미지를 받으면 랜덤으로 덱에 있는 카드 중 한 장이 삭제됩니다.
> 
> [코드](https://github.com/Lawrence1031/ProjectNiO/blob/main/release_1009/scene/s08_battleevent.py#L449)

</br>

### 3. 이벤트 시스템
> 이 게임은 하나의 방에서 다른 방으로 이동하는 경우에 확률에 따라 여러 이벤트 중에 하나의 이벤트가 발생합니다.
> 
> 방에 따라서 정해진 텍스트 이벤트, 배틀 이벤트, 시나리오 이벤트 중의 하나가 확률로 발생합니다.
> 
> 아래의 링크는 첫번째 방에 대한 코드입니다.
> 
> 첫번째 방에 방문하면 최초 방문 시 발생하는 이벤트가 있으며 그 이후에는 다른 이벤트가 발생합니다.
>
> 또, 이 방에 방문하는 것으로 다른 방도 열리도록 구현하였습니다.
> 
> [코드](https://github.com/Lawrence1031/ProjectNiO/blob/main/release_1009/scene/s06_stage1.py#L490)

</br>

기획문서
----
<details>
  <summary>
    
  </summary>
</details>
