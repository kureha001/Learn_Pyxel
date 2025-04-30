#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER5
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.定数
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┬
#□└┐シーン
	#□タイトル画面
	#□プレイ画面
	#□ゲームオーバー画面
SCENE_TITLE     = 0
SCENE_PLAY      = 1 
SCENE_GAMEOVER  = 2
#┴　┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃ジェット噴射(ON/OFF)の判定
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def Fun_FireOn():
	#┬
	#◇┐キーの状態に合わせて、プレイヤーの速度を更新する
	if pyxel.btn(pyxel.KEY_SPACE)				: return True
	elif pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)		: return True
	#　├→（スペースキーかＡボタンが押された場合）
		#○『はい』を返す
		#┴
	#　└┐（その他）
	else 										: return False
		#○『いいえ』を返す
	#┴　┴

def Fun_FireOff():
	#┬
	#◇┐キーの状態に合わせて、プレイヤーの速度を更新する
	if pyxel.btnr(pyxel.KEY_SPACE)				: return True
	elif pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)	: return True
	#　├→（スペースキーかＡボタンが押された場合）
		#○『はい』を返す
		#┴
	#　└┐（その他）
	else 										: return False
		#○『いいえ』を返す
	#┴　┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃プレイヤーから一定距離離れた位置を得る 
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃【引き数】最低の離す距離
#┃【戻り値】リスト(X座標,Y座標)
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def Fun_Position(argDist, argX, argY):
	#┬
	#◎└┐座標が決まるまで繰り返す
	while True:
		#○ランダムに座標を求める
		x = pyxel.rndi(0, pyxel.width  - 8)
		y = pyxel.rndi(0, pyxel.height - 8)
		#│
		#○プレイヤーとの差を求める
		diff_x = x - argX
		diff_y = y - argY
		#│
		#◇┐プレイヤーとの差によって、座標を確定する
		if diff_x**2 + diff_y**2 > argDist**2:
		#　├→（指定の距離以上に離れている場合）
			#▼座標を返す
			return (x, y)
			#┴
		#　└┐（その他）
	#┴　┴　┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃衝突の有無を得る
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃【引き数】① OBJ型 ：対象物（1つ目）
#┃　　　　　② OBJ型 ：対象物（2つ目）
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃【戻り値】① 論理型：衝突あり：True／衝突なし：False
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def Fun_Collision(
    argObj1,    #① 対象物１
    argObj2     #② 対象物２
    ):
    #┬
    #○対象物１の座標範囲を求める
    tmpObj1_X1 = argObj1.X + argObj1.HitArea[0]
    tmpObj1_Y1 = argObj1.Y + argObj1.HitArea[1]
    tmpObj1_X2 = argObj1.X + argObj1.HitArea[2]
    tmpObj1_Y2 = argObj1.Y + argObj1.HitArea[3]
    #│
    #○対象物２の座標範囲を求める
    tmpObj2_x1 = argObj2.X + argObj2.HitArea[0]
    tmpObj2_y1 = argObj2.Y + argObj2.HitArea[1]
    tmpObj2_x2 = argObj2.X + argObj2.HitArea[2]
    tmpObj2_y2 = argObj2.Y + argObj2.HitArea[3]
    #│
    #◇┐衝突の有無を返す
    if (
        tmpObj1_X1 > tmpObj2_x2 or
        tmpObj1_X2 < tmpObj2_x1 or
        tmpObj1_Y1 > tmpObj2_y2 or
        tmpObj1_Y2 < tmpObj2_y1
    ):
    #　├→（座標範囲が重なっていない場合）
        #▼『衝突なし』を返す
        return False
    #　│
    #　└┐（その他）
    else:
        #▼『衝突あり』を返す
        return True
    #┴　┴