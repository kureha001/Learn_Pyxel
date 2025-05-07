#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER6:MAGA WING
#┃処理モジュール
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from ._定数         import class所有者ID, class効果ID, class効果
from .ゲーム        import classGame
from .更新1_移動    import class移動処理
from .更新2_除外    import class除外処理
from .更新3_発射    import class発射処理
from .更新4_衝突    import class衝突処理
from .更新5_出現    import class出現処理