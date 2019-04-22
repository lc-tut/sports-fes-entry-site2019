import React from "react";
import { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Home from './Home';
import About from './About';
import QandA from './QandA';
import Contact from './Contact';
import Entry from './Entry';

class App extends Component {
  render() {
    return (
      <Router>
        <Route exact path="/" component={Home} />
        <Route path="/about" component={About} />
        <Route path="/qanda" component={QandA} />
        <Route path="/contact" component={Contact} />
        <Route path="/entry" component={Entry} />
      </Router>
    );
  }
}

export default App;
