import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import { Auth0Provider, useAuth0 } from "@auth0/auth0-react";
import "./style.css";
import { GetUser } from "./components/GetUser";
import { Buy } from "./components/Buy";
import { ListInvestments } from "./components/ListInvestments";
import { GiveBonus } from "./components/GiveBonus";
import { LoginButton } from "./components/LoginButton";
import { LogoutButton } from "./components/LogoutButton";
import { Profile } from "./components/Profile";
import { authyRequest } from "./AuthorizeAPI";

const App = () => {
  // let [currentUser, setCurrentUser] = useState(undefined);
  let [data, setData] = useState(undefined);
  let { user, isAuthenticated, getAccessTokenSilently } = useAuth0();

  useEffect(async () => {
    console.log("called on isauth change");
    const audience = "https://swap-bongobooks.herokuapp.com";
    const scope = "read:user";

    if (isAuthenticated) {
      let token = await getAccessTokenSilently({ audience, scope });
      authyRequest(
        "/user",
        "POST",
        {
          username: user.name,
        },
        token
      ).then((d) => {
        switch (d.status) {
          case 406:
            console.log("Username is not set");
          case 409:
            console.log("Username already exists in DB");
          case 201:
            console.log("User successfully created in DB");
          default:
            console.log("Base case, status is: " + d.status);
        }
      });
    }
  }, [isAuthenticated, user]);

  return (
    <div className="container">
      <h5>UI</h5>
      <br />
      <br />
      <LoginButton />
      <Profile />
      <LogoutButton />

      <hr></hr>
      {isAuthenticated ? (
        <div>
          <GetUser
            whenUsed={(d) => {
              setData(d);
            }}
            currentUser={user.email}
          />

          {data != undefined ? <code>{JSON.stringify(data)}</code> : <></>}

          <hr></hr>

          {user ? (
            <div>
              <Buy whenUsed={() => {}} currentUser={user.name} />
              <br />
              <br />
              <hr></hr>
              <ListInvestments whenUsed={() => {}} currentUser={user.name} />
            </div>
          ) : (
            <></>
          )}

          <br />
          <br />
          <hr />

          <GiveBonus whenUsed={() => {}} />
        </div>
      ) : (
        <></>
      )}
    </div>
  );
};

ReactDOM.render(
  <Auth0Provider
    domain="dev-h0m7eost.us.auth0.com"
    clientId="0bRcYNnpzByw7zol0Dke6h3DnGDnXiOK"
    redirectUri={"https://swap-bongobooks.herokuapp.com/index.html"}
    audience="https://swap-bongobooks.herokuapp.com"
    scope="read:investments create:investments delete:investments read:user update:user"
  >
    <App />
  </Auth0Provider>,
  document.getElementById("react-hook")
);
