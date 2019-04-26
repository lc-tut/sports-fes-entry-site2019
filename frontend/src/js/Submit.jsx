import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Esign from "./Esign";
import Login from "./Login";
import config from "./config.json";

class Entry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogin: false,
      teamName: "",
      name: "",
      mail: "",
      experience: false,
      drawing: false,
      program: "soccer",
      programJP: "サッカー",
      feed: {
        entry: [
          {
            member: []
          }
        ]
      },
      name_ok: true,
      mail_ok: true,
      form_ok: false
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
    this.setState({ [event.target.name]: event.target.type === "checkbox" ? event.target.checked : event.target.value })
  }
  formHandleChange = (event) => {
    let name_ok = this.state.name_ok;
    let mail_ok = this.state.mail_ok;
    const member_copy = this.state.feed.entry[0].member.slice();
    console.log(event.target);
    console.log(member_copy);
    //名前欄が空でなければ緑で表示
    if (event.target.name.match(/name.*/)) {
      if (event.target.value !== "") {
        event.target.className = "form studentNumber_ok";
        this.setState({ name_ok: true })
        name_ok=true;
      }
      else {
        event.target.className = "form studentNumber_ng";
        this.setState({ name_ok: false })
        name_ok=false;
      }
    }
    //学籍番号が正しければ緑で表示
    if (event.target.name.match(/mail.*/)) {
      const regexp = new RegExp(/^[bcemhg][0-9]{7}$/i);
      if (event.target.value.match(regexp)) {
        event.target.className = "form studentNumber_ok";
        this.setState({ mail_ok: true })
        mail_ok=true;
      }
      else {
        event.target.className = "form studentNumber_ng";
        this.setState({ mail_ok: false })
        mail_ok=false;
      }
    }
    //メンバー人数を見て登録ボタンを有効化
    //有効の場合は追加ボタンは無効化
    const member_value = config.program[this.state.program];
    const now_members = this.state.feed.entry[0].member.length;
    if(name_ok&&mail_ok&&member_value.min_member<=now_members&&member_value.max_member>=now_members){
      this.setState({ form_ok: true });
    }
    else{
      this.setState({ form_ok: false });
    }
    const key = event.target.name.replace(/.*_/, "");
    console.log(key);
    //checkboxならvalueじゃない方を返す
    member_copy[key][event.target.name.replace(/_.*/, "")] = event.target.type === "checkbox" ? event.target.checked : event.target.value;
    const member_wrap = { member: member_copy };
    this.setState({
      feed: {
        entry: [
          member_wrap
        ]
      }
    });
    console.log(this.state);
  }
  addMember = () => {
    this.setState((prevState) => ({
      feed: ((prevState) => {
        if (!prevState.feed.entry[0].member) {
          prevState.feed.entry[0].member = []
        }
        prevState.feed.entry[0].member.push({ name: "", mail: "", experience: false })
        return prevState.feed
      })(prevState)
      ,
      name_ok: false,
      mail_ok: false
    }))
    console.log(this.state)
    //もし最大人数と一緒だったらボタンを無効化
  }
  MemberForm(key) {
    return (
      <form key={key.toString()}>
        <h3>名前</h3>
        <input className="form" type="text" value={this.state.feed.entry[0].member[key].name} name={"name_" + key} onChange={(e, key) => this.formHandleChange(e, key)} />
        <h3>学籍番号</h3>
        <input className="form" maxlength="8" type="text" value={this.state.feed.entry[0].member[key].mail} name={"mail_" + key} onChange={(e, key) => this.formHandleChange(e, key)} />
        <h3>競技経験がある場合チェック</h3>
        <input className="form" type="checkbox" checked={this.state.feed.entry[0].member[key].experience} name={"experience_" + key} onChange={(e, key) => this.formHandleChange(e, key)} />
      </form>
    )
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
                  {/*このしたはログイン後表示*/}
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
                      <p>{this.state.mail}</p>
                      <h3>競技経験がある場合チェック</h3>
                      <input className="form" type="checkbox" value={this.state.experience} name="experience" onChange={this.handleChange} />
                    </form>
                    <h2>メンバー</h2>
                    {this.state.feed.entry &&
                      this.state.feed.entry[0].member &&
                      this.state.feed.entry[0].member.map((row, key) => this.MemberForm(key))}
                    <div className={"entryButton " + ((this.state.name_ok && this.state.mail_ok)&&!this.state.form_ok ? "" : "entryButton_disable")}><a onClick={this.addMember}>メンバーを追加</a></div>
                    <br />
                    <div className={"entryButton " + (this.state.form_ok ? "" : "entryButton_disable")}><a onClick={this.onClick}>登録</a></div>
                  </div>
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