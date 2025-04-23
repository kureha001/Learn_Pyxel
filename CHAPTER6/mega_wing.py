#====================================================== 
# インクルード・ライブラリ
#====================================================== 
import mmpPeter # MMPペーター
import pyxel    # ゲームエンジン
import time

# 背景クラス
class Background:
    NUM_STARS = 100  # 星の数

    # 背景を初期化してゲームに登録する
    def __init__(self, game):
        self.game = game  # ゲームへの参照
        self.stars = []  # 星の座標と速度のリスト

        # 星の座標と速度を初期化してリストに登録する
        for i in range(Background.NUM_STARS):
            x = pyxel.rndi(0, pyxel.width - 1)  # X座標
            y = pyxel.rndi(0, pyxel.height - 1)  # Y座標
            vy = pyxel.rndf(1, 2.5)  # Y方向の速度
            self.stars.append((x, y, vy))  # タプルとしてリストに登録

        # ゲームに背景を登録する
        self.game.background = self

    # 背景を更新する
    def update(self):
        for i, (x, y, vy) in enumerate(self.stars):
            y += vy
            if y >= pyxel.height:  # 画面下から出たか
                y -= pyxel.height  # 画面上に戻す
            self.stars[i] = (x, y, vy)

    # 背景を描画する
    def draw(self):
        # タイトル画面以外で銀河を描画する
        if self.game.scene != Game.SCENE_TITLE:
            pyxel.blt(0, 0, 1, 0, 0, 120, 160)

        # 星を描画する
        for x, y, speed in self.stars:
            color = 12 if speed > 1.8 else 5  # 速度に応じて色を変える
            pyxel.pset(x, y, color)


# 自機クラス
class Player:
    MOVE_SPEED = 2  # 移動速度
    SHOT_INTERVAL = 6  # 弾の発射間隔

    # 自機を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.chPos = [0,0,0,0]
        self.game = game  # ゲームへの参照
        self.x = x  # X座標
        self.y = y  # Y座標
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2)
        self.shot_timer = 0  # 弾発射までの残り時間

        # ゲームに自機を登録する
        self.game.player = self

    # 自機にダメージを与える
    def add_damage(self):
        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)

        # BGMを止めて爆発音を再生する
        pyxel.stop()
        pyxel.play(0, 2)

        # 自機を削除する
        self.game.player = None

        # シーンをゲームオーバー画面に変更する
        self.game.change_scene(self.game.SCENE_GAMEOVER)

    # ★自機を更新する
    def update(self):
        #〇MMPを読み取る。
        objMMP.read()
        while objMMP.read_Ready == False : time.sleep(0)
        for i in range(objMMP.anaPins):
            self.chPos[i] = int(objMMP.valAnaPin[0][i])
        time.sleep(1/40)    # フレームレート(秒)
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT) or (objMMP.valAnaPin[0][1]<50):
            self.x -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) or (objMMP.valAnaPin[0][1]>54):
            self.x += Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_UP) or (objMMP.valAnaPin[0][0]<50):
            self.y -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN) or (objMMP.valAnaPin[0][0])>54:
            self.y += Player.MOVE_SPEED

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - 8)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - 8)

        # 弾を発射する
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

#        if pyxel.btn(pyxel.KEY_SPACE) and self.shot_timer == 0:
        if   objMMP.valAnaPin[0][2] > 75: tmpKey=3
        elif objMMP.valAnaPin[0][2] > 30: tmpKey=2
        elif objMMP.valAnaPin[0][2] > 15: tmpKey=1
        else                            : tmpKey=0
        if tmpKey>0 and self.shot_timer == 0:
            # 自機の弾を生成する
            Bullet(self.game, Bullet.SIDE_PLAYER, self.x, self.y - 3, -90, 5)

            # 弾発射音を再生する
            pyxel.play(3, 0)

            # 次の弾発射までの残り時間を設定する
            self.shot_timer = Player.SHOT_INTERVAL

    # 自機を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0)


# 敵クラス
class Enemy:
    KIND_A = 0  # 敵A
    KIND_B = 1  # 敵B
    KIND_C = 2  # 敵C

    # 敵を初期化してゲームに登録する
    def __init__(self, game, kind, level, x, y):
        self.game = game
        self.kind = kind  # 敵の種類
        self.level = level  # 強さ
        self.x = x
        self.y = y
        self.hit_area = (0, 0, 7, 7)
        self.armor = self.level - 1  # 装甲
        self.life_time = 0  # 生存時間
        self.is_damaged = False  # ダメージを受けたかどうか

        # ゲームの敵リストに登録する
        self.game.enemies.append(self)

    # 敵にダメージを与える
    def add_damage(self):
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1
            self.is_damaged = True

            # ダメージ音を再生する
            pyxel.play(2, 1, resume=True)  # チャンネル2で割り込み再生させる
            return

        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)

        # 爆発音を再生する
        pyxel.play(2, 2, resume=True)  # チャンネル2で割り込み再生させる

        # 敵をリストから削除する
        if self in self.game.enemies:  # 敵リストに登録されている時
            self.game.enemies.remove(self)

        # スコアを加算する
        self.game.score += self.level * 10

    # 自機の方向の角度を計算する
    def calc_player_angle(self):
        player = self.game.player
        if player is None:  # 自機が存在しない時
            return 90
        else:  # 自機が存在する時
            return pyxel.atan2(player.y - self.y, player.x - self.x)

    # 敵を更新する
    def update(self):
        # 生存時間をカウントする
        self.life_time += 1

        # 敵Aを更新する
        if self.kind == Enemy.KIND_A:
            # 前方に移動させる
            self.y += 1.2

            # 一定時間毎に自機の方向に向けて弾を発射する
            if self.life_time % 50 == 0:
                player_angle = self.calc_player_angle()
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle, 2)

        # 敵Bを更新する
        elif self.kind == Enemy.KIND_B:
            # 前方に移動させる
            self.y += 1

            # 経過時間に応じて左右に移動する
            if self.life_time // 30 % 2 == 0:
                self.x += 1.2
            else:
                self.x -= 1.2

        # 敵Cを更新する
        elif self.kind == Enemy.KIND_C:
            # 前方に移動させる
            self.y += 0.8

            # 一定時間毎に４方向に弾を発射する
            if self.life_time % 40 == 0:
                for i in range(4):
                    Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, i * 45 + 22, 2)

        # 敵が画面下から出たら敵リストから登録を削除する
        if self.y >= pyxel.height:  # 画面下から出たか
            if self in self.game.enemies:
                self.game.enemies.remove(self)  # 敵リストから登録を削除する

    # 敵を描画する
    def draw(self):
        if self.is_damaged:
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)
            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 8, 0, 8, 8, 0)
            pyxel.pal()
        else:
            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 8, 0, 8, 8, 0)


# 弾クラス
class Bullet:
    SIDE_PLAYER = 0  # 自機の弾
    SIDE_ENEMY = 1  # 敵の弾

    # 弾を初期化してゲームに登録する
    def __init__(self, game, side, x, y, angle, speed):
        self.game = game
        self.side = side
        self.x = x
        self.y = y
        self.vx = pyxel.cos(angle) * speed
        self.vy = pyxel.sin(angle) * speed

        # 弾の種類に応じた初期化とリストへの登録を行う
        if self.side == Bullet.SIDE_PLAYER:
            self.hit_area = (2, 1, 5, 6)
            game.player_bullets.append(self)
        else:
            self.hit_area = (2, 2, 5, 5)
            game.enemy_bullets.append(self)

    # 弾にダメージを与える
    def add_damage(self):
        # 弾をリストから削除する
        if self.side == Bullet.SIDE_PLAYER:
            if self in self.game.player_bullets:  # 自機の弾リストに登録されている時
                self.game.player_bullets.remove(self)
        else:
            if self in self.game.enemy_bullets:  # 敵の弾リストに登録されている時
                self.game.enemy_bullets.remove(self)

    # 弾を更新する
    def update(self):
        # 弾の座標を更新する
        self.x += self.vx
        self.y += self.vy

        # 弾が画面外に出たら弾リストから登録を削除する
        if (
            self.x <= -8
            or self.x >= pyxel.width
            or self.y <= -8
            or self.y >= pyxel.height
        ):
            if self.side == Bullet.SIDE_PLAYER:
                self.game.player_bullets.remove(self)
            else:
                self.game.enemy_bullets.remove(self)

    # 弾を描画する
    def draw(self):
        src_x = 0 if self.side == Bullet.SIDE_PLAYER else 8
        pyxel.blt(self.x, self.y, 0, src_x, 8, 8, 8, 0)


# 爆発エフェクトクラス
class Blast:
    START_RADIUS = 1  # 開始時の半径
    END_RADIUS = 8  # 終了時の半径

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.radius = Blast.START_RADIUS  # 爆発の半径

        # ゲームの爆発エフェクトリストに登録する
        game.blasts.append(self)

    # 爆発エフェクトを更新する
    def update(self):
        # 半径を大きくする
        self.radius += 1

        # 半径が最大になったら爆発エフェクトリストから登録を削除する
        if self.radius > Blast.END_RADIUS:
            self.game.blasts.remove(self)

    # 爆発エフェクトを描画する
    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 7)
        pyxel.circb(self.x, self.y, self.radius, 10)


# キャラクター同士のヒットエリアが重なっているか判定する
def check_collision(entity1, entity2):
    entity1_x1 = entity1.x + entity1.hit_area[0]
    entity1_y1 = entity1.y + entity1.hit_area[1]
    entity1_x2 = entity1.x + entity1.hit_area[2]
    entity1_y2 = entity1.y + entity1.hit_area[3]

    entity2_x1 = entity2.x + entity2.hit_area[0]
    entity2_y1 = entity2.y + entity2.hit_area[1]
    entity2_x2 = entity2.x + entity2.hit_area[2]
    entity2_y2 = entity2.y + entity2.hit_area[3]

    # キャラクター1の左端がキャラクター2の右端より右にある
    if entity1_x1 > entity2_x2:
        return False

    # キャラクター1の右端がキャラクター2の左端より左にある
    if entity1_x2 < entity2_x1:
        return False

    # キャラクター1の上端がキャラクター2の下端より下にある
    if entity1_y1 > entity2_y2:
        return False

    # キャラクター1の下端がキャラクター2の上端より上にある
    if entity1_y2 < entity2_y1:
        return False

    # 上記のどれでもなければ重なっている
    return True


# ゲームクラス(ゲーム全体を管理するクラス)
class Game:
    SCENE_TITLE = 0  # タイトル画面
    SCENE_PLAY = 1  # プレイ画面
    SCENE_GAMEOVER = 2  # ゲームオーバー画面

    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(120, 160, title="Mega Wing")

        # リソースファイルを読み込む
        pyxel.load("mega_wing.pyxres")

        # ゲームの状態を初期化する
        self.score = 0  # スコア
        self.scene = None  # 現在のシーン
        self.play_time = 0  # プレイ時間
        self.level = 0  # 難易度レベル
        self.background = None  # 背景
        self.player = None  # 自機
        self.enemies = []  # 敵のリスト
        self.player_bullets = []  # 自機の弾のリスト
        self.enemy_bullets = []  # 敵の弾のリスト
        self.blasts = []  # 爆発エフェクトのリスト

        # 背景を生成する(背景はシーンによらず常に存在する)
        Background(self)

        # シーンをタイトル画面に変更する
        self.change_scene(Game.SCENE_TITLE)

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する
    def change_scene(self, scene):
        self.scene = scene

        # タイトル画面
        if self.scene == Game.SCENE_TITLE:
            # 自機を削除する
            self.player = None  # プレイヤーを削除

            # 全ての弾と敵を削除する
            self.enemies.clear()
            self.player_bullets.clear()
            self.enemy_bullets.clear()

            # BGMを再生する
            pyxel.playm(0, loop=True)

        # プレイ画面
        elif self.scene == Game.SCENE_PLAY:
            # プレイ状態を初期化する
            self.score = 0  # スコアを0に戻す
            self.play_time = 0  # プレイ時間を0に戻す
            self.level = 1  # 難易度レベルを1に戻す

            # BGMを再生する
            pyxel.playm(1, loop=True)

            # 自機を生成する
            Player(self, 56, 140)

        # ゲームオーバー画面
        elif self.scene == Game.SCENE_GAMEOVER:
            # 画面表示時間を設定する
            self.display_timer = 60

            # 自機を削除する
            self.player = None

    # ゲーム全体を更新する
    def update(self):
        # 背景を更新する
        self.background.update()

        # 自機を更新する
        if self.player is not None:
            self.player.update()

        # 敵を更新する
        # ループ中に要素の追加・削除が行われても問題ないようにコピーしたリストを使用する
        for enemy in self.enemies.copy():
            enemy.update()

            # 自機と敵の当たり判定を行う
            if self.player is not None and check_collision(self.player, enemy):
                self.player.add_damage()  # 自機にダメージを与える

        # 自機の弾を更新する
        for bullet in self.player_bullets.copy():
            bullet.update()

            # 自機の弾と敵の当たり判定を行う
            for enemy in self.enemies.copy():
                if check_collision(enemy, bullet):
                    bullet.add_damage()  # 自機の弾にダメージを与える
                    enemy.add_damage()  # 敵にダメージを与える

                    if self.player is not None:  # 自機が存在する時
                        self.player.sound_timer = 5  # 弾発射音を止める時間を設定する

        # 敵の弾を更新する
        for bullet in self.enemy_bullets.copy():
            bullet.update()

            # プレイヤーと敵の弾の当たり判定を行う
            if self.player is not None and check_collision(self.player, bullet):
                bullet.add_damage()  # 敵の弾にダメージを与える
                self.player.add_damage()  # 自機にダメージを与える

        # 爆発エフェクトを更新する
        for blast in self.blasts.copy():
            blast.update()

        # シーンを更新する
        if self.scene == Game.SCENE_TITLE:  # タイトル画面
            if pyxel.btnp(pyxel.KEY_RETURN):
                pyxel.stop()  # BGMの再生を止める
                self.change_scene(Game.SCENE_PLAY)

        elif self.scene == Game.SCENE_PLAY:  # プレイ画面
            self.play_time += 1  # プレイ時間をカウントする
            self.level = self.play_time // 450 + 1
            # 15秒(毎秒30フレームx15)毎に難易度を1上げる

            # 敵を出現させる
            spawn_interval = max(60 - self.level * 10, 10)
            if self.play_time % spawn_interval == 0:
                kind = pyxel.rndi(Enemy.KIND_A, Enemy.KIND_C)
                Enemy(self, kind, self.level, pyxel.rndi(0, 112), -8)

        elif self.scene == Game.SCENE_GAMEOVER:  # ゲームオーバー画面
            if self.display_timer > 0:  # 画面表示時間が残っている時
                self.display_timer -= 1
            else:  # 画面表示時間が0になった時
                self.change_scene(Game.SCENE_TITLE)

    # ゲーム全体を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)

        # 背景を描画する
        self.background.draw()

        # 自機を描画する
        if self.player is not None:
            self.player.draw()

        # 敵を描画する
        for enemy in self.enemies:
            enemy.draw()

        # 自機の弾を描画する
        for bullet in self.player_bullets:
            bullet.draw()

        # 敵の弾を描画する
        for bullet in self.enemy_bullets:
            bullet.draw()

        # 爆発エフェクトを描画する
        for blast in self.blasts:
            blast.draw()

        # スコアを描画する
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

        # シーンを描画する
        if self.scene == Game.SCENE_TITLE:  # タイトル画面
            pyxel.blt(0, 18, 2, 0, 0, 120, 120, 15)
            pyxel.text(31, 148, "- PRESS ENTER -", 6)

        elif self.scene == Game.SCENE_GAMEOVER:  # ゲームオーバー画面
            pyxel.text(43, 78, "GAME OVER", 8)



#====================================================== 
# メイン処理
#====================================================== 
#〇MMPを実体化する。
objMMP = MultiMultiPlexer.MMP(
    argAnaPins      = 3,        # ボードのアナログPin数 
    argMpxPins      = 1,        # MultiPlexerのアナログPin数
    argAdrOutPin    = [2,3,6,7]         # THC4067アドレス指定Pin
    )

# ゲームを生成して開始する
Game()
