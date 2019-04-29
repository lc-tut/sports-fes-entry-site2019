import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Header from './Header'
import Footer from './Footer'
//import Team from './Team' これいる？

class Home extends Component {
  render() {
    return (
      <div>
        <Header />
        <div className="toppage_text">
          <p>体育会では、スポーツ大会の参加者を募集中です。<br />
            普段から体を動かしたいと思っている方、自分の体力を試すチャンスです。<br />
            日頃運動をしない方も、これを機にスポーツを楽しんでみませんか？<br />
            さぁ、すがすがしい初夏の風を感じながら、健康的に汗を流しましょう！</p>
          <div className="toppage_link">
            <Link to="/qanda">Q&A</Link>
            {/*<Team />*/}
          </div>
        </div>
        <div className="toppage_button"><Link to="/entry">エントリー</Link></div>
        <Footer />
      </div>
    )
  }
}

export default Home;