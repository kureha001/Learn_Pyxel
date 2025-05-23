#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃キャラクタ：自機：描画機能
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
import main.DB
from   特殊効果 import 効果ID

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃仕様
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class 仕様クラス:
    def __init__(self   ,
            引数_仕様   ):  #① 所有者を識別するID
        #--------------------------------------------------------------------
        # イメージバング
        #--------------------------------------------------------------------
        #□ 画像     ：イメージバンクの切り出し条件
        x =  引数_仕様.番号 * 8
        self.画像 = (0, x,0, 8,8, 0)

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃メイン
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class 描画クラス:
    #┌───────────────────────────────────
    #│初期化
    #└───────────────────────────────────
    def __init__(self   ,
            引数_個体   ): #① 個体オブジェクト
        #┬
        #〇個体オブジェクトのリファレンスを用意する
        self._仕様  = 引数_個体.仕様
        self._情報  = 引数_個体.情報
        #│
        #○外部オブジェクトのリファレンスを用意する
        self.特情   = main.DB.obj特殊効果.情報
        #│
        #≫データセットを用意する
        self.仕様   = 仕様クラス(self._仕様)
        self.情報   = None
        #┴

    #┌───────────────────────────────────
    #│機能実行
    #└───────────────────────────────────
    def 実行(self):
        #┬
        #●バリヤーを描画する
        self.Fnバリヤー()
        #│
        #○画像情報に基づき描画する
        pyxel.blt(self._情報.X, self._情報.Y, *self.仕様.画像)
        #┴
	#────────────────────────────────────	
    def Fnバリヤー(self):
        #┬
        #●特殊効果から、ダメージ倍率を求める
        発動状況 = self.特情.発動中
        キー   = 効果ID.防御
        ダメージ倍率 = (発動状況[キー][1]) if キー in 発動状況 else (1)
        #│
        #◇┐機体の画像情報を求める
        if   ダメージ倍率 >= 1:
        #　├┐（ダメージ倍率が『標準』の場合）
            #↓
            #○バリアーなし
            return
            #┴
        elif ダメージ倍率 == 0  : x = 2
        #　├┐（ダメージ倍率が『無敵』の場合）
            #↓
            #○仕様の画像情報を『無敵用』の座標に変更する
            #┴
        elif ダメージ倍率 < 0   : x = 3
        #　├┐（ダメージ倍率が『吸収』の場合）
            #↓
            #○仕様の画像情報を『吸収用』の座標に変更する
            #┴
        else                    : x = 1
        #　└┐（その他）
            #↓
            #○仕様の画像情報を『半減用』の座標に変更する
            #┴
        #│
        #○バリヤーを描画する
        画像 = (0, (x * 16),0, 16,16, 0)
        x    = self._情報.X - 4
        y    = self._情報.Y - 4
        pyxel.blt(x, y, *画像)
        #┴