import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import config from "./config.json";

class EntryButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      drawing_time: false,
      hayaimonogachi_time: false,
      registerable: {}
    };
  }
  componentWillReceiveProps = (e) => {
    this.setState({ registerable: e.registerable });
    //console.log(e.registerable);
    //console.log(this.state.registerable[this.props.program]);
  }
  componentWillMount = () => {
    const now = new Date().getTime();
    const d_start = new Date(config.drawing_date_start).getTime();
    const d_end = new Date(config.drawing_date_end).getTime();
    const limit = new Date(config.submit_limmit).getTime();
    //console.log(`${now}/${d_start}/${d_end}/${limit}`)
    if (d_start < now && d_end > now) {
      this.setState({ drawing_time: true });
    }
    else if (d_end < now && now < limit) {
      this.setState({ hayaimonogachi_time: true });
    }
    else {
      //alert("申込期間外です");
      //this.props.history.push('/');
      //this.setState({ hayaimonogachi_time: true });
    }
  }
  render = () => {
    //console.log(this.props.program)
    //console.log(this.state.registerable[this.props.program]);
    return (
      <div>
        <section className="entrySection">
          <div className="entrySectionContent">
            <div>
              <div className="flex">
                <div className="pinksymbol"></div>
                <div>
                  <div className="category"><span>抽選</span>Web先行申し込み</div>
                  <div className="entrySectionContentText">受付期間:2019.5.6(月)10:00～2019.5.11(土)23:59</div>
                </div>
              </div>
            </div>
            <div className={"entryButton " + (this.state.drawing_time ? "" : "entryButton_disable")}>
              <Link to={"/submit/" + this.props.program + "/drawing/"}>{this.state.drawing_time ? "申込む" : "申込期間外"}</Link>
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
                  <div className="entrySectionContentText">受付期間:2019.5.11(土)00:00～2019.5.18(土)23:59</div>
                </div>
              </div>
            </div>
            <div className={"entryButton " + ((this.state.hayaimonogachi_time && this.state.registerable[this.props.program] === "true") ? "" : "entryButton_disable")}>
              <Link to={"/submit/" + this.props.program + "/general/"}>{this.state.hayaimonogachi_time ? this.state.registerable[this.props.program] === "true" ? "申込む" : "完売" : "申込期間外"}</Link>
            </div>
          </div>
        </section>
      </div>
    )
  }
}
export default EntryButton;