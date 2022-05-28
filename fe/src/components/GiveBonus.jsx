import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { authyRequest } from "../AuthorizeAPI";
import { patch } from "../util";

export const GiveBonus = (props) => {
  let { whenUsed } = props;
  let [oneLuckySOB, setOneLuckySOB] = useState(undefined);
  let [bonus, setBonus] = useState(undefined);
  let { getAccessTokenSilently } = useAuth0();
  let [token, setToken] = useState(null);
  const audience = "https://swap-bongobooks.herokuapp.com";
  const scope = "update:user";

  useEffect(async () => {
    setToken(await getAccessTokenSilently({ audience, scope }));
  }, []);

  return (
    <div>
      <h5>Give Bonus</h5>
      <input
        type="text"
        placeholder="username"
        value={oneLuckySOB}
        onChange={(e) => {
          setOneLuckySOB(e.target.value);
        }}
      />
      <input
        type="number"
        placeholder="amount"
        value={bonus}
        onChange={(e) => {
          setBonus(e.target.value);
        }}
      />
      <br />
      <br />
      <button
        className="btn btn-primary"
        onClick={() => {
          whenUsed();
          setOneLuckySOB("");
          setBonus(null);
          authyRequest(
            `/user/${oneLuckySOB}`,
            "PATCH",
            { bonus: bonus },
            token
          );
          // .then((d) => {console.log(d.status); return d})
          // .then((d) => {
          //   d.status >= 400
          //     ? alert("Only administrators can perform this action")
          //     : alert(`Bonus awarded to ${oneLuckySOB}`); return d
          // });
        }}
      >
        {oneLuckySOB && oneLuckySOB.length > 0 && bonus && bonus > 0
          ? `Give ${bonus} to ${oneLuckySOB}`
          : "Type user and bonus amount."}
      </button>
    </div>
  );
};
