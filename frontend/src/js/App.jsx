import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

function BasicExample() {
  return (
    <Router>
      <div>
        <Link to="/"><img className="top" src="supotai@2x.png"></img></Link>
        <Route exact path="/" component={Home} />
        <Route path="/about" component={About} />
        <Route path="/qanda" component={QandA} />
        <Route path="/topics" component={Topics} />
        <footer>
          <div>
            <p><Link to="/about">お問い合わせ</Link> </p>
            <p>(c)LinuxClub</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <div className="toppage_text">
        <p>体育会では、スポーツ大会の参加者を募集中です。<br />
          普段から体を動かしたいと思っている方、自分の体力を試すチャンスです。<br />
          日頃運動をしない方も、これを機にスポーツを楽しんでみませんか？<br />
          さぁ、すがすがしい初夏の風を感じながら、健康的に汗を流しましょう！</p>
        <div className="toppage_link">
          <Link to="/about">科目一覧を見る</Link>
          <Link to="/qanda">Q&A</Link>
        </div>
      </div>
      <div className="toppage_button"><Link to="/about">エントリー</Link></div>
    </div>
  );
}

function About() {
  return (
    <div>
      <h2>About</h2>
    </div>
  );
}
function QandA() {
  return (
    <div>
      <h2>Q&A</h2>
    </div>
  );
}
function Topics({ match }) {
  return (
    <div>
      <h2>Topics</h2>
      <ul>
        <li>
          <Link to={`${match.url}/rendering`}>Rendering with React</Link>
        </li>
        <li>
          <Link to={`${match.url}/components`}>Components</Link>
        </li>
        <li>
          <Link to={`${match.url}/props-v-state`}>Props v. State</Link>
        </li>
      </ul>

      <Route path={`${match.path}/:topicId`} component={Topic} />
      <Route
        exact
        path={match.path}
        render={() => <h3>Please select a topic.</h3>}
      />
    </div>
  );
}

function Topic({ match }) {
  return (
    <div>
      <h3>{match.params.topicId}</h3>
    </div>
  );
}

export default BasicExample;
