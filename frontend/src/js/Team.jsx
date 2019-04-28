import React from "react";
import { Component } from 'react';


class Team extends Component {

    getCookie = (name) => {
        const value = "; " + document.cookie;
        const parts = value.split("; " + name + "=");
        console.log(parts);
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

    fetchTeamData = () => {
        return fetch('http://localhost:8080/teams/', {
            method: 'GET',
            credentials: "include",
        }).then((response) => {
            return response.json();
        }).then((json) => {
            console.log(json);
        })
    }

    postTeamData = () => {
        const body = {
            "name": "test",
            "event": "Tennis",
            "leader": {
                "name": "hako",
                "email": "c011822457@edu.teu.ac.jp",
                "experience": false
            },
            "members": [
                {
                    "name": "hakomori",
                    "email": "c011822457@edu.teu.ac.jp",
                    "experience": true
                }
            ]
        }
        return fetch('http://localhost:8080/teams/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            },
            body: JSON.stringify(body),
            credentials: 'include',
        }).then((response) => {
            return response.json()
        }).then((json) => {
            console.log(json);
        })
    }

    componentDidMount() {
        this.fetchTeamData();
        this.postTeamData();
    }
    
    render() {
      return (
          <div>はろー</div>
      );
    }
}

export default Team;
