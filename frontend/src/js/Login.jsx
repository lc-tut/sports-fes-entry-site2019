import React from "react";
import { Component } from 'react';
import config from "./config.json";

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLogin: false,
        };
    }
    componentDidMount() {
        this.downloadGoogleScript(this.initSignInButton)
    }

    downloadGoogleScript = (callback) => {
        const element = document.getElementsByTagName('script')[0];
        const js = document.createElement('script');
        js.id = 'google-platform';
        js.src = '//apis.google.com/js/platform.js';
        js.async = true;
        js.defer = true;
        element.parentNode.insertBefore(js, element);
        js.onload = () => callback(window.gapi);
    }

    initSignInButton = (gapi) => {
        gapi.load('auth2', () => {
            gapi.auth2.init({ client_id: config.config_cliient_id })
                .then(
                    (result) => {
                        gapi.signin2.render('google-signin-button', {
                            'onsuccess': this.onSignin,
                            'onfailure': (err) => console.error(err)
                        });
                    },
                    (err) => console.error(err)
                );
        });
    }

    getCookie = (name) => {
        const value = "; " + document.cookie;
        const parts = value.split("; " + name + "=");
        //console.log(parts);
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

    signOut = () => {
        const auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(() => {
            //console.log('User signed out.');
            this.setState({ isLogin: false });
            //console.log(this.state);
            this.props.pushLogout();
        });

        auth2.disconnect();

        fetch(config.url + 'tokenlogout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCookie('csrftoken'),
            },
            credentials: 'include',
        }).then((response) => {
            return response.text()
        }).then((text) => {
            //console.log(text);
        })
    }

    onSignin = (googleUser) => {
        const profile = googleUser.getBasicProfile();
        /*console.log("ID: " + profile.getId()); // Don't send this directly to your server!
        console.log('Full Name: ' + profile.getName());
        console.log('Given Name: ' + profile.getGivenName());
        console.log('Family Name: ' + profile.getFamilyName());
        console.log("Image URL: " + profile.getImageUrl());
        console.log("Email: " + profile.getEmail());*/
        this.props.callback({
            "name": profile.getName(),
            "mail": profile.getEmail()
        });
        this.setState({ isLogin: true });
        // The ID token you need to pass to your backend:
        const id_token = googleUser.getAuthResponse().id_token;
        const csrftoken = this.getCookie('csrftoken');
        //console.log("ID Token: " + id_token);

        fetch(config.url + 'tokensignin/', {
            method: 'POST',
            body: 'idtoken=' + id_token,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            },
            credentials: "include"
        }).then((response) => {
            if (response.status == 400) {
                this.signOut();
                return;
            }

            return response.text();
        }, (error) => {
            console.log(error.message);
        }).then(text => {
            //console.log('Signed in as: ' + text);
            //console.log('csrftoken: ' + this.getCookie('csrftoken'));
        })
    }

    render() {
        return (
            <div>
                <div id="google-signin-button" className={this.state.isLogin ? "hide" : ""}></div>
                <div id="sign-out" className={this.state.isLogin ? "" : "hide"} onClick={this.signOut}>サインアウト</div>
            </div>
        )
    }
}

export default Login;