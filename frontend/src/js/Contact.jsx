import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Header from './Header'
import Footer from './Footer'

class Contact extends Component {
  render() {
    return (
      <div>
        <Header />
        <div className="aboutText">
          <h2>お問い合わせ</h2>
          <h3>お問い合わせの前に</h3>
          <p>画面をよく見ましたか？<br />申込期間はチェックしましたか？<br />人数は正しいですか？<br />最新のブラウザを使っていますか？<br />学籍番号は正しいですか？<br /><br />以上を再確認の上お問い合わせください</p><br />
          <p>下記のフォームから送信してください</p>
          <h3><a href="https://docs.google.com/forms/d/e/1FAIpQLScrBozdonGuydLeo-xkV8rQVrrSu_y-Lf-opbt2sNHp2IVGNQ/viewform?usp=sf_link">GoogleForm</a></h3>
          <p className="aboutTextLink"><Link to="/">戻る</Link></p>
        </div>
        <Footer />
      </div>
    )
  }
}

export default Contact;