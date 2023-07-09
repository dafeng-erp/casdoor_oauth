// Copyright 2021 The casbin Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
class Sdk {
    constructor(config) {
        this.config = config;
        if (config.redirectPath === undefined || config.redirectPath === null) {
            this.config.redirectPath = "/callback";
        }
    }
    getSignupUrl(enablePassword = true) {
        if (enablePassword) {
            sessionStorage.setItem("signinUrl", this.getSigninUrl());
            return `${this.config.serverUrl.trim()}/signup/${this.config.appName}`;
        }
        else {
            return this.getSigninUrl().replace("/login/oauth/authorize", "/signup/oauth/authorize");
        }
    }
    getOrSaveState() {
        const state = sessionStorage.getItem("casdoor-state");
        if (state !== null) {
            return state;
        }
        else {
            const state = Math.random().toString(36).slice(2);
            sessionStorage.setItem("casdoor-state", state);
            return state;
        }
    }
    clearState() {
        sessionStorage.removeItem("casdoor-state");
    }
    getSigninUrl() {
        const redirectUri = this.config.redirectPath && this.config.redirectPath.includes('://') ? this.config.redirectPath : `${window.location.origin}${this.config.redirectPath}`;
        const scope = "read";
        const state = this.getOrSaveState();
        return `${this.config.serverUrl.trim()}/login/oauth/authorize?client_id=${this.config.clientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${scope}&state=${state}`;
    }
    getUserProfileUrl(userName, account) {
        let param = "";
        if (account !== undefined && account !== null) {
            param = `?access_token=${account.accessToken}`;
        }
        return `${this.config.serverUrl.trim()}/users/${this.config.organizationName}/${userName}${param}`;
    }
    getMyProfileUrl(account, returnUrl = "") {
        let params = "";
        if (account !== undefined && account !== null) {
            params = `?access_token=${account.accessToken}`;
            if (returnUrl !== "") {
                params += `&returnUrl=${returnUrl}`;
            }
        }
        else if (returnUrl !== "") {
            params = `?returnUrl=${returnUrl}`;
        }
        return `${this.config.serverUrl.trim()}/account${params}`;
    }
    async signin(serverUrl, signinPath, code, state) {
        if (!code || !state) {
            const params = new URLSearchParams(window.location.search);
            code = params.get("code");
            state = params.get("state");
        }
        const expectedState = this.getOrSaveState();
        this.clearState();
        if (state !== expectedState) {
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve({
                        // @ts-ignore
                        status: "error",
                        msg: `invalid state parameter, expected: ${expectedState}, got: ${state}`,
                    });
                }, 10);
            });
        }
        return fetch(`${serverUrl}${signinPath || this.config.signinPath || '/api/signin'}?code=${code}&state=${state}`, {
            method: "POST",
            credentials: "include",
        }).then(res => res.json());
    }
    isSilentSigninRequested() {
        const params = new URLSearchParams(window.location.search);
        return params.get("silentSignin") === "1";
    }
    silentSignin(onSuccess, onFailure) {
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = `${this.getSigninUrl()}&silentSignin=1`;
        const handleMessage = (event) => {
            if (window !== window.parent) {
                return null;
            }
            const message = event.data;
            if (message.tag !== "Casdoor" || message.type !== "SilentSignin") {
                return;
            }
            if (message.data === 'success') {
                onSuccess(message);
            }
            else {
                onFailure(message);
            }
        };
        window.addEventListener('message', handleMessage);
        document.body.appendChild(iframe);
    }
    async popupSignin(serverUrl, signinPath, callback) {
        const width = 500;
        const height = 600;
        const left = window.screen.width / 2 - width / 2;
        const top = window.screen.height / 2 - height / 2;
        const popupWindow = window.open(this.getSigninUrl() + "&popup=1", "login", `width=${width},height=${height},top=${top},left=${left}`);
        const handleMessage = (event) => {
            if (event.origin !== this.config.serverUrl) {
                return;
            }
            if (event.data.type === "windowClosed" && callback) {
                callback("login failed");
            }
            if (event.data.type === "loginSuccess") {
                this.signin(serverUrl, signinPath, event.data.data.code, event.data.data.state)
                    .then((res) => {
                    sessionStorage.setItem("token", res.token);
                    window.location.reload();
                });
                popupWindow.close();
            }
        };
        window.addEventListener("message", handleMessage);
    }
}
export default Sdk;