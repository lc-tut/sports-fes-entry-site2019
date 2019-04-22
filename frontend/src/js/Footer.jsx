import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

class Footer extends Component {
  render() {
    return (
      <footer>
      <div>
        <p><Link to="/contact">お問い合わせ</Link> </p>
        <p>(c)LinuxClub</p>
      </div>
    </footer>
    )
  }
}

export default Footer;