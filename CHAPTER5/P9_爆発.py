#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.爆発クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classCrush:
    #┬
    #□開始時の半径
    #□終了時の半径
    START_RADIUS    = 1
    END_RADIUS      = 8
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：Ｘ座標
    #┃　　　　　③ 整数型：Ｙ座標
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self,
        atgGame,    #① 生成先のオブジェクト
        argX,       #② Ｘ座標
        argY        #③ Ｙ座標
        ):
		#┬
        #○引数を退避する
        self.objGame    = atgGame
        self.X          = argX
        self.Y          = argY
        #│
        #○基本データ(半径)を初期化する
        self.Radius     = classCrush.START_RADIUS
        #│
        #○BGMを止める
        #○爆発音を鳴らす
        pyxel.stop()
        pyxel.play(2, 63, resume=True)
        #│
        #〇爆発を生成(リスト追加)する
        self.objGame.objCrush.append(self)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        if pyxel.frame_count % 2 != 0: return
        #○半径を大きくする
        self.Radius += 1
        if self.Radius > classCrush.END_RADIUS:
        #　 ＼（半径が最大になった場合）
            #○爆発を抹消(リストから除外)する
            self.objGame.objCrush.remove(self)
            pyxel.playm(7, loop=True)
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○爆発を描画する
        pyxel.circ (self.X, self.Y, self.Radius,  7)
        pyxel.circb(self.X, self.Y, self.Radius, 10)
        #┴