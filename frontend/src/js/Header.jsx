import React from "react";
import { Component } from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

class Header extends Component {
  render() {
    return (
      <div>
        <div id="back_blur"></div>
        <Link to="/"><img className="top" src="supotai@2x.png"></img></Link>
      </div>
    )
  }
}

export default Header;