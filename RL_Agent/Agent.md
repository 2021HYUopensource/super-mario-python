```
from PPO.PPO_main_sys import create_ppo_main_sys
```



## create_ppo_main_sys

### args

env : 환경 오브젝트

state_shape : state shape

action_size : action space 크기

verbose : 로그 출력 여부(bool)

param : 하이퍼 파라미터(dict)

기본 하이퍼 파라미터

```
param = {
    "learning_rate": 0.001,
    "loss_clipping": 0.2,
    "entropy_loss": 0.001,
    "epoch": 10,
    "gamma": 0.99,
    "lmbda": 0.95,
    "batch_size": 1000
}
```

### return

(object) ppo_main_sys



## ppo_main_sys.train()

모델을 학습함. 지정 횟수 만큼 학습하며 로그를 텐서보드에 기록함

### args

(int) epi : 학습할 에피소드 수

 (bool) load_model : 가중치를 불러와서 학습할지 여부



### return

None



## ppo_main_sys.test()

모델을 테스트함. 지정 횟수만큼 테스트 진행 후 평균 점수 출력

### args

(int) epi : 테스트 횟수

 (bool) load_model : 가중치를 불러와서 테스트



### return

None

