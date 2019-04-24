import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Esign from "./Esign";
import Login from "./Login";

class Entry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogin: false,
      name:""
    };
  }
  onClick = () => {
    console.log(this.state);
    console.dir(this.props);
  }
  loginCallback=(data)=>{
    this.setState({isLogin:true});
    if(!data.mail.match(/@edu.teu.ac.jp/)) alert("大学のアドレスでログインしてください");
    console.log(data)
    this.setState({name:data.name})
  }
  logoutCallback=()=>{
    this.setState({isLogin:false});
    console.log("logouted");
  }
  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
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
                    <h3>参加する競技を選んでください</h3>
                    <a onClick={this.onClick}>test</a>
                    <input type="text" value={this.state.name } name="name" onChange={this.handleChange} />
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