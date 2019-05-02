import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Header from './Header'
import Footer from './Footer'

class QandA extends Component {
  render() {
    return (
      <div>
        <Header />
        <div className="aboutText">
          <h2>Q&A</h2>
          <h3>これはなんのサイトですか</h3>
          <p>スポーツ大会の登録サイトです</p>
          <h3>なぜ背景がいらすとやなんですか？</h3>
          <p>お察しください</p>
          <h3>誰が運用しているんですか</h3>
          <p>サイトの開発・運用は東京工科大学公認サークル「LinuxClub」が行っております</p>
          <h3>デザインがダサいんですが</h3>
          <p>デザイン学部のそこの君！LinuxClubではそんなあなたの入部を待っているぞ！</p>
          <h3>エントリーの仕方がわかりません</h3>
          <p>お問い合わせページからお問い合わせしてください</p>
          <h3>ページが正常に表示されません</h3>
          <p>最新のブラウザをご利用ください</p>
          <p className="aboutTextLink"><Link to="/">戻る</Link></p>
        </div>
        <Footer />
      </div>
    )
  }
}

export default QandA;