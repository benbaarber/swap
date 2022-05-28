import React, { useState, useEffect } from "react";
import { sell } from "../util";
import { useAuth0 } from "@auth0/auth0-react";
import { authyRequest } from "../AuthorizeAPI";

export const ListInvestments = (props) => {
  let { whenUsed, currentUser } = props;
  let [investments, setInvestments] = useState(undefined);
  let [ID, setID] = useState(undefined);
  let { getAccessTokenSilently } = useAuth0();
  let [token, setToken] = useState(null);
  const audience = "https://swap-bongobooks.herokuapp.com";
  const scope = "read:investments delete:investments";

  useEffect(async () => {
    setToken(await getAccessTokenSilently({ audience, scope }));
  }, []);

  return (
    <div>
      <h5>List Investments</h5>
      <button
        className="btn btn-primary"
        onClick={() => {
          authyRequest(
            `/user/${currentUser}/investments`,
            "GET",
            null,
            token
          ).then((d) => setInvestments(d));
        }}
      >
        Update
      </button>
      <br />
      <br />
      {investments && investments.data ? (
        investments.data.map((e, i) => (
          <div style={{}} key={"unique" + i}>
            {`Investment ID: ${e.id} | ${e.amount} ${e.coin} on ${e.date}`}
            <button
              className="btn btn-primary"
              onClick={() => {
                authyRequest(
                  `/user/${currentUser}/investments/${e.id}`,
                  "DELETE",
                  null,
                  token
                )
                  .then((d) => console.log(d.status))
                  .then(() =>
                    authyRequest(
                      `/user/${currentUser}/investments`,
                      "GET",
                      null,
                      token
                    )
                  )
                  .then((d) => setInvestments(d));
              }}
            ></button>
          </div>
        ))
      ) : (
        <></>
      )}
      <br />
      <br />
    </div>
  );
};
