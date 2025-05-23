#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER6:MAGA WING
#┠─────────────────────────────────────
#┃処理（ゲーム本体）
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
import main.DB
from   シーン    import *
from   背景	     import 背景作成
from   .更新処理 import 更新処理
from   .描画処理 import 描画処理

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃メイン
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class 本体:
    #┌───────────────────────────────────
    #│初期化
    #└───────────────────────────────────
    def __init__(self):
        #┬
        #○Pyxel(画面/音楽)を初期化する
        self.初期化_リソース()
        #│
        #〇処理で用いる各種オブジェクトを作成する
        self.初期化_処理セット()
        #│
        #≫シーンを『終了画面』に進行する
        main.DB.FNシーン[ シーンID.終了画面 ].FN移動.Fn次シーン準備()
        #│
        #○フレーム処理に、処理セットを登録する
        pyxel.run(self.FN更新処理.実行, self.FN描画処理.実行)
        #┴
	#────────────────────────────────────	
    def 初期化_リソース(self):
        #┬
        #○画面を初期化する
        pyxel.init(120, 160, title="Mega Wing  Ver.2025/05/03-02")
        #│
        #○リソースファイルを読み込む
        pyxel.load("../リソース/改造版.pyxres")
        #│
        #○Soundデータを登録する
        pyxel.sounds[50].mml(
                "t100 @1 o2 q7 v7 l4" +
                "l8d4a4g2.fed4c<b->c<a>e4d1.a4>" +
                "c4<b2.gfe4fga1&a1d4a4g2.fed4c<b->c<a>e4d1." )
        pyxel.sounds[51].mml(
                "t100 @0 o1 q7 v4 l2" +
                "l8dafadbgbd>c<a>c<db-fb-e>c<a>c" +
                "<daf+adaf+agb-a>c" +
                "<dafadbgbdbgbdb-g+b-c" +
                "+aeadaeac+aea<b>ac+adafadbgbd>c" +
                "<a>c<db-fb-e>c<a>c<daf+adaf+adaf+a" )
        #│
        #○Musicデータを登録する
        pyxel.musics[7].set([50],[51])
        #┴
	#────────────────────────────────────	
    def 初期化_処理セット(self):
        #┬
        #≫更新処理をオブジェクト化する
        self.FN更新処理 = 更新処理()
        #│
        #≫描画処理をオブジェクト化する
        self.FN描画処理 = 描画処理()
        #│
        #≫シーンをオブジェクト化する
        main.DB.objシーン = {
            シーンID.タイトル画面   : タイトル画面(),
            シーンID.プレイ画面     : プレイ画面()  ,
            シーンID.終了画面       : 終了画面()    }
        #│
        #≫背景をオブジェクト化する
        main.DB.obj背景 = 背景作成()
        #┴