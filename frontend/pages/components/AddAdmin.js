import React from "react";

export default function AddAdmin(props) {
  return props.trigger ? (
    <div className="withdrawcard">
      <div
      //className=""
      >
        {props.children}
      </div>
    </div>
  ) : (
    ""
  );
}
