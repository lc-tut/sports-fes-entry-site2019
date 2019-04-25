import React from "react";
import { Component } from 'react';


class Team extends Component {

    fetchTeamData = () => {
        return fetch('http://localhost:8080/teams', {
            method: 'GET',
            credentials: "include",
        }).then((response) => {
            return response.json();
        }).then((json) => {
            console.log(json);
        })
    }

    componentDidMount() {
        this.fetchTeamData();
    }
    
    render() {
      return (
          <div>はろー</div>
      );
    }
}

export default Team;
