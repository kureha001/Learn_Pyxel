#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER5
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
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
	#□隕石用
	#□宇宙飛行士用
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
		#○１．Pyxelを初期化する
		pyxel.init(300, 200, title = GAME_TITLE)
		#│
		#○２．リソースファイルを読み込む
		pyxel.load("space_rescue.pyxres")
		#│
		#○３．シーンを『タイトル』にセットする
		self.Scene = self.SCENE_TITLE
		#│
		#○背景を初期化する
		self.objScreen	= None
		classScreen(self)
		#│
		#●４．ゲームをリセットする
		self.reset_game()
		#│
		#○５．アプリの実行を開始する
		pyxel.run(self.update, self.draw)
		#┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．アプリを更新 ※1秒に30回実行
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update(self):
		#┬
        #●背景を更新する
		self.objScreen.update()
		#　│
		#◇┐１．タイトル表示モードに合わせて、ゲームの流れを変える
		if self.Scene == self.SCENE_TITLE:
		#　├→（シーンを『タイトル』の場合）
			#◇┐1.1.エンターキーが押されている場合：
			#　├→（エンターキーが押されている場合）
			if pyxel.btnp(pyxel.KEY_RETURN):
				#○1.1.1.タイトル表示モードを『プレイ』にする
				self.Scene = self.SCENE_PLAY
				#│
				#●1.1.2.ゲームをリセットする
				self.reset_game()
				#┴
			#▼1.2.関数の処理をここでやめる
			return
		#　↓
		#　└┐（その他）※なにもしない
			#┴
		#│
		#○┐２．ゲームを更新する
		#　●2.1.宇宙船を更新する
		self.update_ship()
		#　│
		#　●2.2.オブジェクトを追加する（宇宙飛行士）
		self.add_survivor()
		#　│
		#　●2.3.オブジェクトを追加する（隕石）
		self.add_meteor()
		#　│
		#　●2.4.衝突判定（宇宙飛行士）
		self.check_survivor()
		#　│
		#　●2.5.衝突判定（隕石）
		self.check_meteor()
		#　┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．アプリを描画 ※1秒に30回実行
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw(self):
		#┬
		#●１．空を描画する
		self.draw_sky()
		#│
        #●背景を描画する
		self.objScreen.draw()
		#│
		#●２．宇宙船を描画する
		self.draw_ship()
		#│
		#●３．宇宙飛行士を描画する
		self.draw_survivors()
		#│
		#●４．隕石を描画する
		self.draw_meteors()
		#│
		#●５．スコアを描画する
		self.draw_score()
		#│
		#◇┐６．タイトルモードに合わせて、タイトルを描画する
		#　│
		#　├→（シーンが『タイトル』の場合）
		if self.Scene == self.SCENE_TITLE:
			#│
			#●6.1.タイトルを描画する
			self.draw_title()
			#┴
		#　↓
		#　└┐（その他）※なにもしない
			#┴
		#┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃『０．初期化する』『１．アプリを更新する』のサブ関数
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃【共通関数】ゲームをリセット
		#┃【利用箇所】0-4／1-1.1.2
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def reset_game(self):
		#┬
		#□得点（初期値：ゼロ）
		self.score 			= 0
		#│
		#□└┐出現タイマー（初期値：ゼロ）
			#□宇宙飛行士用
			#□隕石用
			#┴
		self.timer_survivor	= 0
		self.timer_meteor	= 0
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
		#□宇宙船の状態を（初期値：なし）[爆発=True｜正常=False]
		self.is_exploding	= False
		#│
		#□└┐オブジェクトのリスト（初期値：空）
			#□宇宙飛行士用
			#□隕石用
			#┴
		self.survivors		= []
		self.meteors		= []
		#┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃『１．アプリを更新する』のサブ関数
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃1-2.1.宇宙船を更新
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update_ship(self):
		#┬
		#◇┐１．キーの状態に合わせて、宇宙船の速度を更新する
		#　│
		#　├→（スペースキーが押されている場合）
		if pyxel.btn(pyxel.KEY_SPACE):
			#│
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
			pyxel.play(0, 0)
			#┴
		#　↓
		#　└┐（その他）
		else:
			#│
			#○噴射状態を「噴射なし」にする
			self.is_jetting	= False
			#│
			#○減速する(縦)
			self.ship_vy = min(self.ship_vy + SHIP_ACCEL_DOWN, MAX_SHIP_SPEED)
			#┴
		#│
		#◇┐２．キーの状態に合わせて、次に進む方向を変える
		#　│
		#　├→（スペースキーが離された場合）
		if pyxel.btnr(pyxel.KEY_SPACE):
			#│
			#○次に進む方向を反転する
			self.ship_dir = -self.ship_dir
			#┴
		#　↓
		#　└┐（その他）※なにもしない
			#┴
		#│
		#○└┐３．宇宙船を移動する
			#○X座標を変更する ※ベクトル量を加える
			#○Y座標を変更する ※ベクトル量を加える
		self.ship_x += self.ship_vx
		self.ship_y += self.ship_vy
			#┴
		#│
		#○└┐４．画面の終端位置を求める
			#│
			#○右端の位置(右端の８ドット手前)を求める
			#○下端の位置(下端の８ドット手前)求める
			#┴
		max_ship_x = pyxel.width	- 8
		max_ship_y = pyxel.height	- 8 

		#◇┐５．宇宙船の座標に合わせて、跳ね返す
		#　│
		#　├→（宇宙船の『X座標が左端』をはみ出した場合）
		if self.ship_x < 0:
			#│
			#○X座標を一番左に戻す
			self.ship_x		= 0
			#│
			#○移動方向を右に変える ※速度はそのまま
			self.ship_vx	= abs(self.ship_vx)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1)
			#┴
		#　│
		#　├→（宇宙船の『X座標が右端』をはみ出した場合）
		elif self.ship_x > max_ship_x:
			#│
			#○X座標を一番右に戻す
			self.ship_x		= max_ship_x
			#│
			#○移動方向を左に変える ※速度はそのまま
			self.ship_vx 	= -abs(self.ship_vx)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1)
			#┴
		#　│
		#　├→（宇宙船の『Y座標が上端』をはみ出した場合）
		elif self.ship_y < 0:
			#│
			#○Y座標を一番下に戻す
			self.ship_y		= 0
			#│
			#○移動方向を下に変える ※速度はそのまま
			self.ship_vy 	= abs(self.ship_vy)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1)
			#┴
		#　│
		#　├→（宇宇宙船の『Y座標が下端』をはみ出した場合）
		elif self.ship_y > max_ship_y:
			#│
			#○Y座標を一番下に戻す
			self.ship_y		= max_ship_y
			#│
			#○移動方向を上に変える ※速度はそのまま
			self.ship_vy 	= -abs(self.ship_vy)
			#│
			#○跳ね返り音を鳴らす
			pyxel.play(0, 1)
			#┴
		#　↓
		#　└┐（その他）※なにもしない
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃1-2.2.オブジェクトを追加（宇宙飛行士）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def add_survivor(self):
		#┬
		#◇┐１．タイマーの残りに合わせて、隕石を追加する
		#　│
		#　├→（タイマーがゼロの場合）
		if self.timer_survivor == 0:
			#│
			#●1.1.宇宙船から距離を30以上離す
			survivor_pos = self.get_position(30)
			#│
			#○宇宙飛行士のリストに追加する
			self.survivors.append(survivor_pos)
			#│
			#○タイマーを最初に戻す
			self.timer_survivor = INTERVAL_SURVIVOR
			#┴
		#　↓
		#　└┐２．（その他）
		else:
			#│
			#○タイマーをカウントダウンする
			self.timer_survivor -= 1
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃1-2.3.オブジェクトを追加（隕石）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def add_meteor(self):
		#┬
		#◇┐タイマーの残りに合わせて、宇宙飛行士を追加する
		#　│
		#　├→１．（タイマーがゼロの場合）
		if self.timer_meteor == 0:
			#│
			#●1.1.宇宙船から距離を60以上離す
			meteor_pos = self.get_position(60)
			#│
			#○隕石のリストに追加する
			self.meteors.append(meteor_pos)
			#│
			#○タイマーを最初に戻す
			self.timer_meteor = INTERVAL_METEOR
			#┴
		#　↓
		#　└┐２．（その他）
		else:
			#│
			#○タイマーをカウントダウンする
			self.timer_meteor -= 1
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃1-2.4.衝突判定（宇宙飛行士）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def check_survivor(self):
		#┬
		#□(0...n)宇宙飛行士の新しいリスト
		new_survivors = []
		#┴
		#┬
		#◎└┐リストの順番で、宇宙飛行士を衝突判定する
		for survivor_x, survivor_y in self.survivors:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#│
			#◇┐当該の宇宙飛行士を判定する
			#　│
			#　├→（衝突している場合）
			if self.check_collision(survivor_x, survivor_y):
				#│
				#○スコアを1点増やす
				self.score += 1
				#│
				#○救助音を鳴らす
				pyxel.play(1, 2)
				#┴
			#　↓
			#　└┐（その他）
			else:
				#│
				#○宇宙飛行士の新しいリストに追加する
				new_survivors.append((survivor_x, survivor_y))
				#┴
			#┴
		#│
		#○宇宙飛行士のリストを新しいリストで入れ替える
		self.survivors = new_survivors
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃1-2.5.衝突判定（隕石）
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def check_meteor(self):
		#┬
		#◎└┐リストの順番で、隕石を衝突判定する
		for meteor_x, meteor_y in self.meteors:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#│
			#◇当該の隕石を判定する
			#　│
			#　├→（衝突している場合）
			if self.check_collision(meteor_x, meteor_y):
				#│
				#○宇宙船の状態を『爆発』にする
				self.is_exploding	= True
				#│
				#○シーンを『タイトル』にセットする
				self.Scene = self.SCENE_TITLE
				#│
				#○発音を鳴らす
				pyxel.play(1, 3)
				#┴
			#　↓
			#　└┐（その他）※なにもしない
				#┴
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃【共通関数】宇宙船から一定距離離れた位置を得る 
		#┃【利用箇所】1.2.2.1.1／1.2.3.1.1
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
				#▼関数の処理をやめて、座標を返す
				return (x, y)
				#┴
			#　↓
			#　└┐（その他）※なにもしない
				#┴
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃【共通関数】宇宙船とオブジェクトの衝突判定 
		#┃【利用箇所】1.2.4／1.2.5
		#┃【引　　数】① 対象のX座標
		#┃　　　　　　② 対象のY座標
		#┃【戻 り 値】衝突判定［True:衝突している／False：衝突していない］
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def check_collision(self, x, y):
		#┬
		#▼関数の処理をやめて、座標を返す
		#  ※宇宙船との位置が5ドット以内(XY座標がともに)の場合は衝突
		return abs(self.ship_x - x) <= 5 and abs(self.ship_y - y) <= 5
		#┴


	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃『２．アプリを描画する』のサブ関数
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃2-1.空を描画
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
			#│
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
		#┃2-2.宇宙船を描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_ship(self):
		#┬
		#○１．ジェット噴射の表示位置をずらす量を計算する
		offset_y = (pyxel.frame_count % 3 + 2) if self.is_jetting else 0
		offset_x = offset_y * -self.ship_dir
		#│
		#○２．左右方向のジェット噴射を描画する
			# ① 描画位置のX座標            [宇宙船のX座標]※位置をずらす
			# ② 描画位置のY座標            [宇宙船のY座標]
			# ③ 参照するイメージバンク番号 [0]
			# ④ 参照イメージの左上のX座標  [8]
			# ⑤ 参照イメージの左上のY座標  [8]
			# ⑥ 参照イメージの幅           [8]または[-8] ※負は左右反転
			# ⑦ 参照イメージの高さ         [8]
			# ⑧ 透明色                     [0]
		pyxel.blt(
			self.ship_x - self.ship_dir * 3 + offset_x,
			self.ship_y,
			0,
			0,
			0,
			8 * self.ship_dir,
			8,
			0,
		)
		#│
		#○３．下方向のジェット噴射を描画する
			# ① 描画位置のX座標            [宇宙船のX座標]
			# ② 描画位置のY座標            [宇宙船のY座標] ※位置をずらす
			# ③ 参照するイメージバンク番号 [0]
			# ④ 参照イメージの左上のX座標  [8]
			# ⑤ 参照イメージの左上のY座標  [8]
			# ⑥ 参照イメージの幅           [8]
			# ⑦ 参照イメージの高さ         [8]
			# ⑧ 透明色                     [0]
		pyxel.blt(
			self.ship_x,
			self.ship_y + 3 + offset_y,
			0,
			8,
			8,
			8,
			8,
			0,
		)
		#│
		#○４．宇宙船を描画する
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
		if self.is_exploding:
		#　│
		#　├→（宇宙船の状態が『爆発』の場合）
			#│
			#○爆発を描画する
			blast_x = self.ship_x + pyxel.rndi(1, 6)
			blast_y = self.ship_y + pyxel.rndi(1, 6)
			blast_radius = pyxel.rndi(2, 4)
			blast_color = pyxel.rndi(7, 10)
			pyxel.circ(blast_x, blast_y, blast_radius, blast_color)
			#┴
		#　│
		#　└┐（その他）※なにもしない
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃2-3.宇宙飛行士を描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_survivors(self):
		#┬
		#◎└┐リストの順番で、宇宙飛行士を描画する
		for survivor_x, survivor_y in self.survivors:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#│
			#○当該の宇宙飛行士を描画する
			pyxel.blt(survivor_x, survivor_y, 0, 16, 0, 8, 8, 0)
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃2-4.隕石を描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_meteors(self):
		#┬
		#◎└┐リストの順番で、隕石を描画する
		for meteor_x, meteor_y in self.meteors:
			#│＼（リストの最後の要素を処理した場合）
			#│ ▼繰り返し処理を抜ける
			#│
			#○当該の隕石を描画する
			pyxel.blt(meteor_x, meteor_y, 0, 24, 0, 8, 8, 0)
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃2-5.スコアを描画
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
			#│
			#○影・文字別に色を求める
			color = 7 if i == 0 else 0
			#│
			#○求めた色でスコアを表示する ※影と文字は1ドットずらす
			pyxel.text(3 + i, 3, score, color)
			#┴
		#┴

		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃2-6.1.タイトルを描画
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw_title(self):
		#┬
		#◎└┐影・文字の順に表示する
		for i in range(1, -1, -1):
			#│＼（影・文字の両方を表示し終えた場合）
			#│ ▼繰り返し処理を抜ける
			#│
			#○影・文字別に色を求める
			color = 10 if i == 0 else 8
			#│
			#○求めた色でタイトルを表示する ※影と文字は1ドットずらす
			pyxel.text(57, 50 + i, GAME_TITLE, color)
			#┴
		#│
		#○キー入力の案内を表示する
		pyxel.text(42, 70, "- Press Enter Key -", 3)
		#┴