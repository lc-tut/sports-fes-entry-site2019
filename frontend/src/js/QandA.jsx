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
          <p>見ればわかる</p>
          <h3>なぜ背景がいらすとやなんですか？</h3>
          <p>写真部が再三の催促を無視して写真を提出しなかったためです</p>
          <h3>なぜデザインが薬キメてるみたいなんですか？</h3>
          <p>そもそも無償の仕事に責任なんてないし、デザイナーもいない</p>
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