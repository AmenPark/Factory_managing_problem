# Factory_managing_problem
### 코딩테스트를 보고 영감을 얻어서 만들어보는 프로젝트.
### API로 응시자는 서버와 소통한다.
### 여기서는 그 API 서버 부분을 작성해보고자 한다.

## 문제
### 당신은 상상공장의 매니저이다.
### 같은 카테고리의 제품은 동일 라인을 이용해서 생산 가능하다.
### 계약의 수주와 제품 생산, 거래를 통해서 이익을 최대한 남겨야 한다.
### 제품 정보, 계약 정보는 아래에 따로 기술할 예정.

## API
### strat test
    - /start_test/으로 post.
    - {"address" : "YOUREMAIL"} 데이터 전달.
    - {"key" : "YOURKEY"}가 리턴.
    - 해당 키는 6시간동안 유효.

### start problem
    - /start_test/으로 post.
    - data : {"key" : "YOURKEY", "problem" : 1}
    - return : {"Category" :
                {"name" : "drink",
                 "items" : [{"name":"beer",
                            "duration":3,
                            "expirey": 15,
                            "production_cost" : 4},...]
                 "costs" : 500,
                 "capacity" : 50,
                 "build_time" : 3,
                 "start_num" : 1
                }
                "time_limit" : 365,
                "start_money" : 300
               }
    - 각각 카테고리-카테고리명,품목 - 품목명, 제작기한, 유통기한, 생산단가
                  생산라인 증가비용, 라인당 생산량, 생산라인 확장시간, 초기 라인숫자
                  초기 돈 보유량. 을 의미한다.

### get contract info
    - 이번에 들어온 계약을 의미한다.
    - /contrats/로 get.
    - return : {"id" : 101024
                "name" : "beer",
                "num" : 120,
                "date" : 12,
                "down_payment" : 300,
                "partial_payment" : 300,
                "penalty_payment" : 900
                }
    - 각각 id, 품목명, 수량, 납품일자, 선지급금, 후지급금, 위약금을 의미.
    
### post action
    - 이번에 들어온 계약에 대해 계약여부를 반환한다.
    - 설비 증여 및 납품내역도 반환한다.
    - data : {"contrats" : [{"id":13313,"accepted":True},...],
              "extension" : "category Name"(Optional),
              "delivery" : [{"id":13515, "item" : "beer", "num" : 40},...]}
    - return : {"day" : 4, "Failed Delivery" : 0}
    - 데이터는 id, 계약여부를 의미한다. extension은 해당 공장설비의 증여를 의미한다.
    - delivery는 납품으로 계약 id, 품목, 수량을 담는다.
    - 하루 지난 날자와 납품 실패 수가 반환된다.

### get score
    - 지정된 일자가 모두 지난 이후에만 제대로 된 점수가 출력되며, 그 전에는 0점이 출력된다.
    - 점수 산출방식은 다음과 같다.
    - 기본 점수 2000점.
    - 

### 이런 문제는 어떨까?
    - 편의점 물품 배치하기.
    - 한정된 진열대에 손님들이 와서 물건을 사 간다.
    - 알바는 N명, 손님 최대 수용량은 M명. N<M.
    - 손님 계산시 알바가 계산대에 없으면 시간 지연.
    - 계산은 한 턴에 가능. 고르기는 재고가 없으면 지연.
    - 각 알바의 행동은 재고 채우기, 계산대, 손님응대가 있다.
    - 손님응대는 없는 재고 채우기이다.
    - 손님 수용이 M명일 경우 편의점 들어오려던 손님이 그냥 지나쳐간다.
    - 최대한 많은 손님을 받는게 목표.