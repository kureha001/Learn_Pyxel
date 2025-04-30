#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER5
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
import time
from P1_背景    import classScreen

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.定数
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┬
#□ゲームタイトル
GAME_TITLE		  = "bigban"
#│
#□└┐宇宙船の移動
	#□左右方向の加速度
	#□上方向(上昇)の加速度
	#□下方向(落下)の加速度
	#□最大速度
	#┴
SHIP_ACCEL_X 		= 0.06
SHIP_ACCEL_UP 		= 0.04
SHIP_ACCEL_DOWN 	= 0.02
MAX_SHIP_SPEED		= 0.8
#│
#□└┐出現カウント(30で１秒)
	#□ボスキャラ用
	#□敵子分用
	#┴
INTERVAL_SURVIVOR	= 210
INTERVAL_METEOR		= 210
#┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅲ．クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Game:
    #┬
    #□タイトル画面
    #□プレイ画面
    #□ゲームオーバー画面
	SCENE_TITLE     = 0
	SCENE_PLAY      = 1 
	SCENE_GAMEOVER  = 2
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化 ※1度だけ実行
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def __init__(self):
		#┬
		#○Pyxelを初期化する
		pyxel.init(300, 200, title = GAME_TITLE)
		#│
		#○リソースファイルを読み込む
		#pyxel.load("res-org.pyxres")		# 最初のリソース
		pyxel.load("res-kureha.pyxres")		# 呉羽のリソース
		#pyxel.load("res-sumin.pyxres")		# スー民のリソース
		#│
		#●BGMを初期化する
		self.init_music()
		#│
		#○シーンを『タイトル』にセットする
		self.Scene = self.SCENE_TITLE
		#│
		#●背景を生成する
		self.objScreen	= None
		classScreen(self)
		#│
		#●ゲームをリセットする
		self.reset_game()
		#│
		#○アプリの実行を開始する
		pyxel.run(self.update, self.draw)
		#┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．アプリを更新 ※1秒に30回実行
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update(self):
		#┬
        #●背景を更新する
		self.objScreen.update()
		#│
		#◇┐シーンに合わせて、ゲームの流れを変える
		if self.Scene == self.SCENE_GAMEOVER:
		#　├→（シーンが『ゲームオーバー』の場合）
			#▼関数の処理をここでやめる
			return
		#│
		elif self.Scene == self.SCENE_TITLE:
		#　├→（シーンが『タイトル』の場合）
			#◇┐エンターキーが押されている場合：
			if self.Fn_JetON():
			#　├→（ジェット噴射の指示が『ある』場合）
				#○タイトル表示モードを『プレイ』にする
				self.Scene = self.SCENE_PLAY
				#│
				#●ゲームをリセットする
				self.reset_game()
				#┴
			#▼関数の処理をここでやめる
			return
		#　└┐（その他）※なにもしない
			#┴
		#│
		#○┐ゲームを更新する
		#　●宇宙船を更新する
		self.update_ship()
		#　│
		#　●オブジェクトを追加する（敵子分）
		self.add_henchman()
		#　│
		#　●オブジェクトを追加する（ボスキャラ）
		self.add_boss()
		#　│
		#　●接触判定（敵子分）
		self.check_henchman()
		#　│
		#　●接触判定（ボスキャラ）
		self.check_boss()
		#　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．アプリを描画 ※1秒に30回実行
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw(self):
		#┬
		#●空を描画する
		self.draw_sky()
		#│
        #●背景を描画する
		self.objScreen.draw()
		#│
		#●宇宙船を描画する
		self.draw_ship()
		#│
		#●敵子分を描画する
		self.draw_henchman()
		#│
		#●ボスキャラを描画する
		self.draw_boss()
		#│
		#●スコアを描画する
		self.draw_score()
		#│
		#◇┐シーンに合わせて、処理を制御する
		if self.Scene == self.SCENE_TITLE:
		#　├→（シーンが『タイトル』の場合）
			#●タイトルを描画する
			self.draw_title()
			#┴
		#│
		elif self.Scene == self.SCENE_GAMEOVER:
		#　├→（シーンが『ゲームオーバー』の場合）
			#◇┐爆破音を鳴らす
			if self.timer_GameOver == 0:
			#　├→（ゲームオーバー直後の場合）
				#○爆破音を鳴らす
				pyxel.stop()
				pyxel.play(2, 63, resume=True)
				#┴
			#│
			#◇┐ゲームオーバーのシーンを終了する
			if self.timer_GameOver > 30:
			#　├→（ゲームオーバーが終了する時間の場合）
				#○ＢＧＭを鳴らす
				#○シーンを『タイトル画面』にセットする
				pyxel.playm(7, loop=True)
				self.Scene = self.SCENE_TITLE
			#│
			#〇ゲームオーバーの経過時間を増やす
			self.timer_GameOver += 1
			#┴
		#　└┐（その他）※なにもしない
		#┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃『０．初期化する』『１．アプリを更新する』のサブ関数
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃BGMを初期化する（ゲームオーバー）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def init_music(self):
		#┬
		#○Soundデータを登録する
		pyxel.sounds[60].mml(
			"t100 @1 o2 q7 v7 l4" +
			"l8d4a4g2.fed4c<b->c<a>e4d1.a4>" +
			"c4<b2.gfe4fga1&a1d4a4g2.fed4c<b->c<a>e4d1."
			)
		pyxel.sounds[61].mml(
			"t100 @0 o1 q7 v4 l2" +
			"l8dafadbgbd>c<a>c<db-fb-e>c<a>c" +
			"<daf+adaf+agb-a>c" +
			"<dafadbgbdbgbdb-g+b-c" +
			"+aeadaeac+aea<b>ac+adafadbgbd>c" +
			"<a>c<db-fb-e>c<a>c<daf+adaf+adaf+a"
			)
		#│
		#○Musicデータを登録する
		pyxel.musics[7].set([60],[61])
		#┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃【共通関数】ゲームをリセット
		#┃【利用箇所】0-4／1-1.1.2
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def reset_game(self):
		#┬
		#□得点（初期値：ゼロ）
		self.score 			= 0
		#│
		#□└┐タイマー（初期値：ゼロ）
			#□敵子分の出現
			#□ボスキャラの出現
			#□ゲームオーバーの経過
			#┴
		self.timer_henchman	= 0
		self.timer_boss	= 0
		self.timer_GameOver	= 0
		#│
		#□└┐宇宙船の位置
			#□X座標（初期値：画面の2分の1から8ドット左）
			#□Y座標（初期値：画面の4分の1）
			#┴
		self.ship_x 		= (pyxel.width - 8) / 2
		self.ship_y 		= pyxel.height      / 4
		#│
		#□└┐宇宙船の速度（初期値：ゼロ）
			#□X方向
			#□Y方向
			#┴
		self.ship_vx 		= 0
		self.ship_vy 		= 0
		#│
		#□宇宙船の向き（初期値：右）[右=1｜左=2]
		self.ship_dir 		= 1 
		#│
		#□宇宙船の噴射状態（初期値：あり）[あり=True｜なし=Fals]
		self.is_jetting 	= False
		#│
		#□└┐オブジェクトのリスト（初期値：空）
			#□敵子分用
			#□ボスキャラ用
			#┴
		self.henchman	= []
		self.boss		= []

		#◇┐
		pyxel.stop()
		if self.Scene == self.SCENE_TITLE:
		#　├→（）
			#○BGMを鳴らす ※繰り返し鳴らす
			pyxel.playm(0, loop=True)
			#┴
		#│
		elif self.Scene == self.SCENE_PLAY:
		#　├→（）
			#○BGMを鳴らす ※繰り返し鳴らす
			pyxel.playm(1, loop=True)
		#　└┐（その他）
		#┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃『１．アプリを更新する』のサブ関数
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃宇宙船を更新
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update_ship(self):
		#┬
		#◇┐キーの状態に合わせて、宇宙船の速度を更新する
		if self.Fn_JetON():
		#　├→（ジェット噴射の指示が『ある』場合）
			#○噴射状態を「噴射あり」にする
			self.is_jetting	= True
			#│
			#○加速する(縦) ※速度制限する
			self.ship_vy 	= max(self.ship_vy - SHIP_ACCEL_UP, -MAX_SHIP_SPEED)
			#│
			#○加速する(横) ※速度制限する
			self.ship_vx 	= max(
				min(self.ship_vx + self.ship_dir * SHIP_ACCEL_X, 1), -MAX_SHIP_SPEED
			)
			#│
			#○ジェット音を鳴らす
			pyxel.play(0, 0, resume=True)
			#┴
		else:
		#　└┐（その他）
			#○噴射状態を「噴射なし」にする
			self.is_jetting	= False
			#│
			#○減速する(縦)
			self.ship_vy = min(self.ship_vy + SHIP_ACCEL_DOWN, MAX_SHIP_SPEED)
			#┴
		#│
		#◇┐キーの状態に合わせて、次に進む方向を変える
		if self.Fn_JetOFF():
		#　├→（ジェット噴射の指示が『ない』場合）
			#○次に進む方向を反転する
			self.ship_dir = -self.ship_dir
			#┴
		#　└┐（その他）※なにもしない
			#┴
		#│
		#○└┐宇宙船を移動する
			#○X座標を変更する ※ベクトル量を加える
			#○Y座標を変更する ※ベクトル量を加える
		self.ship_x += self.ship_vx
		self.ship_y += self.ship_vy
			#┴
		#│
		#○└┐画面の終端位置を求める
			#○右端の位置(右端の８ドット手前)を求める
			#○下端の位置(下端の８ドット手前)求める
			#┴
		max_ship_x = pyxel.width	- 8
		max_ship_y = pyxel.height	- 8 

		#◇┐宇宙船の座標に合わせて、跳ね返す
		if self.ship_x < 0:
		#　├→（宇宙船の『X座標が左端』をはみ出した場合）
			#○X座標を一番左に戻す
			self.ship_x		= 0
			#│
			#○移動方向を右に変える ※速度はそのまま
			self.ship_vx	= abs(self.ship_vx)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1, resume=True)
			#┴
		#　│
		elif self.ship_x > max_ship_x:
		#　├→（宇宙船の『X座標が右端』をはみ出した場合）
			#○X座標を一番右に戻す
			self.ship_x		= max_ship_x
			#│
			#○移動方向を左に変える ※速度はそのまま
			self.ship_vx 	= -abs(self.ship_vx)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1, resume=True)
			#┴
		#　│
		elif self.ship_y < 0:
		#　├→（宇宙船の『Y座標が上端』をはみ出した場合）
			#○Y座標を一番下に戻す
			self.ship_y		= 0
			#│
			#○移動方向を下に変える ※速度はそのまま
			self.ship_vy 	= abs(self.ship_vy)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1, resume=True)
			#┴
		#　│
		elif self.ship_y > max_ship_y:
		#　├→（宇宇宙船の『Y座標が下端』をはみ出した場合）
			#○Y座標を一番下に戻す
			self.ship_y		= max_ship_y
			#│
			#○移動方向を上に変える ※速度はそのまま
			self.ship_vy 	= -abs(self.ship_vy)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1, resume=True)
			#┴
		#　└┐（その他）※なにもしない
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃オブジェクトを追加（敵子分）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def add_henchman(self):
		#┬
		#◇┐タイマーの残りに合わせて、敵子分を追加する
		if self.timer_henchman == 0:
		#　├→（タイマーがゼロの場合）
			#●宇宙船から距離を30以上離す
			henchman_pos = self.get_position(30)
			#│
			#○敵子分のリストに追加する
			self.henchman.append(henchman_pos)
			#│
			#○タイマーを最初に戻す
			self.timer_henchman = INTERVAL_SURVIVOR
			#┴
		else:
		#　└┐（その他）
			#○タイマーをカウントダウンする
			self.timer_henchman -= 1
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃オブジェクトを追加（ボスキャラ）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def add_boss(self):
		#┬
		#◇┐タイマーの残りに合わせて、ボスキャラを追加する
		if self.timer_boss == 0:
		#　├→（タイマーがゼロの場合）
			#│
			#●1.1.宇宙船から距離を60以上離す
			boss_pos = self.get_position(60)
			#│
			#○ボスキャラのリストに追加する
			self.boss.append(boss_pos)
			#│
			#○タイマーを最初に戻す
			self.timer_boss = INTERVAL_METEOR
			#┴
		else:
		#　└┐（その他）
			#○タイマーをカウントダウンする
			self.timer_boss -= 1
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃接触判定（敵子分）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def check_henchman(self):
		#┬
		#□(0...n)敵子分の新しいリスト
		new_henchman = []
		#┴
		#┬
		#◎└┐リストの順番で、敵子分を接触判定する
		for henchman_x, henchman_y in self.henchman:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#◇┐当該の敵子分を判定する
			#　│
			#　├→（接触している場合）
			if self.check_collision(
				henchman_x,     # Ｘ座標
				henchman_y,     # Ｙ座標
				8,              # キャラクタの幅
				0              	# 敏感度
				):
				#│
				#○スコアを1点増やす
				self.score += 1
				#│
				#○効果音を鳴らす
				pyxel.play(1, 2, resume=True)
				#┴
			else:
			#　└┐（その他）
				#○敵子分の新しいリストに追加する
				new_henchman.append((henchman_x, henchman_y))
			#┴　┴
		#│
		#○敵子分のリストを新しいリストで入れ替える
		self.henchman = new_henchman
		#┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃接触判定（ボスキャラ）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def check_boss(self):
		#┬
		#◎└┐リストの順番で、ボスキャラを接触判定する
		for boss_x, boss_y in self.boss:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#│
			#◇当該のボスキャラを判定する
			#　│
			#　├→（接触している場合）
			if self.check_collision(
				boss_x,       # Ｘ座標
				boss_y,       # Ｙ座標
				16,             # キャラクタの幅
				-1              # 敏感度
				):
				#│
				#○タイトル表示モードを『オン』にする
				self.Scene = self.SCENE_GAMEOVER
				#┴
			#　└┐（その他）※なにもしない
		#┴　┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃【共通関数】宇宙船から一定距離離れた位置を得る 
		#┃【引　　数】最低の離す距離
		#┃【戻 り 値】リスト(X座標,Y座標)
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def get_position(self, dist):
		#┬
		#◎└┐座標が決まるまで繰り返す
		while True:
			#│
			#○ランダムに座標を求める
			x = pyxel.rndi(0, pyxel.width  - 8)
			y = pyxel.rndi(0, pyxel.height - 8)
			#│
			#○宇宙船との差を求める
			diff_x = x - self.ship_x
			diff_y = y - self.ship_y
			#│
			#◇┐宇宙船との差によって、座標を確定する
			if diff_x**2 + diff_y**2 > dist**2:
			#　│
			#　├→（指定の距離以上に離れている場合）
				#│
				#▼座標を返す
				return (x, y)
				#┴
			#　└┐（その他）※なにもしない
		#┴　┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃【共通関数】宇宙船とオブジェクトの接触判定 
		#┃【引　　数】① 対象のX座標
		#┃　　　　　　② 対象のY座標
		#┃　　　　　　③ キャラクタの幅（８か１６）
		#┃　　　　　　④ 敏感度(0：接触しやすい,マイナス：接触しにくい)
		#┃【戻 り 値】接触判定［True:接触している／False：接触していない］
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def check_collision(self,
		argX,			#①Ｘ座標
		argY,			#②Ｙ座標
		arg_width,		#③キャラクタの幅
		argSensitive	#④敏感度
		):
		#┬
		#◇┐Ｘ座標の重なり具合を求める
        #　├→（宇宙船が左、対象が右にある場合）
		if self.ship_x <= argX:
            #○宇宙船の幅を考えて、座標を比較する
			DiffX = ( argX  - (self.ship_x + 8) )
			#┴
		else:
		#　└┐（その他）
            #○対象の幅を考えて、座標を比較する
			DiffX = (self.ship_x - (argX + arg_width) )
			#┴
		#│
		#◇┐Ｙ座標の重なり具合を求める
		if self.ship_y <= argY:
        #　├→（宇宙船が上、対象が下にある場合）
            #○宇宙船の幅を考えて、座標を比較する
			DiffY = (argY - (self.ship_y + 8) )
			#┴
		else:
		#　└┐（その他）
            #○対象の幅を考えて、座標を比較する
			DiffY = (self.ship_y - (argY + arg_width) )
			#┴
		#│
        #▼判定結果を返す
		return (DiffX <= argSensitive and DiffY <= argSensitive)

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃『２．アプリを描画する』のサブ関数
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃空を描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_sky(self):
		#┬
		#○空を描画する条件をセットする
		num_grads	= 4		# グラデーションの数
		grad_height	= 6		# グラデーションの高さ
		grad_start_y = pyxel.height - grad_height * num_grads  # 描画開始位置
		#│
		#○画面をリセットする
		pyxel.cls(0)
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
		#┃宇宙船を描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_ship(self):
		#┬
		#○ジェット噴射の表示位置をずらす量を計算する
		offset_y = (pyxel.frame_count % 3 + 2) if self.is_jetting else 0
		offset_x = offset_y * -self.ship_dir
		#│
		#○左右方向のジェット噴射を描画する
			# ① 描画位置のX座標            [宇宙船のX座標]※位置をずらす
			# ② 描画位置のY座標            [宇宙船のY座標]
			# ③ 参照するイメージバンク番号 [0]
			# ④ 参照イメージの左上のX座標  [8]
			# ⑤ 参照イメージの左上のY座標  [8]
			# ⑥ 参照イメージの幅           [8]または[-8] ※負は左右反転
			# ⑦ 参照イメージの高さ         [8]
			# ⑧ 透明色                     [0]
		pyxel.blt(
			self.ship_x - self.ship_dir * 3 + offset_x, self.ship_y,
			0, 0, 0,
			8 * self.ship_dir, 8,
			0,
		)
		#│
		#○下方向のジェット噴射を描画する
			# ① 描画位置のX座標            [宇宙船のX座標]
			# ② 描画位置のY座標            [宇宙船のY座標] ※位置をずらす
			# ③ 参照するイメージバンク番号 [0]
			# ④ 参照イメージの左上のX座標  [8]
			# ⑤ 参照イメージの左上のY座標  [8]
			# ⑥ 参照イメージの幅           [8]
			# ⑦ 参照イメージの高さ         [8]
			# ⑧ 透明色                     [0]
		pyxel.blt(
			self.ship_x, self.ship_y + 3 + offset_y,
			0, 8, 8,
			8, 8,
			0,
		)
		#│
		#○宇宙船を描画する
			# ① 描画位置のX座標            [宇宙船のX座標]
			# ② 描画位置のY座標            [宇宙船のY座標]
			# ③ 参照するイメージバンク番号 [0]
			# ④ 参照イメージの左上のX座標  [8]
			# ⑤ 参照イメージの左上のY座標  [8]
			# ⑥ 参照イメージの幅           [8]
			# ⑦ 参照イメージの高さ         [8]
			# ⑧ 透明色                     [0]
		pyxel.blt(self.ship_x, self.ship_y, 0, 8, 0, 8, 8, 0)
		#│
		#◇┐５．宇宙船の状態に合わせて、爆発を描画する
		if self.Scene == self.SCENE_GAMEOVER:
		#　├→（宇宙船の状態が『爆発』の場合）
			#│
			#○爆発を描画する
			blast_x = self.ship_x + pyxel.rndi(1, 6)
			blast_y = self.ship_y + pyxel.rndi(1, 6)
			blast_radius = pyxel.rndi(2, 4)
			blast_color = pyxel.rndi(7, 10)
			pyxel.circ(blast_x, blast_y, blast_radius, blast_color)
			#┴
		#　└┐（その他）※なにもしない
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃敵子分を描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_henchman(self):
		#┬
		#◎└┐リストの順番で、敵子分を描画する
		for henchman_x, henchman_y in self.henchman:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#○当該の敵子分を描画する
			pyxel.blt(henchman_x, henchman_y, 0, 16, 0, 8, 8, 0)
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃ボスキャラを描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_boss(self):
		#┬
		#◎└┐リストの順番で、ボスキャラを描画する
		for boss_x, boss_y in self.boss:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#│
			#○当該のボスキャラを描画する
			pyxel.blt(boss_x, boss_y, 0, 24, 0, 16, 16, 0)
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃スコアを描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_score(self):
		#┬
		#○表示する文字を求める
		score = f"SCORE:{self.score}"
		#│
		#◎└┐影・文字の順に表示する
		for i in range(1, -1, -1):
			#│＼（影・文字の両方を表示し終えた場合）
			#│ ▼繰り返し処理を抜ける
			#○影・文字別に色を求める
			color = 7 if i == 0 else 0
			#│
			#○求めた色でスコアを表示する ※影と文字は1ドットずらす
			pyxel.text(3 + i, 3, score, color)
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃タイトルを描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_title(self):
		#┬
		#◎└┐影・文字の順に表示する
		for i in range(1, -1, -1):
			#│＼（影・文字の両方を表示し終えた場合）
			#│ ▼繰り返し処理を抜ける
			#○影・文字別に色を求める
			color = 10 if i == 0 else 8
			#│
			#○キー入力の案内を表示する
			pyxel.text(90, 70+ i, "- Press SPACE Key or Button -", color)
		#┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃ジェット噴射(ON/OFF)の判定
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def Fn_JetON(self):
		#┬
		#◇┐キーの状態に合わせて、宇宙船の速度を更新する
		if pyxel.btn(pyxel.KEY_SPACE)				: return True
		elif pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)		: return True
		elif pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)		: return True
		elif pyxel.btn(pyxel.GAMEPAD1_BUTTON_X)		: return True
		elif pyxel.btn(pyxel.GAMEPAD1_BUTTON_Y)		: return True
		#　├→（スペースキーかパッドのボタンが押された場合）
			#○『はい』を返す
			#┴
		#　└┐（その他）
		else 										: return False
			#○『いいえ』を返す
		#┴　┴
	def Fn_JetOFF(self):
		#┬
		#◇┐キーの状態に合わせて、宇宙船の速度を更新する
		if pyxel.btnr(pyxel.KEY_SPACE)				: return True
		elif pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)	: return True
		elif pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B)	: return True
		elif pyxel.btnr(pyxel.GAMEPAD1_BUTTON_X)	: return True
		elif pyxel.btnr(pyxel.GAMEPAD1_BUTTON_Y)	: return True
		#　├→（スペースキーかパッドのボタンが押された場合）
			#○『はい』を返す
			#┴
		#　└┐（その他）
		else 										: return False
			#○『いいえ』を返す
		#┴　┴