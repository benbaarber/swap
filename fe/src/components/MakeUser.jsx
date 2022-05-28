import React, { useState } from "react";
import { post } from "../util";

export const MakeUser = (props) => {
  let { whenUsed } = props;
  let [newUsername, setNewUsername] = useState(undefined);

  return (
    <div>
      <h5>Create User</h5>
      <input
        type="text"
        placeholder="username"
        onChange={(e) => {
          setNewUsername(e.target.value);
        }}
      />
      <br />
      <br />
      <button
        className="btn btn-primary"
        onClick={() => {
          whenUsed();
          post("/user", { username: newUsername }).then((d) => alert(d.status));
        }}
      >
        {newUsername && newUsername.length > 0
          ? `Create new user: ${newUsername}`
          : "Type your username."}
      </button>
    </div>
  );
};
