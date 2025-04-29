#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
from P9_弾      import classBullet
from P9_爆発    import classCrush

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.自機クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classPlayer:
    #┬
    #□移動速度
    #□弾の発射間隔
    MOVE_SPEED      = 2
    SHOT_INTERVAL   = 6 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：Ｘ座標
    #┃　　　　　③ 整数型：Ｙ座標
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self,   
        argGame,    #① 生成先のオブジェクト
        argX,       #② Ｘ座標
        argY        #③ Ｙ座標
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame
        self.X          = argX
        self.Y          = argY
        #│
        #○└┐基本データを初期化する
            #○当たり判定の領域を初期化する
            #○弾発射までの残り時間を初期化する
        self.HitArea    = (1, 1, 6, 6)
        self.TimeShot   = 0
            #┴
        #│
        #〇自機を生成する
        self.objGame.objPlayer  = self
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #◇┐キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT )   : self.X -= classPlayer.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT)   : self.X += classPlayer.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_UP   )   : self.Y -= classPlayer.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN )   : self.Y += classPlayer.MOVE_SPEED
        #│
        #◇┐ＭＭＰコントローラで自機を移動させる
        #if MMP_X < ARROW_MMP_LEFT   : self.X -= classPlayer.MOVE_SPEED
        #if MMP_X > ARROW_MMP_RIGHT  : self.X += classPlayer.MOVE_SPEED
        #if MMP_Y < ARROW_MMP_UP     : self.Y -= classPlayer.MOVE_SPEED
        #if MMP_Y < ARROW_MMP_DOWN   : self.Y += classPlayer.MOVE_SPEED
        #│
        #〇自機を移動する
        self.X = max(self.X, 0                  )
        self.X = min(self.X, pyxel.width  - 8   )
        self.Y = max(self.Y, 0                  )
        self.Y = min(self.Y, pyxel.height - 8   )
        #│
        #◇┐弾の発射間隔を制限する
        if self.TimeShot > 0:
        #　├→（）
            #○発射可能までの時間を減らす
            self.TimeShot -= 1
            #┴
        #│
        #◇┐弾を発射する
        if pyxel.btn(pyxel.KEY_SPACE) and self.TimeShot == 0:
        #　├→（発射可能で、スペースキーを押した場合）
            #○弾を生成する
            classBullet(
                self.objGame,
                classBullet.OWNER_PLAYER,
                self.X, self.Y - 3,
                -90,
                5
                )
            #│
            #○弾発射音を鳴らす
            pyxel.play(3, 0)
            #│
            #○発射可能までの時間をリセットする
            self.TimeShot = classPlayer.SHOT_INTERVAL
            #┴
        #　└┐（その他）
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．被弾・衝突を処理する
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Sub_Collision(self):
		#┬
        #●爆発を生成する
        classCrush(self.objGame, self.X + 4, self.Y + 4)
        #│
        #○BGMを止める
        #○爆発音を鳴らす
        pyxel.stop()
        pyxel.play(0, 2)
        #│
        #○自機を抹消する
        self.objGame.objPlayer = None
        #│
        #●ゲームオーバー画面を表示する
        self.objGame.Sub_Scene(self.objGame.SCENE_GAMEOVER)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃３．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○自機を描画する
        pyxel.blt(self.X, self.Y, 0, 0, 0, 8, 8, 0)
        #┴
