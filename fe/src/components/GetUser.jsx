import React, { useEffect, useState } from "react";
import { authyRequest } from "../AuthorizeAPI";
import { useAuth0 } from "@auth0/auth0-react";

export const GetUser = (props) => {
  let { whenUsed, currentUser } = props;
  let { getAccessTokenSilently } = useAuth0();
  let [token, setToken] = useState(null);
  const audience = "https://swap-bongobooks.herokuapp.com";
  const scope = "read:user";

  useEffect(async () => {
    setToken(await getAccessTokenSilently({ audience, scope }));
  }, []);

  return (
    <div>
      <h5>Get User</h5>

      <br />
      <br />

      <button
        className="btn btn-primary"
        onClick={() => {
          console.log(token);

          authyRequest(`/user/${currentUser}`, "GET", null, token).then((d) =>
            whenUsed(d)
          );
        }}
      >
        Get data
      </button>
      <br />
      <br />
    </div>
  );
};
