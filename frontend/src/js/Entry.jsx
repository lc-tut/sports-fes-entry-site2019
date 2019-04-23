import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Esign from "./Esign";

class Entry extends Component {
  constructor(props) {
    super(props);
    this.state={
        isHide: "hide",
    };
  }
  onClick= () => {
    if(this.state.isHide==="hide"){
      this.setState({isHide:""});
    }
    else{
      this.setState({isHide:"hide"});
    }
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
                  <img src="supotai@2x.png"></img>
                </div>
                <div className="entrySectionMiddleText">
                  <h3>▼Event特集</h3>
                  <Link to="/">東京工科大学スポーツ大会</Link>
                </div>
              </div>
            </section>
            <h2>競技一覧</h2>
            <section className="entrySection pinkline">
              <div className="entrySectionContent">
                <div>
                  <h3>サッカー<br />2019.5.25(土)</h3>
                  <p className="entrySectionContentText">開演99:99~</p>
                  <p className="entrySectionContentLink">サッカーコート</p>
                </div>
              </div>
              <div className="entrySectionDetail">
                <a onClick={this.onClick}>詳細情報</a>
                <div className={this.state.isHide}>
                  <hr />
                  <h4>ほげ</h4>
                  <p>ほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげ</p>
                </div>
              </div>
            </section>
            <section className="entrySection">
              <div className="entrySectionContent">
                <div>
                  <div className="flex">
                    <div className="pinksymbol"></div>
                    <div>
                      <div className="category"><span>抽選</span>Web先行申し込み</div>
                      <div className="entrySectionContentText">受付期間:2019.4.13(土)10:00～2019.5.9(木)23:59</div>
                    </div>
                  </div>
                </div>
                <div className="entryButton">
                  <Link to="/submit">申し込む</Link>
                </div>
              </div>
            </section>
            <section className="entrySection">
              <div className="entrySectionContent">
                <div>
                  <div className="flex">
                    <div className="pinksymbol"></div>
                    <div>
                      <div className="category"><span>先着</span>一般申し込み</div>
                      <div className="entrySectionContentText">受付期間:2019.4.13(土)10:00～2019.5.9(木)23:59</div>
                    </div>
                  </div>
                </div>
                <div className="entryButton">
                  <Link to="/submit">申し込む</Link>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    )
  }
}
export default Entry;