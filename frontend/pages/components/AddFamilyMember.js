import React from "react";

export default function AddFamilyMember(props) {
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
