'use strict';

const AuthInfoKey = 'conduktor_auth_info';

export function getAuthData() {
    const authInfo = JSON.parse(localStorage.getItem(AuthInfoKey)) || {};

    return {
        loggedIn: !!authInfo.token,
        name: authInfo.name || '',
        token: authInfo.token || '',
    };
}

export function extractAuthData(googleUser, store) {
    const token = googleUser.getAuthResponse().id_token;
    const user = googleUser.getBasicProfile();
    const email = user.getEmail();

    const domains = window.ConduktorConfig ? window.ConduktorConfig.AUTHORIZED_DOMAINS : process.env.AUTHORIZED_DOMAINS.split(',');

    if (!domains.includes(email.split('@')[1].toLowerCase())) {
        throw new Error('Your e-mail address does not belong to an authorized domain. Please try again.');
    }

    localStorage.setItem(
        AuthInfoKey, 
        JSON.stringify({
            name: user.getName(),
            token: token,
        })
    );

    return {
        loggedIn: true,
        name: user.getName(),
        token: token,
    };
}

export function logout() {
    localStorage.removeItem(AuthInfoKey);
}