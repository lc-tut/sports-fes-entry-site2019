import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Esign from "./Esign";
import EntryButton from "./EntryButton";
import config from "./config.json";

class Entry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isHide1: true,
      isHide2: true,
      isHide3: true,
      isHide4: true,
      isHide5: true,
      isHide6: true,
      registerable: {}
    };
  }
  componentWillMount = () => {
    fetch(config.url + 'registerable/', {
      method: 'GET',
      credentials: "include",
    }).then((response) => {
      return response.json();
    }).then((json) => {
      //console.log(json);
      this.setState({ registerable: json });
    })
  }
  detailChange = (event) => {
    this.setState({ [event.target.name]: !this.state[event.target.name] });
  }
  render() {
    return (
      <div>
        <Esign />
        <div className="entry">
          <div className="entryChild">
            <h1>【5/25公演】&lt;東京工科大学&gt;2019年度スポーツ大会のエントリー情報</h1>
            <p>【5/25公演】&lt;東京工科大学&gt;2019年度スポーツ大会のエントリー情報ページです。日程、会場情報を確認し、簡単オンラインエントリーができます。</p>
            <section className="entrySection">
              <div className="entrySectionContent">
                <div className="entrySectionImage">
                  <img src="/supotai@2x.png"></img>
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
                    <h3>サッカー<br />2019.5.25(土)</h3>
                    <p className="entrySectionContentText">10:00～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：総合グラウンド</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a name="isHide1" onClick={this.detailChange}>詳細情報</a>
                  <div className={this.state.isHide1 ? "hide" : ""}>
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
              <EntryButton registerable={this.state.registerable} program="Soccer" />
            </div>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>テニス<br />2019.5.25(土)</h3>
                    <p className="entrySectionContentText">10:00～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：テニスコート</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a name="isHide2" onClick={this.detailChange}>詳細情報</a>
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
              <EntryButton registerable={this.state.registerable} program="Tennis" />
            </div>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>バスケットボール<br />2019.5.25(土)</h3>
                    <p className="entrySectionContentText">9:30～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：体育館</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a name="isHide3" onClick={this.detailChange}>詳細情報</a>
                  <div className={this.state.isHide3 ? "hide" : ""}>
                    <hr />
                    <h4>ルール</h4>
                    <p>
                      人数：1チーム5〜10人(男女混合可)<br />
                      試合時間：予選リーグ…5分2ピリオド(インターバル1分)<br />
                      決勝トーナメント…6分2ピリオド(インターバル2分)<br />
                      タイムアウトは1試合1回、1分間とする。<br />
                      延長戦は決勝トーナメントのみ行う。<br />
                      女子の得点は倍とする。<br />
                      ボールは7号球を使用する。<br />
                      審判及びタイマー等はサークルメンバー(XIIMJ)で行う。<br />
                      試合開始時間に来なかったチームは不戦敗とする。<br />
                    </p>
                  </div>
                </div>
              </section>
              <EntryButton registerable={this.state.registerable} program="BasketBall" />
            </div>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>バドミントン<br />2019.5.25(土)</h3>
                    <p className="entrySectionContentText">10:00～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：体育館（アリーナ）</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a name="isHide4" onClick={this.detailChange}>詳細情報</a>
                  <div className={this.state.isHide4 ? "hide" : ""}>
                    <hr />
                    <h4>ルール</h4>
                    <p>各試合21点3ゲーム（2ゲーム先取）で行う<br />
                      人数：1チーム2人（男女混合可）<br />
                      試合形式：リーグ戦<br />
                      予選リーグ・・・各ブロック内で総当たり戦を行い、各ブロックの1位を決める<br />
                      決勝リーグ・・・各ブロックの1位のチームで総当たり戦を行い、全体の1位、2位、3位を決める<br />
                      持ち物：学生証、ラケット（持っている方のみ）、運動着、運動靴（屋内用）<br />
                      <br />
                      以下のサークルの人は各チーム1人までとします<br />
                      バドミントン部、アミーゴ　※バドミントン部の人とアミーゴの人のペアは不可<br />
                      <br />
                      未経験者一人につき6点のハンディキャップ　(例:未経験者2人のチームの場合12点からスタート)<br />
                      男女混合で試合を行いますが、男女間でのハンデは今回はなしとします<br />

                    </p>
                  </div>
                </div>
              </section>
              <EntryButton registerable={this.state.registerable} program="Badminton" />
            </div>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>バレーボール<br />2019.5.25(土)</h3>
                    <p className="entrySectionContentText">10:00～17:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：体育館</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a name="isHide5" onClick={this.detailChange}>詳細情報</a>
                  <div className={this.state.isHide5 ? "hide" : ""}>
                    <hr />
                    <h4>ルール</h4>
                    <p>人数：６人制（1チーム８人まで）<br />
                      試合時間：トーナメント制で行う。１試合３０分を考えており試合間は５分間とる。<br />
                      持ち物：学生証、運動着、運動靴<br />
                      使用ボールはモルテンとする。<br />
                      参加チームの経験者制限はなし。<br />
                      すべての試合を２５点マッチで行う。（デュースあり）<br />
                      ネットの高さは２ｍ３５ｃｍ。<br />
                      基本的なバレーボールのルールに従って行うが初心者も混ざっているため厳しくは取らない（決勝戦は除く）。

                    </p>
                  </div>
                </div>
              </section>
              <EntryButton registerable={this.state.registerable} program="VolleyBall" />
            </div>
            <div className="game">
              <section className="entrySection pinkline">
                <div className="entrySectionContent">
                  <div>
                    <h3>卓球<br />2019.5.25(土)</h3>
                    <p className="entrySectionContentText">10:00～14:00</p>
                    <p className="entrySectionContentLink">東京工科大学八王子キャンパス：体育館1階稽古場</p>
                  </div>
                </div>
                <div className="entrySectionDetail">
                  <a name="isHide6" onClick={this.detailChange}>詳細情報</a>
                  <div className={this.state.isHide6 ? "hide" : ""}>
                    <hr />
                    <h4>ルール</h4>
                    <p>人数：2人１組のダブルス<br />
                      経験者・未経験者混合　男女混合<br />
                      試合の方式：A～Fの6つのリーグに分けてリーグ戦を行う。その後、各リーグの1,2位で決勝トーナメントを行う。<br />
                      2セット先取3ゲームマッチで試合を行う。<br />

                    </p>
                  </div>
                </div>
              </section>
              <EntryButton registerable={this.state.registerable} program="TableTennis" />
            </div>
          </div>
        </div>
      </div>
    )
  }
}
export default Entry;