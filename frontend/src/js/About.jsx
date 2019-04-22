import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Header from './Header'
import Footer from './Footer'

class About extends Component {
  render() {
    return (
      <div>
        <Header />
        <div className="aboutText">
          <h2>開催概要</h2>
          <p>テキストサンプルほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげ</p>
          <h3>サッカー</h3>
          <p>テキストサンプルほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげ</p>
          <h3>バスケットボール</h3>
          <p>テキストサンプルほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげほげ</p>
          <p className="aboutTextLink"><Link to="/">戻る</Link></p>
        </div>
        <Footer />
      </div>
    )
  }
}

export default About;