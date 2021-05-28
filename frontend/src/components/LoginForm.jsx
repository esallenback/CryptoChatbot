import { useState } from 'react';
import axios from 'axios';
import SignUp from './SignUp';
import {
  CognitoUserPool,
} from 'amazon-cognito-identity-js';

var AmazonCognitoIdentity = require('amazon-cognito-identity-js');
const projectID = 'c2d9d192-c769-47b1-8406-3c3b6489dc73';

const Modal = () => {
  const [signup, setUp] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const authObject = { 'Project-ID': projectID, 'User-Name': username, 'User-Secret': password };

    try {
      await axios.get('https://api.chatengine.io/chats', { headers: authObject });

      localStorage.setItem('username', username);
      localStorage.setItem('password', password);

      window.location.reload();
      setError('');
    } catch (err) {
      var authenticationData = {
        Username: username,
        Password: password,
      };
      var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(
        authenticationData
      );
      var poolData = {
        UserPoolId: "us-east-2_eb2BISGw2", //Change This UserPoolId
        ClientId: "sv1jhfkl5gdkb2qjkkf62327c" //Change This ClientId
      };
      var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
      var userData = {
        Username: username,
        Pool: userPool,
      };
      var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function () {
          localStorage.setItem('username', "cryptocurrent");
          localStorage.setItem('password', "zPM8GtxD34oHQV");
    
          window.location.reload();
          setError('');
        },
        onFailure: function () {
          setError('Oops, incorrect credentials.');
        },
      });
    }
  };

function change() {
  setUp(true)
};

if (signup) return <SignUp></SignUp>;

return (
  <div className="wrapper">
    <div className="form">
      <h1 className="title">Chat Application</h1>
      <form onSubmit={handleSubmit}>
        <input id="username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="input" placeholder="Username" required />
        <input id="passwd" type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="input" placeholder="Password" required />
        <div align="center">
          <button type="submit" className="button">
            <span>Start chatting</span>
          </button>
        </div>
      </form>
      <div align="center">
        <button type="submit" className="button" onClick={change}>
          <span>Sign Up</span>
        </button>
        <h1>{error}</h1>
      </div>
    </div>
  </div>
);
};

export default Modal;
