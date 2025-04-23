#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
import time

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ．ゲームクラス
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
	#┃０．初期化 
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self):
		#┬
        #○Pyxelを初期化する
        #○リソースファイルを読み込む
        pyxel.init(120, 160, title="Mega Wing")
        pyxel.load("mega_wing.pyxres")
        #│
        #○ゲームの状態を初期化する
        self.score          = 0     # スコア
        self.scene          = None  # 現在のシーン
        self.timer_pley     = 0     # プレイ時間
        self.level          = 0     # 難易度レベル
        #│
        #○インスタンスを初期化する
        self.background     = None  # 背景
        self.player         = None  # 自機
        self.enemies        = []    # 敵のリスト
        self.bulletsPlayer  = []    # 弾(自機)のリスト
        self.bulletsEnemy   = []    # 弾(敵機)のリスト
        self.Crushes        = []    # 爆発エフェクトのリスト
        #│
        #●背景を生成する(背景はシーンによらず常に存在する)
        #●タイトル画面を表示する
        #○ゲームの実行を開始する
        Background(self)
        self.show_Screen(Game.SCENE_TITLE)
        pyxel.run(self.update, self.draw)
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #●背景を更新する
        self.background.update()
		#│
		#○自機を更新する
		#○敵機を更新する
        self.update_Player()
        self.update_Enemies()
		#│
		#○弾(自機)を更新する
		#○弾(敵機)を更新する
        self.update_BulletsPlayer()
        self.update_BulletsEnemy()
		#│
		#○破壊を更新する
        self.update_Crushes()
        #│
        #●
        self.update_Scene()
        #┴

        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃1-x.弾(自機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Player(self):
		#┬
        #◇┐自機を更新する
        #　├→（自機が存在する場合）
        if self.player is not None:
            #│
            #●自機を更新する
            self.player.update()
			#┴
		#　└┐（その他）
			#┴
        #┴

        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃1-x.敵機の弾を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Enemies(self):
		#┬
		#◎└┐敵を更新する
        for enemy in self.enemies.copy():
			#│＼（すべての敵を処理し終えた）
			#│ ▼繰り返し処理を抜ける
            #●敵を更新する
            enemy.update()
            #│
            #◇┐自機・敵機の当たり判定を行う自機を更新する
            if self.player is not None and get_Hit(self.player, enemy):
            #　├→（自機が存在し、衝突している場合）
                #│
                #●自機にダメージを与える
                self.player.hit()
                #┴
            #　└┐（その他）
                #┴
            #┴
        #┴

        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃1-x.弾(自機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_BulletsPlayer(self):
		#┬
		#◎└┐弾(自機)を更新する
        for bullet in self.bulletsPlayer.copy():
			#│＼（すべての弾を処理し終えた）
			#│ ▼繰り返し処理を抜ける
            #●弾(自機)を更新する
            bullet.update()
            #│
            #◎└┐敵との当たり判定を行う
            for enemy in self.enemies.copy():
                #│＼（すべての敵を処理し終えた）
                #│ ▼繰り返し処理を抜ける
                #●弾(自機)と敵の衝突を見る
                if get_Hit(enemy, bullet):
                #　＼（衝突している場合）
                    #●弾(自機)にダメージを与える
                    bullet.hit()
                    #│
                    #●敵にダメージを与える
                    enemy.hit() 
                    #│
                    #◇┐
                    if self.player is not None:
                    #　├→（自機が存在する時場合）
                        #│
                        #○弾発射音を止める時間を設定する
                        self.player.timer_sound = 5
                        #┴
                    #　└┐（その他）
                        #┴
                    #┴
                #┴
            #┴
        #┴

        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃1-x.弾(敵機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_BulletsEnemy(self):
		#┬
        #◎└┐弾(敵機)を更新する
        for bullet in self.bulletsEnemy.copy():
            #│＼（）
            #│ ▼繰り返し処理を抜ける
            #●弾(敵機)を更新する
            bullet.update()
            #│
            #◇プレイヤーとの当たり判定を行う
            if self.player is not None and get_Hit(self.player, bullet):
            #　├→（）
                #│
                #●弾(敵機)にダメージを与える
                bullet.hit()
                #│
                #●自機にダメージを与える
                self.player.hit()
                #┴
            #　└┐（その他）
                #┴
            #┴
        #┴

        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃1-x.破壊を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Crushes(self):
		#┬
        #◎└┐爆発エフェクトを更新する
        for Crush in self.Crushes.copy():
            #│＼（）
            #│ ▼繰り返し処理を抜ける
            #●
            Crush.update()
            #┴
        #┴

        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃1-x.更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Scene(self):
        #◇┐シーンを更新する
        if self.scene == Game.SCENE_TITLE: 
        #　├→（タイトル画面の場合）
            #│
            #◇┐
            if pyxel.btnp(pyxel.KEY_RETURN):
            #　├→（エンターキーが押された場合）
                #│
                #○BGMの再生を止める
                pyxel.stop()
                #│
                #●プレー画面を表示する
                self.show_Screen(Game.SCENE_PLAY)
                #┴
            #　└┐（その他）
                #┴
        #　│
        elif self.scene == Game.SCENE_PLAY:
        #　├→（プレイ画面の場合）
            #│
            #○プレイ時間をカウントする
            self.timer_pley += 1
            #│
            #○
            self.level = self.timer_pley // 450 + 1
            # 15秒(毎秒30フレームx15)毎に難易度を1上げる
            #│
            #◇┐敵を出現させる
            spawn_interval = max(60 - self.level * 10, 10)
            if self.timer_pley % spawn_interval == 0:
            #　├→（出現タイミングの場合）
                #│
                #○敵機の種類をランダムに求める
                kind = pyxel.rndi(Enemy.KIND_A, Enemy.KIND_C)
                #│
                #●
                Enemy(self, kind, self.level, pyxel.rndi(0, 112), -8)
                #┴
            #　└┐（その他）
                #┴
			#┴
        #　│
        elif self.scene == Game.SCENE_GAMEOVER:
        #　├→（ゲームオーバー画面の場合）
            #│
            #◇┐
            if self.timer_display > 0:
            #　├→（画面表示時間が残っている場合）
                #│
                #●画面表示時間をカウントダウンする
                self.timer_display -= 1
                #┴
            #　│
            else:
            #　└┐（その他
                #●タイトル画面を表示する
                self.show_Screen(Game.SCENE_TITLE)
                #┴
			#┴
		#　└┐（その他）
			#┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○画面をクリアする
        pyxel.cls(0)
        #│
        #●背景を描画する
        self.background.draw()
        #│
        #◇┐自機を描画する
        if self.player is not None          : self.player.draw()
        #　├→（自機が存在する場合）
            #●描画する
			#┴
		#　└┐（その他）
			#┴
        #│
        #◎└┐敵を描画する
        for enemy in self.enemies:
            #│＼（すべての敵を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●描画する
            enemy.draw()
			#┴
        #│
        #◎└┐弾(自機)を描画する
        for bullet in self.bulletsPlayer:
            #│＼（すべての弾を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●描画する
            bullet.draw()
			#┴
        #│
        #◎└┐弾(敵機)を描画する
        for bullet in self.bulletsEnemy: 
            #│＼（すべての弾を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●描画する
            bullet.draw()
			#┴
        #│
        #◎└┐爆発エフェクトを描画する
        for Crush in self.Crushes:
            #│＼（すべての爆発を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●描画する
            Crush.draw()
			#┴
        #│
        #○スコアを描画する
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)
        #│
        #◇┐シーンを描画する
        if self.scene == Game.SCENE_TITLE:
        #　├→（タイトル画面の場合）
            #│
            #〇メッセージを表示する
            pyxel.blt(0, 18, 2, 0, 0, 120, 120, 15)
            pyxel.text(31, 148, "- PRESS ENTER -", 6)
			#┴
        #　│
        elif self.scene == Game.SCENE_GAMEOVER:
        #　├→（ゲームオーバー画面の場合）
            #│
            #〇メッセージを表示する
            pyxel.text(43, 78, "GAME OVER", 8)
			#┴
        #　└┐（その他）
			#┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃シーンを変更する
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def show_Screen(self, scene):
		#┬
        #○シーンを引数から求める
        self.scene = scene
        #│
        #◇┐画面を表示する
        if self.scene == Game.SCENE_TITLE:
        #　├→（シーンがタイトル画面の場合）
            #│
            #●自機を消滅する
            self.player = None
            #│
            #●敵をクリアする
            #●弾(自分)と敵を削除する
            #●弾(敵機)と敵を削除する
            self.enemies.clear()
            self.bulletsPlayer.clear()
            self.bulletsEnemy.clear()
            #│
            #○BGMを再生する
            pyxel.playm(0, loop=True)
            #┴
        #　│
        elif self.scene == Game.SCENE_PLAY:
        #　├→（シーンがプレイ画面の場合）
            #│
            #○プレイ状態を初期化する
            self.score      = 0  # スコアを0に戻す
            self.timer_pley = 0  # プレイ時間を0に戻す
            self.level      = 1  # 難易度レベルを1に戻す
            #│
            #○BGMを再生する
            pyxel.playm(1, loop=True)
            #│
            #●自機を生成する
            Player(self, 56, 140)
            #┴
        #　│
        elif self.scene == Game.SCENE_GAMEOVER:
        #　├→（シーンがゲームオーバー画面の場合）
            #│
            #○画面表示時間を設定する
            self.timer_display = 60
            #│
            #●自機を消滅する
            self.player = None
            #┴
		#　└┐（その他）
			#┴
        #┴
    
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.背景クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Background:
    #┬
    #□星の数
    NUM_STARS = 100 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self, game):
		#┬
        self.game   = game  # ゲームへの参照
        self.stars  = []    # 星の座標と速度のリスト
        #│
        #◎└┐星の座標と速度を初期化してリストに登録する
        for i in range(Background.NUM_STARS):
            #│＼（）
            #│ ▼繰り返し処理を抜ける
            #○X座標を求める
            #○Y座標を求める
            #○方向の速度を求める
            x  = pyxel.rndi(0, pyxel.width  - 1 )  
            y  = pyxel.rndi(0, pyxel.height - 1 )  
            vy = pyxel.rndf(1, 2.5              ) 
            #│
            #○
            self.stars.append((x, y, vy))
            #┴
        #│
        #〇ゲームに背景を登録する
        self.game.background = self
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #◎└┐
        for i, (x, y, vy) in enumerate(self.stars):
			#│＼（）
			#│ ▼繰り返し処理を抜ける
            #○前に進める
            y += vy
            #│
            if y >= pyxel.height:  # 画面下から出たか
                y -= pyxel.height  # 画面上に戻す
                #┴
            #│
            #○
            self.stars[i] = (x, y, vy)
            #┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #◇┐銀河を描画する
        if self.game.scene != Game.SCENE_TITLE:
        #　├→（タイトル画面以外の場合）
            #│
            #○銀河を描画する
            pyxel.blt(0, 0, 1, 0, 0, 120, 160)
            #┴
		#　└┐（その他）
			#┴
        #│
        #◎└┐星を描画する
        for x, y, speed in self.stars:
			#│＼（）
			#│ ▼繰り返し処理を抜ける
            #○速度に応じて色を変える
            color = 12 if speed > 1.8 else 5
            pyxel.pset(x, y, color)
            #┴
        #┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅲ.自機クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Player:
    #┬
    #□移動速度
    #□弾の発射間隔
    MOVE_SPEED      = 2
    SHOT_INTERVAL   = 6 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self, game, x, y):
		#┬
        #○
        self.chPos      = [0,0,0,0]
        self.game       = game          # ゲームへの参照
        self.x          = x             # X座標
        self.y          = y             # Y座標
        self.hit_area   = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2)
        self.timer_shot = 0             # 弾発射までの残り時間
        #│
        #〇ゲームに自機を登録する
        self.game.player = self
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新す
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #◇┐キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT ) : self.x -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) : self.x += Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_UP   ) : self.y -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN ) : self.y += Player.MOVE_SPEED
        #│
        #〇自機の画面位置を補正する
        self.x = max(self.x, 0                  )
        self.x = min(self.x, pyxel.width - 8    )
        self.y = max(self.y, 0                  )
        self.y = min(self.y, pyxel.height - 8   )
        #│
        #◇┐弾を発射する ※弾発射までの残り時間を減らす
        if self.timer_shot > 0: self.timer_shot -= 1
        #│
        #◇┐
        if pyxel.btn(pyxel.KEY_SPACE) and self.timer_shot == 0:
        #　├→（）
            #│
            #○弾(自機)を生成する
            Bullet(self.game, Bullet.SIDE_PLAYER, self.x, self.y - 3, -90, 5)
            #│
            #○弾発射音を再生する
            pyxel.play(3, 0)
            #│
            #○次の弾発射までの残り時間を設定する
            self.timer_shot = Player.SHOT_INTERVAL
            #┴
        #　└┐（その他）
            #┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0)
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃被弾
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def hit(self):
		#┬
        #●爆発エフェクトを生成する
        Crush(self.game, self.x + 4, self.y + 4)
        #│
        #○BGMを止めて爆発音を再生する
        pyxel.stop()
        pyxel.play(0, 2)
        #│
        #○自機を消滅する
        self.game.player = None
        #│
        #●ゲームオーバー画面を表示する
        self.game.show_Screen(self.game.SCENE_GAMEOVER)
        #┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅳ.敵クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Enemy:
    #┬
    #□敵A
    #□敵B
    #□敵C
    KIND_A = 0
    KIND_B = 1
    KIND_C = 2
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self, game, kind, level, x, y):
		#┬
        #○
        self.game = game
        self.kind = kind  # 敵の種類
        self.level = level  # 強さ
        #│
        #○
        self.x = x
        self.y = y
        #│
        #○
        self.hit_area = (0, 0, 7, 7)
        self.armor = self.level - 1 # 装甲
        self.life_time = 0          # 生存時間
        self.is_damaged = False     # ダメージを受けたかどうか
        #│
        #○ゲームの敵リストに登録する
        self.game.enemies.append(self)
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○生存時間をカウントする
        self.life_time += 1
        #│
        #◇┐敵を更新する
        if self.kind == Enemy.KIND_A:
        #　├→（種類が敵Aの場合）
            #│
            #○前方に移動させる
            self.y += 1.2
            #│
            #◇┐弾を発射する
            if self.life_time % 50 == 0:
            #　├→（生存時間が50カウントの場合）
                #│
                #●自機の角度を求める
                player_angle = self.get_Angle()
                #│
                #●弾を発射する
                Bullet(
                    self.game,
                    Bullet.SIDE_ENEMY,
                    self.x,
                    self.y,
                    player_angle,
                    2
                    )
                #┴
            #　└┐（その他）
                #┴
            #┴
        #　│
        elif self.kind == Enemy.KIND_B:
        #　├→（種類が敵Bの場合）
            #│
            #○前方に移動させる
            self.y += 1
            #│
            #◇┐左右に移動する
            if self.life_time // 30 % 2 == 0:
            #　├→（生存時間が30カウントの場合）
                #│
                #○右に移動する
                self.x += 1.2
                #┴
            #　│
            else:
            #　└┐（その他）
                #○左に移動する
                self.x -= 1.2
                #┴
            #┴
        #　│
        elif self.kind == Enemy.KIND_C:
        #　├→（種類が敵Cの場合）
            #│
            #○前方に移動させる
            self.y += 0.8
            #│
            #◇┐弾を発射する
            if self.life_time % 40 == 0:
            #　├→（生存時間が40カウントの場合）
                #│
                #◎└┐４方向に発射する
                for i in range(4):
                    #│＼（4方向の処理を終えた場合）
                    #│ ▼繰り返し処理を抜ける
                    #○当該の方向に弾を発射する
                    Bullet(
                        self.game,
                        Bullet.SIDE_ENEMY,
                        self.x, self.y,
                        i * 45 + 22,
                        2
                        )
                    #┴
                #┴
            #　└┐（その他）
                #┴
            #┴
        #│
        #◇┐敵が画面下から出たら敵リストから登録を削除する
        if self.y >= pyxel.height:
        #　├→（画面下から出た場合）
            #│
            #◇┐
            if self in self.game.enemies:
            #　├→（敵が存在する場合）
                #│
                #○敵リストから登録を削除する
                self.game.enemies.remove(self) 
                #┴
            #　└┐（その他）
                #┴
            #┴
        #　└┐（その他）
            #┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #◇┐
        if self.is_damaged:
        #　├→（ダメージを受ける場合）
            #│
            #○ダメージを受けないようにする
            self.is_damaged = False
            #│
            #◎└┐
            for i in range(1, 15):
                #│＼（）
                #│ ▼繰り返し処理を抜ける
                #○
                pyxel.pal(i, 15)
                #┴
            #│
            #○
            pyxel.blt(
                self.x, self.y,
                0,
                self.kind * 8 + 8,
                0,
                8, 8,
                0
                )
            pyxel.pal()
            #┴
        #　│
        else:
        #　└┐（その他）
            #○
            pyxel.blt(
                self.x, self.y,
                0,
                self.kind * 8 + 8,
                0,
                8, 8,
                0
                )
            #┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃被弾
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def hit(self):
		#┬
        #◇┐
        if self.armor > 0:
        #　├→（装甲が残っている場合）
            #│
            #○装甲を減らす
            self.armor -= 1
            #│
            #○ダメージフラグを『ＯＮ』にする
            self.is_damaged = True
            #│
            #○ダメージ音を再生する
            pyxel.play(2, 1, resume=True)
            #│
            #▼
            return
        #│
        #●爆発エフェクトを生成する
        Crush(self.game, self.x + 4, self.y + 4)
        #│
        #○爆発音を再生する
        pyxel.play(2, 2, resume=True) 
        #│
        #◇┐敵を削除する
        if self in self.game.enemies:
        #　├→（敵リストに登録されている場合）
            #│
            #○リストから削除する
            self.game.enemies.remove(self)
            #┴
        #　└┐（その他）
            #┴
        #│
        #○スコアを加算する
        self.game.score += self.level * 10
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃発射角を得る
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def get_Angle(self):
		#┬
        #○自機を参照する
        player = self.game.player
        #│
        #◇┐角度を求める
        if player is None: 
        #　├→（自機が存在しない場合）
            #│
            #▼90度を返す
            return 90
        #　│
        else:
		#　└┐（その他）
            #▼自機の方角を返す
            return pyxel.atan2(player.y - self.y, player.x - self.x)
        #┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅴ.弾クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Bullet:
    #┬
    #□弾(自機)
    #□弾(敵機)
    SIDE_PLAYER = 0
    SIDE_ENEMY  = 1 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self, game, side, x, y, angle, speed):
		#┬
        #○
        self.game = game
        self.side = side
        self.x = x
        self.y = y
        self.vx = pyxel.cos(angle) * speed
        self.vy = pyxel.sin(angle) * speed
        #│
        #◇┐弾を増やす
        if self.side == Bullet.SIDE_PLAYER:
        #　├→（弾の種類が『自機』の場合）
            #│
            #○
            self.hit_area = (2, 1, 5, 6)
            #│
            #○弾(自機)を増やす
            game.bulletsPlayer.append(self)
            #┴
        #│
        else:
        #　└┐（その他）
            #○
            self.hit_area = (2, 2, 5, 5)
            #│
            #○敵機の弾を増やす
            game.bulletsEnemy.append(self)
            #┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○弾の座標を更新する
        self.x += self.vx
        self.y += self.vy
        #│
        #◇┐弾リストから登録を削除する
        if (
            self.x <= -8 or self.x >= pyxel.width   or
            self.y <= -8 or self.y >= pyxel.height
        ):
        #　├→（弾が画面外に出た場合）
            #│
            #◇┐弾を削除する
            if self.side == Bullet.SIDE_PLAYER:
            #　├→（弾(自機)リストに登録されている場合）
                #│
                #○弾(自機)リストから削除する
                self.game.bulletsPlayer.remove(self)
                #┴
            #│
            else:
            #　└┐（その他）
                #○弾(敵機)リストから削除する
                self.game.bulletsEnemy.remove(self)
                #┴
            #┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃３．描画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        src_x = 0 if self.side == Bullet.SIDE_PLAYER else 8
        pyxel.blt(self.x, self.y, 0, src_x, 8, 8, 8, 0)
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃被弾
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def hit(self):
		#┬
        #◇┐弾をリストから削除する
        if self.side == Bullet.SIDE_PLAYER:
        #　├→（場合）
            #│
            #◇┐弾をリストから削除する
            if self in self.game.bulletsPlayer:
            #　├→（弾(自機)リストに登録されている場合）
                #│
                #○リストから削除する
                self.game.bulletsPlayer.remove(self)
                #┴
            #　└┐（その他）
                #┴
            #┴
        #　│
        elif self in self.game.bulletsEnemy:
        #　├→（弾(敵機)リストに登録されている時場合）
            #│
            #○リストから削除する
            self.game.bulletsEnemy.remove(self)
            #┴
        #　└┐（その他）
            #┴
        #┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅵ.爆発クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Crush:
    #┬
    #□開始時の半径
    #□終了時の半径
    START_RADIUS    = 1
    END_RADIUS      = 8 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self, game, x, y):
		#┬
        #○
        self.game = game
        self.x = x
        self.y = y
        self.radius = Crush.START_RADIUS  # 爆発の半径
        #│
        #○ゲームの爆発エフェクトリストに登録する
        game.Crushes.append(self)
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○半径を大きくする
        self.radius += 1
        #│
        #○爆発を削除する
        if self.radius > Crush.END_RADIUS:
        #　├→（半径が最大になった場合）
            #│
            #○当該の爆発をリストから削除する
            self.game.Crushes.remove(self)
            #┴
        #┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○
        pyxel.circ (self.x, self.y, self.radius,  7)
        pyxel.circb(self.x, self.y, self.radius, 10)
        #┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃衝突判定
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_Hit(entity1, entity2):
    #┬
    #○
    entity1_x1 = entity1.x + entity1.hit_area[0]
    entity1_y1 = entity1.y + entity1.hit_area[1]
    entity1_x2 = entity1.x + entity1.hit_area[2]
    entity1_y2 = entity1.y + entity1.hit_area[3]
    #│
    #○
    entity2_x1 = entity2.x + entity2.hit_area[0]
    entity2_y1 = entity2.y + entity2.hit_area[1]
    entity2_x2 = entity2.x + entity2.hit_area[2]
    entity2_y2 = entity2.y + entity2.hit_area[3]
    #│
    # キャラクター1の左端がキャラクター2の右端より右にある
    # キャラクター1の右端がキャラクター2の左端より左にある
    # キャラクター1の上端がキャラクター2の下端より下にある
    # キャラクター1の下端がキャラクター2の上端より上にある
    if entity1_x1 > entity2_x2: return False
    if entity1_x2 < entity2_x1: return False
    if entity1_y1 > entity2_y2: return False
    if entity1_y2 < entity2_y1: return False
    #│
    #▼上記のどれでもなければ重なっている
    return True
    #┴

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅶ.メイン処理
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┬
#●ゲームのクラスを実行する
Game()
#┴
