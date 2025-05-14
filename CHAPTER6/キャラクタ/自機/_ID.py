#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃キャラクタ：自機：ID
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from    enum import IntEnum, auto

class 効果ID(IntEnum):

    追加速度     = 1
    連射         = auto()
    防御UP       = auto()
    貫通弾       = auto()
    発射数       = auto()
    発射方向     = auto()