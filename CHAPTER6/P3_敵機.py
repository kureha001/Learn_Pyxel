#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
from P9_弾      import classBullet
from P9_爆発    import classCrush

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.敵機クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classEnemy:
    #┬
    #□機種Ａ
    #□機種Ｂ
    #□機種Ｃ
    TYPE_A = 0
    TYPE_B = 1
    TYPE_C = 2
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：機種
    #┃　　　　　③ 整数型：難易度
    #┃　　　　　④ 整数型：Ｘ座標
    #┃　　　　　⑤ 整数型：Ｙ座標
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self,
        argGame,    #① 生成先のオブジェクト
        argType,    #② 機種
        argLevel,   #③ 難易度
        argX,       #④ Ｘ座標
        argY        #⑤ Ｙ座標
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame
        self.Type       = argType
        self.Level      = argLevel
        self.X          = argX
        self.Y          = argY
        #│
        #○└┐基本データを初期化する
            #○当たり判定の領域を初期化する
            #○防御力を初期化する
            #○生存時間を初期化する
            #○衝突有無を初期化する
        self.HitArea    = (0, 0, 7, 7)
        self.Armor      = self.Level - 1
        self.TimeLife   = 0
        self.Collided   = False
        #│
        #〇敵機を生成(リスト追加)する
        self.objGame.objEnemie.append(self)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○生存時間をカウントする
        self.TimeLife += 1
        #│
        #◇┐敵機を更新する
        if self.Type == classEnemy.TYPE_A:
        #　├→（機種が『Ａ』の場合）
            #○前方に移動させる
            self.Y += 1.2
            #│
            #◇┐弾を発射する
            if self.TimeLife % 50 == 0:
            #　├→（生存時間が50カウントの場合）
                #●自機の角度を求める
                #●弾を発射する
                tmpAngle = self.Fun_Angle()
                classBullet(
                    self.objGame,
                    classBullet.OWNER_ENEMY,
                    self.X, self.Y,
                    tmpAngle,
                    2
                    )
                #┴
            #　└┐（その他）
            #┴　┴
        #　│
        elif self.Type == classEnemy.TYPE_B:
        #　├→（機種が『Ｂ』の場合）
            #○前方に移動する
            self.Y += 1
            #│
            #◇┐左右に移動する
            if self.TimeLife // 30 % 2 == 0:
            #　├→（生存時間が30カウントの場合）
                #│
                #○右に移動する
                self.X += 1.2
                #┴
            #　│
            else:
            #　└┐（その他）
                #○左に移動する
                self.X -= 1.2
            #┴　┴
        #　│
        elif self.Type == classEnemy.TYPE_C:
        #　├→（機種が『Ｃ』の場合）
            #○前方に移動する
            self.Y += 0.8
            #│
            #◇┐弾を発射する
            if self.TimeLife % 40 == 0:
            #　├→（生存時間が40カウントの場合）
                #◎└┐４方向に発射する
                for tmpCnt in range(4):
                    #│＼（4方向の処理を終えた場合）
                    #│ ▼繰り返し処理を抜ける
                    #○当該の方向に弾を発射する
                    classBullet(
                        self.objGame,
                        classBullet.OWNER_ENEMY,
                        self.X, self.Y,
                        tmpCnt * 45 + 22,
                        2
                        )
                #┴　┴
            #　└┐（その他）
            #┴　┴
        #│
        #◇┐敵機を消する
        if self.Y >= pyxel.height:
        #　├→（画面下から出た場合）
            #◇┐敵機を消す
            if self in self.objGame.objEnemie:
            #　├→（敵が存在する場合）
                #○敵機リストから抹消する
                self.objGame.objEnemie.remove(self) 
                #┴
            #　└┐（その他）
            #┴　┴
        #　└┐（その他）
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃1-1.発射角を得る
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【戻り値】① 小数型：角度
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Fun_Angle(self):
		#┬
        #○自機を参照する
        tmpObj = self.objGame.objPlayer
        #│
        #◇┐角度を求める
        if tmpObj is None: 
        #　├→（自機が存在しない場合）
            #▼90度を返す
            return 90
        #　│
        else:
		#　└┐（その他）
            #▼自機の方角を返す
            return pyxel.atan2(tmpObj.Y - self.Y, tmpObj.X - self.X)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．被弾を処理する
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Sub_Collision(self):
		#┬
        #◇┐
        if self.Armor > 0:
        #　├→（防御力が残っている場合）
            #○防御力を減らす
            #○ダメージ有無を『あり』にする
            #○被弾音を鳴らす
            self.Armor      -= 1
            self.Collided = True
            pyxel.play(2, 1, resume=True)
            #┴
        #　│
        else:
        #　└┐（その他）
            #●爆発エフェクトを生成する
            #○爆発音を鳴らす
            #○スコアを加算する
            classCrush(self.objGame, self.X + 4, self.Y + 4)
            pyxel.play(2, 2, resume=True) 
            self.objGame.Score += self.Level * 10
            #│
            #◇┐敵機を消す
            if self in self.objGame.objEnemie:
            #　├→（敵機リストに存在する場合）
                #○敵機を抹消(リストから除外)する
                self.objGame.objEnemie.remove(self)
                #┴
            #　└┐（その他）
        #┴　┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃３．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○敵機を描画する
        pyxel.blt(
            self.X, self.Y,
            0, self.Type * 8 + 8, 0,
            8, 8,
            0
            )
        #┴