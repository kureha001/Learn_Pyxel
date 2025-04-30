#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.背景クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classScreen:
    #┬
    #□星の数
    NUM_STARS = 50
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self,
        argGame     #① 生成先のオブジェクト
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame   # ゲームへの参照
        #│
        #○基本データを初期化する
        self.Star       = []        # 星リスト
        #│
        #◎└┐すべての星を追加する
        for cnt in range(classScreen.NUM_STARS):
            #│＼（すべての星を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #○└┐座標と速度を求める
                #○X座標をランダムに求める
                #○Y座標をランダムに求める
                #○縦方向の速度をセットする
            tmpX  = pyxel.rndi(0, pyxel.width  - 1 )  
            tmpY  = pyxel.rndi(0, pyxel.height - 1 )  
            tmpVY = pyxel.rndf(1, 2.5              ) 
                #┴
            #│
            #○星を追加する
            self.Star.append((tmpX, tmpY, tmpVY))
            #┴
        #│
        #〇地平線を描画する
        #〇背景を生成する
        self.objGame.objScreen = self
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #◎└┐すべての星を更新する
        for tmpID, (tmpX, tmpY, tmpVY) in enumerate(self.Star):
			#│＼（すべての星を処理し終えた場合）
			#│ ▼繰り返し処理を抜ける
            #│
            #○座標を画面下方向に移動する
            tmpY += tmpVY
            if tmpY >= pyxel.height:
            #│＼（画面下に達した場合）
                #○座標を画面上に移動する
                tmpY -= pyxel.height
                #┴
            #│
            #○座標を更新する
            self.Star[tmpID] = (tmpX, tmpY, tmpVY)
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
		#●地表を描画する
		#●星を描画する
        self.draw_ground()
        self.draw_star()
        #┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃地表を描画
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw_ground(self):
		#┬
		#○空を描画する条件をセットする
        num_grads	= 4		# グラデーションの数
        grad_height	= 6		# グラデーションの高さ
        grad_start_y = pyxel.height - grad_height * num_grads  # 描画開始位置
		#│
		#◎└┐グラデーションの数だけ、背景を描画する
        for i in range(num_grads):
			#│＼（最後のラデーションの数を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#○ディザリングを有効にする
            pyxel.dither((i + 1) / num_grads)
			#│
			#○四角形を描画する
            pyxel.rect(
                0,
                grad_start_y + i * grad_height,
                pyxel.width,
                grad_height,
                1,
                )
			#┴
		#│
		#○ディザリングを無効にする
        pyxel.dither(1)
		#┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃星を描画
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw_star(self):
        #◎└┐すべての星を描画する
        for tmpX, tmpY, tmpSpeed in self.Star:
			#│＼（）
			#│ ▼繰り返し処理を抜ける
			#│
            #○速度に応じて色を変える
            #○星を表示する
            tmpColor = 12 if tmpSpeed > 1.8 else 5
            pyxel.pset(tmpX, tmpY, tmpColor)
        #┴　┴
