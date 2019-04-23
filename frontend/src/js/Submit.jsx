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
    };
  }
  onClick = () => {
    console.log(this.state);
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
                  <Login />
                  {//このしたはログイン後表示
                  }
                  <h3>参加する競技を選んでください</h3>
                  <a onClick={this.onClick}>test</a>
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