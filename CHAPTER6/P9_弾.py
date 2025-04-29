#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅴ.弾クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classBullet:
    #┬
    #□所有者(自機)
    #□所有者(敵機)
    OWNER_PLAYER = 0
    OWNER_ENEMY  = 1 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：所有者
    #┃　　　　　③ 整数型：Ｘ座標
    #┃　　　　　④ 整数型：Ｙ座標
    #┃　　　　　⑤ 小数型：発射角度
    #┃　　　　　⑥ 整数型：移動速度
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self,
        argGame,    #① 生成先のオブジェクト
        argOwner,   #② 所有者
        argX,       #③ Ｘ座標
        argY,       #④ Ｙ座標
        argAngle,   #⑤ 発射角度
        argSpeed    #⑥ 移動速度
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame
        self.Owner      = argOwner
        self.X          = argX
        self.Y          = argY
        #│
        #○└┐基本データを初期化する
            #○Ｘ軸のベクトル
            #○Ｙ軸のベクトル
        self.VectorX    = pyxel.cos(argAngle) * argSpeed
        self.VectorY    = pyxel.sin(argAngle) * argSpeed
            #┴
        #│
        #◇┐弾を増やす
        if self.Owner == classBullet.OWNER_PLAYER:
        #　├→（弾の所有者が『自機』の場合）
            #○当たり判定の領域をセットする
            #〇弾(自機)を生成(リスト追加)する
            self.HitArea = (2, 1, 5, 6)
            self.objGame.objBullet_Player.append(self)
            #┴
        #│
        else:
        #　└┐（その他）
            #○当たり判定の領域をセットする
            #〇弾(敵機)を生成(リスト追加)する
            self.HitArea = (2, 2, 5, 5)
            self.objGame.objBullet_Enemy.append(self)
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○座標を更新する
        self.X += self.VectorX
        self.Y += self.VectorY
        #│
        #◇┐弾を消す
        if (
            self.X <= -8 or self.X >= pyxel.width   or
            self.Y <= -8 or self.Y >= pyxel.height
        ):
        #　├→（座標が画面表示外の場合）
            #◇┐弾を消す
            if self.Owner == classBullet.OWNER_PLAYER:
            #　├→（所有者が『自機』の場合）
                #○弾(自機)リストから抹消する
                self.objGame.objBullet_Player.remove(self)
                #┴
            #│
            else:
            #　└┐（その他）
                #○弾(敵機)リストから抹消する
                self.objGame.objBullet_Enemy.remove(self)
        #┴　┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．命中を処理する
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Sub_Collision(self):
		#┬
        #◇┐弾を消す
        if self.Owner == classBullet.OWNER_PLAYER:
        #　├→（所有者が『自機』の場合）
            #◇┐弾(自機)リストから魔性する
            if self in self.objGame.objBullet_Player:
            #　├→（弾(自機)リストに存在する場合）
                #○弾(自機)を抹消(リストから除外)する
                self.objGame.objBullet_Player.remove(self)
                #┴
            #　└┐（その他）
            #┴　┴
        #　│
        elif self in self.objGame.objBullet_Enemy:
        #　├→（弾(敵機)リストに存在する時場合）
            #○弾(敵機)を抹消(リストから除外)する
            self.objGame.objBullet_Enemy.remove(self)
            #┴
        #　└┐（その他）
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃３．描画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○弾を描画する
        tmpSrcX = 0 if self.Owner == classBullet.OWNER_PLAYER else 8
        pyxel.blt(self.X, self.Y, 0, tmpSrcX, 8, 8, 8, 0)
        #┴
