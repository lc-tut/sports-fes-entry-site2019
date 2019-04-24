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
          <p>下記のメールまたはフォームから送信してください</p>
          <h3>メール</h3>
          <p>linuxclub.tut@gmail.com</p>
          <h3>GoogleForm</h3>
          <p>urlはまだない</p>
          <p className="aboutTextLink"><Link to="/">戻る</Link></p>
        </div>
        <Footer />
      </div>
    )
  }
}

export default Contact;