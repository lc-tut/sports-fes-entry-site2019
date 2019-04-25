import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Esign from "./Esign";
import Login from "./Login";
import Team from './Team';

class Entry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogin: false,
      teamName:"",
      name: "",
      mail: "",
      experience: false,
      drawing: false,
      program: "soccer",
      programJP: "サッカー"
    };
  }
  onClick = () => {
    console.log(this.state);
    console.dir(this.props);
  }
  loginCallback = (data) => {
    this.setState({ isLogin: true });
    if (!data.mail.match(/@edu.teu.ac.jp/)) alert("大学のアドレスでログインしてください");
    console.log(this.props)
    this.setState({ name: data.name, mail: data.mail })
    const url = this.props.location.pathname;
    console.log(url)
    if (url.match(/drawing/)) {
      //先行申し込み
      this.setState({ drawing: true });
    }
    else {
      //一般申込み
      this.setState({ drawing: false });
    }
    if (url.match(/soccer/)) {
      this.setState({ program: "soccer", programJP: "サッカー" });
    }
    else if (url.match(/tennis/)) {
      this.setState({ program: "tennis", programJP: "テニス" });
    }
    else if (url.match(/basketball/)) {
      this.setState({ program: "basketball", programJP: "バスケットボール" });
    }
    else if (url.match(/badminton/)) {
      this.setState({ program: "badminton", programJP: "バドミントン" });
    }
    else if (url.match(/volleyball/)) {
      this.setState({ program: "volleyball", programJP: "バレーボール" });
    }
    else {
      this.setState({ program: "tabletennis", programJP: "卓球" });
    }
    console.log(this.state);
  }
  logoutCallback = () => {
    this.setState({ isLogin: false });
    console.log("logouted");
  }
  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value })
  }
  render() {
    return (
      <div>
        <Esign />
        <div className="entry">
          <div className="entryChild">
            <br />
            <section className="entrySection pinkline">
              <div className="entrySectionContent">
                <div className="submitPage">
                  <h3>大学のGmailでログインしてください</h3>
                  <Login callback={this.loginCallback} pushLogout={this.logoutCallback} />
                  {//このしたはログイン後表示
                  }
                  <div className={this.state.isLogin ? "" : "hide"}>
                    <h3>申し込み種別</h3>
                    <p>{(this.state.drawing ? "【抽選】Web先行：" : "【先着】一般申込：") + this.state.programJP}</p>
                    <form>
                      <h2>チーム名</h2>
                      <input className="form" type="text" value={this.state.teamName} name="teamName" onChange={this.handleChange} />
                      <h2>代表(登録者)情報</h2>
                      <h3>名前</h3>
                      <input className="form" type="text" value={this.state.name} name="name" onChange={this.handleChange} />
                      <h3>メール</h3>
                      <input className="form" type="text" value={this.state.mail} name="mail" onChange={this.handleChange} />
                      <h3>競技経験がある場合チェック</h3>
                      <input className="form" type="checkbox" value={this.state.experience} name="experience" onChange={this.handleChange} />
                    </form>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
        <Team />
      </div>
    )
  }
}
export default Entry;