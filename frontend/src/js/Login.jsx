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

    getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        console.log(parts);
        if (parts.length == 2) return parts.pop().split(";").shift();
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
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:8080/tokensignin/');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', this.getCookie('csrftoken'));
        xhr.withCredentials = true;
        var _this = this;
        xhr.onload = function () {
            if (xhr.status == 400) {
                var auth2 = gapi.auth2.getAuthInstance();
                auth2.signOut().then(function () {
                    console.log('invalid mail address');
                })
                auth2.disconnect();
                return;
            }
            console.log('Signed in as: ' + xhr.responseText);
            console.log('csrftoken: ' + _this.getCookie('csrftoken'));
        };
        xhr.send('idtoken=' + id_token);
    }

    signOut=()=> {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then( ()=> {
            console.log('User signed out.');
            this.setState({isLogin:false});
            //console.log(this.state);
        });
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:8080/tokenlogout/');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.withCredentials = true;
        xhr.onload = function () {
            console.log(xhr.responseText);
        }
        xhr.send();
        auth2.disconnect();
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