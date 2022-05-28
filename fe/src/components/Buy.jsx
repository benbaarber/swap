import React, { useState, useEffect } from "react";
import { post } from "../util";
import { useAuth0 } from "@auth0/auth0-react";
import { authyRequest } from "../AuthorizeAPI";

export const Buy = (props) => {
  let { whenUsed, currentUser } = props;
  let [newCoin, setNewCoin] = useState("");
  let [newAmount, setNewAmount] = useState(null);
  let { getAccessTokenSilently } = useAuth0();
  let [token, setToken] = useState(null);
  const audience = "https://swap-bongobooks.herokuapp.com";
  const scope = "create:investments";

  useEffect(async () => {
    setToken(await getAccessTokenSilently({ audience, scope }));
  }, []);

  return (
    <div>
      <h5>Buy</h5>
      <input
        type="text"
        placeholder="TICKER"
        value={newCoin}
        onChange={(e) => {
          setNewCoin(e.target.value.toUpperCase());
        }}
      />
      <input
        type="number"
        placeholder="NUMBER OF COINS"
        onChange={(e) => {
          setNewAmount(e.target.value);
        }}
      />
      <br />
      <br />

      <button
        className="btn btn-primary"
        onClick={() => {
          setNewCoin("");
          setNewAmount(null);
          authyRequest(
            `/user/${currentUser}/investments`,
            "POST",
            {
              coin: newCoin,
              amount: parseFloat(newAmount),
            },
            token
          ).then((d) => console.log(d.status));
        }}
      >
        {newCoin && newCoin.length > 0 && newAmount && newAmount.length > 0
          ? `Create new investment: ${newAmount} ${newCoin}`
          : "Type number of coins and ticker"}
      </button>
    </div>
  );
};
