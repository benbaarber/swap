import React, { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { authyRequest } from "../AuthorizeAPI";
import { postNewUser } from "../util";
import { GetUser } from "./GetUser";

export const LoginButton = () => {
  const { loginWithRedirect, isAuthenticated, user } = useAuth0();
  const audience = "https://swap-bongobooks.herokuapp.com";
  const scope = "read:user";

  useEffect(async () => {
    if (isAuthenticated) {
      let token = await getAccessTokenSilently({ audience, scope });

      authyRequest(
        `/user`,
        "POST",
        {
          username: user.name,
        },
        token
      ).then((d) =>
        d.status == 409
          ? console.log("User already exists")
          : console.log(d.status)
      );
    }
  }, []);

  return !isAuthenticated ? (
    <button onClick={() => loginWithRedirect()}>Log In</button>
  ) : (
    <></>
  );
};
