# 개요
- 코딩테스트를 보고 영감을 얻어서 만들어보는 프로젝트.
- API로 응시자는 서버와 소통한다.
- 여기서는 그 API 서버 부분을 작성해보고자 한다.
# 문제
- 편의점 물품 배치하기.
- 한정된 진열대에 손님들이 와서 물건을 사 간다.
- 알바는 N명, 손님 최대 수용량은 M명. N<M.
- 손님 계산시 알바가 계산대에 없으면 시간 지연.
- 계산은 한 턴에 가능. 고르기는 재고가 없으면 지연.
- 알바의 행동은 재고채우기, 고객응대-계산하기가 있다.
- 손님 수용이 M명일 경우 편의점 들어오려던 손님이 그냥 지나쳐간다.
- 최대한 많은 손님을 받아 많은 숫자의 품목을 파는 것이 목표.
- 고객응대시 품목이 충분히 진열되어 있지 않다면 실패하며, 손님은 그냥 나간다.

## API
### strat test
    - /start_test/으로 post.
    - {"address" : "YOUREMAIL"} 데이터 전달.
    - {"key" : "YOURKEY"}가 리턴.
    - 해쉬 기반으로 키를 생성해서 email별로 유니크하게 만들었다.

### start problem
    - /start_test/problems으로 post.
    - data : {"key" : "YOURKEY", "problem" : 1}
    - return : {"key" : "problemkey",
                "max_time" : 120,
                "part_timer" : 5,
                "items": ["cookie", ...]
                "customer_capacity" : 10,
                "max_item" : 5}
    - 각각 영업시간, 알바생 수, 품목, 최대고객수, 품목당 최대진열.

### customer
    - /customer/로 get.
    - header : {"key" : "problemkey"}
    - return : {"customers" : [{"id" : 13313, 
                    "needs":[{"item":"cookie", "num":3},...]},...]}
    -각각 손님id, 원하는것-품목, 수량을 의미한다.

### customer/action
    - /customer/action/으로 post.
    - header : {"key" : "problemkey"}
    - data : {"accepted" : [14233,...]
              "rejected" : []
              "data" : [{"id":1, "type" : "serve" / "display",
                      "target": customerid / "ITEM NAME"},...]
    - accepted에 있는 모든 고객들은 매장에서 '대기'상태가 된다. 최대 15분 대기한다.
    - rejected에 있는 모든 고객은 매장에서 즉시 나간다.
    - 각각 알바id(1부터 순차적으로 존재.), 행동타입(고객응대/재고채우기)
        대상(고객id/재고명)을 의미한다.
    -유효하지 않은 행동은 무시된다.
    - return : {"serve failed" : 0, "time" : 1}
    - 각각 고객응대실패숫자와 시간(1분 뒤)를 의미한다.

### score
    - /score/으로 get.
    - header : {"key" : "problemkey"}
    - 매장 개장시간이 끝났다면 점수를 return한다. 아니라면 0점이다.
    - 점수는 다음과 같다.
    - 기본점수 - 500
    - 판매점수 - 총판매수량/(모든고객의 주문수량합) * 200
    - 만족점수 - 고객대기시간/(매장수용고객량 * 15) * 50
    - 페널티점수 - 거절당한 고객수/(총고객수)*50 + 잘못응대한고객수/총고객수 *500
    - 최종점수 - 기본점수+판매점수+만족점수 - 페널티점수.
    

--------------------

## 이런 문제는 어떨까?
## Factory_managing_problem
- 당신은 상상공장의 매니저이다.
- 같은 카테고리의 제품은 동일 라인을 이용해서 생산 가능하다.
- 계약의 수주와 제품 생산, 거래를 통해서 이익을 최대한 남겨야 한다.
- 제품 정보, 계약 정보는 아래에 따로 기술할 예정.
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