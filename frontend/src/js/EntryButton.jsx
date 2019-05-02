import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

class EntryButton extends Component {
  render() {
    return (
      <div>
        <section className="entrySection">
          <div className="entrySectionContent">
            <div>
              <div className="flex">
                <div className="pinksymbol"></div>
                <div>
                  <div className="category"><span>抽選</span>Web先行申し込み</div>
                  <div className="entrySectionContentText">受付期間:2019.4.13(土)10:00～2019.5.9(木)23:59</div>
                </div>
              </div>
            </div>
            <div className="entryButton">
              <Link to={"/submit/"+this.props.program+"/drawing/"}>申し込む</Link>
            </div>
          </div>
        </section>
        <section className="entrySection">
          <div className="entrySectionContent">
            <div>
              <div className="flex">
                <div className="pinksymbol"></div>
                <div>
                  <div className="category"><span>先着</span>一般申し込み</div>
                  <div className="entrySectionContentText">受付期間:2019.4.13(土)10:00～2019.5.9(木)23:59</div>
                </div>
              </div>
            </div>
            <div className="entryButton">
              <Link to={"/submit/"+this.props.program+"/general/"}>申し込む</Link>
            </div>
          </div>
        </section>
      </div>
    )
  }
}
export default EntryButton;