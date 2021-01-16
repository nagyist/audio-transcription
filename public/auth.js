const ui = new firebaseui.auth.AuthUI(firebase.auth());

const uiConfig = {
    callbacks: {
        signInSuccessWithAuthResult(authResult, redirectUrl) {
            var token = authResult.credential.accessToken;
            var user = authResult.user;
            return true;
        },
        uiShown() {
            // document.getElementById('loader').style.display = 'none';
        },
    },
    signInFlow: 'popup',
    signInSuccessUrl: '/',
    signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
    ],
};
ui.start('#firebaseui-auth-container', uiConfig);
console.log("bar");

// gapi set token ref https://github.com/google/google-api-javascript-client/issues/304


