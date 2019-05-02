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
          <p>下記のフォームから送信してください</p>
          <h3>GoogleForm</h3>
          <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScrBozdonGuydLeo-xkV8rQVrrSu_y-Lf-opbt2sNHp2IVGNQ/viewform?embedded=true" width="640" height="944" frameborder="0" marginheight="0" marginwidth="0">読み込んでいます...</iframe>
          <p className="aboutTextLink"><Link to="/">戻る</Link></p>
        </div>
        <Footer />
      </div>
    )
  }
}

export default Contact;