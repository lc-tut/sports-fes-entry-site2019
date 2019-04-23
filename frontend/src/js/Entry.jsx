import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Esign from "./Esign";
import EntryButton from "./EntryButton";

class Entry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isHide: "hide",
      isHide2: true,
      isHide3:true,
    };
  }
  onClick = () => {
    if (this.state.isHide === "hide") {
      this.setState({ isHide: "" });
    }
    else {
      this.setState({ isHide: "hide" });
    }
  }
  onClick2 = () => {
    this.setState({ isHide2: !this.state.isHide2 });
  }
  onClick3 = () => {
    this.setState({ isHide3: !this.state.isHide3 });
  }
  render() {
    return (
      <div>
        <Esign />
        <div className="entry">
          <div className="entryChild">
            <h1>【5/26公演】&lt;東京工科大学&gt;2019年度スポーツ大会のエントリー情報</h1>
            <p>【5/26公演】&lt;東京工科大学&gt;2019年度スポーツ大会のエントリー情報ページです。日程、会場情報を確認し、簡単オンラインエントリーができます。</p>
            <section className="entrySection">
              <div className="entrySectionContent">
                <div className="entrySectionImage">
                  <img src="supotai@2x.png"></img>
                </div>
                <div className="entrySectionMiddleText">
                  <h3>▼Event特集</h3>
                  <Link to="/">東京工科大学スポーツ大会</Link>
                </div>
              </div>
            </section>
            <h2>競技一覧</h2>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>サッカー<br />2019.5.26(土)</h3>
                    <p className="entrySectionContentText">10:00～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：総合グラウンド</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a onClick={this.onClick}>詳細情報</a>
                  <div className={this.state.isHide}>
                    <hr />
                    <h4>ルール</h4>
                    <p>人数：8人制（1チーム13人まで）<br />
                      試合時間：予選リーグ・・・7分ハーフ（ハーフタイム1分）<br />
                      決勝トーナメント・・・10分ハーフ（ハーフタイム2分）<br />
                      持ち物：学生証、運動着、運動靴（スパイク可）<br />
                      <br />
                      参加チームの経験者制限はありません<br />
                      決勝トーナメントのみ同点の場合はPK方式<br />
                      ボールは5号球を使用<br />
                      ボールがピッチ外に出たらスローインからリスタート<br />
                      オフサイドはなし<br />
                      選手交代は自由(ただしピッチ内にいる選手がピッチ外へ完全に出てから)
                  </p>
                  </div>
                </div>
              </section>
              <EntryButton />
            </div>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>テニス<br />2019.5.26(土)</h3>
                    <p className="entrySectionContentText">10:00～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：テニスコート</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a onClick={this.onClick2}>詳細情報</a>
                  <div className={this.state.isHide2 ? "hide" : ""}>
                    <hr />
                    <h4>ルール</h4>
                    <p>人数：2人のダブルスのみ（男女混合可）<br />
                      ゲーム数：予選リーグ・・・4ゲーム先取<br />
                      決勝トーナメント・・・6ゲーム先取<br />
                      持ち物：学生証、運動着、運動靴（テニスシューズ可）<br />
                      <br />
                      参加チームの経験者制限はありません<br />
                      ボールはSt.JAMESを使用<br />
                      審判はセルフジャッジ<br />
                      警告、退場は無し<br />
                      初心者、女子が含まれるチームには毎ゲーム15ポイントハンデを与える<br />
                      初心者、女子のみのペアは毎ゲーム15ポイントハンデと1ゲームのハンデを与える
                  </p>
                  </div>
                </div>
              </section>
              <EntryButton />
            </div>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>バスケットボール<br />2019.5.26(土)</h3>
                    <p className="entrySectionContentText">9:30～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：体育館</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a onClick={this.onClick3}>詳細情報</a>
                  <div className={this.state.isHide3 ? "hide" : ""}>
                    <hr />
                    <h4>ルール</h4>
                    <p>	バスケットボールは 15m×28m のコート中に各チームプレイヤー5 人ずつ <br />
                      	相手チームが防御するリングにシュートを入れ得点し、また逆に相手チームが得点す る事を防御し得点を競合うゲームである。 <br />
                      	試合は６分の１ピリオドを２回行う。 <br />
                      	第 1・2 ピリオドの間に 2 分間のインターバル<br />
                      	普通のシュートは 2 点、3P ライン外側からのシュートは 3 点である。<br />
                      	女子の得点は二倍とする。<br />
                      	ファウル(スコア上記録される反則)、バイオレーション(スコア上記録されない反則)、 タイムアウト、は時間が止められ、次のプレイが始まると同時にスタートされる。<br />
                      	またボールは手で扱い、ボールを持ったまま 3 歩以上歩けない(トラベリング)、ドリブルを止めて一度手に持ったボールを再びドリブルすることは出来ない(ダブルドリブル)がある。 <br />
                      	ボールは7号球を使用する。<br />
                      	審判およびタイマーなどはサークルメンバーで行う。 <br />
                      	試合開始時間に来なかったチームは不戦敗とする。<br />
                      時間制限ルール<br />
                      	24 秒ルール：ボールを保持してから 24 秒以内にシュートを打たなければいけない。 <br />
                      	8 秒ルール：オフェンスは 8 秒以内にバックコート(相手チームゴール)から、フロントコート(自チームゴール)へボールを運ばなければならない。 <br />
                      	5 秒ルール：オフェンスはサイドライン、エンドラインからのスローインを 5 秒以内にしなければならない。またボールを持ったプレイヤーがパスもドリブルもしないで、5 秒以上ボールを保持してはならない。 <br />
                      	3 秒ルール：オフェンスは自チームゴールのフリースローレーン(制限区域内)の中に 3 秒以上いてはならない(チームがアライブのボールを保持している時)。<br />
                      	タイムアウト：各ピリオド毎にそれぞれ 1 分間のタイムアウトを請求できる。但し第 4 ピリオドは 2 回。延長戦は 1 回の延長につき、 1 回のタイムアウトを請求できる。<br />
                      	なお、延長は 3 分、１ピリで行う。 <br />
                      反則 <br />
                      	記録されない反則：バイオレーション(ダブルドリブル、トラベリング、オーバータイ ム等) 記録される反則：ファウルは 5 回で退場になる。またシュートに対するファウルは、シュートが入れば二点が入り、なおかつ自分たちボール、入らなければ二点が入り相手ボールでスタート。原則的にその他のファウルはサイドライン、エンドラインからのスローインになるが、各ピリオド毎にチームファウルが 4 個以上になった場合、5 個目からはシュートモーション以外のファウルでも 2 点が与えられる。延長の時は第 4 ピリオドに起こったものとみなす。<br />
                      選手交代<br />
                      	選手交代は退場していない各プレイヤーが何回でも行うことが出来る。<br />

                    </p>
                  </div>
                </div>
              </section>
              <EntryButton />
            </div>
          </div>
        </div>
      </div>
    )
  }
}
export default Entry;