import React from "react";
import { Component } from 'react';

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
            gapi.auth2.init({ client_id: "895653784508-4pieb0kb7oo3blmvtetc1cc24pmm6d25.apps.googleusercontent.com" })
                .then(
                    (result) => {
                        gapi.signin2.render('google-signin-button', {
                            'onsuccess': this.onSignin,
                            'onfailure': (err) => console.error(err)
                        });
                    },
                    (err) => console.error(err)
                );
        })
    }

    getCookie = (name) => {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        console.log(parts);
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

    signOut=()=> {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then( ()=> {
            console.log('User signed out.');
            this.setState({isLogin:false});
            //console.log(this.state);
        });

        auth2.disconnect();

        fetch('http://localhost:8080/tokenlogout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCookie('csrftoken'),
            },
            credentials: 'same-origin',
        }).then((response) => {
          return response.text()  
        }).then((text) => {
            console.log(text);
        })
    }

    onSignin = (googleUser) => {
        var profile = googleUser.getBasicProfile();
        console.log("ID: " + profile.getId()); // Don't send this directly to your server!
        console.log('Full Name: ' + profile.getName());
        console.log('Given Name: ' + profile.getGivenName());
        console.log('Family Name: ' + profile.getFamilyName());
        console.log("Image URL: " + profile.getImageUrl());
        console.log("Email: " + profile.getEmail());
        this.setState({isLogin:true});
        // The ID token you need to pass to your backend:
        var id_token = googleUser.getAuthResponse().id_token;
        console.log("ID Token: " + id_token);

        fetch('http://localhost:8080/tokensignin/', {
            method: 'POST',
            body: 'idtoken=' + id_token,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': this.getCookie('csrftoken')
            },
            credentials: "same-origin"
        }).then((response) => {
            if (response.status == 400) {
                this.signOut();
                return;
            }

            return response.text();
        }, (error) => {
            console.log(error.message);
        }).then(text => {
            console.log('Signed in as: ' + text);
            console.log('csrftoken: ' + this.getCookie('csrftoken'));
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