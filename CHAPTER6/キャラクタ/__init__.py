#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER6:MAGA WING
#┃キャラクター・モジュール
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from .自機      import class自機
from .標的      import class標的    , class種類ID as 敵機ID

from .アイテム  import classアイテム
from .アイテム  import class種類ID  as アイテムID
from .アイテム  import class仕様    as アイテム仕様

from .弾        import class弾
from .爆発      import class爆発