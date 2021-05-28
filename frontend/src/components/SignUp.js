import React, { useState } from 'react';
import { CognitoUserPool } from 'amazon-cognito-identity-js';
import Modal from './LoginForm';
import './../App.css';

const SignUp = () => {
    const [login, setLogin] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState('');
    const poolData = {
        UserPoolId: "us-east-2_eb2BISGw2", //Change This UserPoolId
        ClientId: "sv1jhfkl5gdkb2qjkkf62327c" //Change This ClientId
    };

    const userPool = new CognitoUserPool(poolData);

    const onsubmit = e => {
        e.preventDefault()
        console.log("submitting....")
        userPool.signUp(email, password, [], null, (err, data) => {
            if (err) {
                setError("Incorrect Sign Up Info");
            }else{
                setError("Success! Plz Check Your Email For Verification.")
            };
        })
    };

    function change(){
        setLogin(true)
    }

    if (login) return <Modal></Modal>;

    return (
        <div className="wrapper">
            <div className="form">
                <h1 className="title">Sign Up Form</h1>
                    <form onSubmit={onsubmit}>
                        <input placeholder="Email" id="username" className="input" type="text" value={email} onChange={e => setEmail(e.target.value)}></input>
                        <input placeholder="Password" id="passwd" className="input" type="text" value={password} onChange={e => setPassword(e.target.value)}></input>
                        <div align="center">
                            <button className="button" type="submit">Sign Up</button>
                        </div>
                    </form>
                    <div align="center">
                        <button className="button" onClick={change}>Back</button>
                    </div>
                    <h1>{error}</h1>
            </div>
        </div>
    );
};

export default SignUp;
