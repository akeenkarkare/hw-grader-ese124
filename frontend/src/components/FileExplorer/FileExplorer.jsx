import React, { useState, useEffect } from "react";
import TopBar from "./TopBar";
import Display from "./Display";
import localData from "./data.json";
import Input from "./Input";

export default function FileExplorer(){
  const [data, setData] = useState([]);
  const [addNew, setAddNew] = useState({});

  useEffect(() => {
    if (!localStorage.getItem("data")) {
      setData(localData);
      localStorage.setItem("data", JSON.stringify(localData));
    } else {
      setData(JSON.parse(localStorage.getItem("data")));
    }
  }, []);

  useEffect(() => {
    if (data) localStorage.setItem("data", JSON.stringify(data));
  }, [data]);

  const props = {
    data,
    setData,
    addNew,
    setAddNew
  };

  return (
    <div className="block bg-gray-800 h-full p-4!">
      <div className="px-4 w-full min-w-[250px] sm:max-w-xs bg-gray-800">
        <TopBar {...{ addNew, setAddNew, root: true }} />
        {addNew && addNew.root && <Input {...{ addNew, setAddNew, setData }} />}
        <Display {...props} />
      </div>
    </div>
  );
}