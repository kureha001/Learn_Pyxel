#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃キャラクタ：アイテム：ID
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from    enum import IntEnum, auto

class ID(IntEnum):
    #┬
    #□└┐機体
    速度UP	        = 0
    弾薬回復	    = auto()
    シールド回復	= auto()
    ダメージ無し	= auto()
    ダメージ半分	= auto()
    ダメージ吸収    = auto()
    発射_連射   	= auto()
    発射_弾数UP   	= auto()
    発射_貫通弾	    = auto()
    発射_上下方向   = auto()
    発射_左右方向   = auto()
    発射_4方向   	= auto()
    発射_8方向   	= auto()
    #┴
