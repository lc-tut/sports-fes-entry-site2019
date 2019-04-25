import React from "react";
import { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Home from './Home';
import QandA from './QandA';
import Contact from './Contact';
import Entry from './Entry';
import Submit from './Submit';
import ScrollToTop from './ScrollToTop';

class App extends Component {
  render() {
    return (
      <Router>
        <ScrollToTop><Route exact path="/" component={Home} /></ScrollToTop>
        <ScrollToTop><Route path="/qanda" component={QandA} /></ScrollToTop>
        <ScrollToTop><Route path="/contact" component={Contact} /></ScrollToTop>
        <ScrollToTop><Route path="/entry" component={Entry} /></ScrollToTop>
        <ScrollToTop><Route path="/submit" component={Submit} /> </ScrollToTop>
      </Router>
    );
  }
}

export default App;
