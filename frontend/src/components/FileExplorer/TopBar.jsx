import React from "react";
import New from "./New";

export default function TopBar(props) {
  return (
    <div className="div-top-bar flex items-center justify-between border-b pb-2">
      <p className="p-tb font-bold uppercase text-gray-400 text-xs tracking-wide">
        file explorer
      </p>
      <New {...props} />
    </div>
  );
}
