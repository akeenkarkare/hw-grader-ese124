import React, { useEffect, useState } from "react";
import File from "./File";
import Folder from "./Folder";

export default function Display(props) {
  const { data, setData, addNew, setAddNew } = props;
  const [open, setOpen] = useState([]);

  useEffect(() => {
    if (addNew) {
      setOpen((prev) => {
        if (!prev || prev.length === 0) {
          return [addNew.id];
        }
        if (!prev.includes(addNew.id)) {
          return [...prev, addNew.id];
        }
        return prev;
      });
    }
  }, [addNew]);

  const toggleFolderState = (id) => {
    if (open.length === 0) {
      setOpen([id]);
    } else {
      if (open.includes(id)) setOpen((prev) => prev.filter((p) => p !== id));
      else setOpen((prev) => [...prev, id]);
    }
  };

  const getChild = (cd) => {
    return data.find((d) => d.id === cd);
  };

  const getChildrens = () => {
    if (data) {
      const folders = data.filter((d) => d.children && d.children.length > 0);
      let childrens = [];

      folders.forEach((fd) => {
        fd.children.forEach((cd) => {
          childrens.push(cd);
        });
      });
      return childrens;
    }
  };

  const getRootFolders = () => {
    if (data) {
      const childrens = getChildrens();
      let rootFolders = [];
      data.forEach((d) => {
        if (!childrens.includes(d.id)) {
          rootFolders.push(d);
        }
      });
      return rootFolders;
    }
    return [];
  };

  const render = () => {
    return getRootFolders().map((d) => {
      if (d.type === "folder")
        return (
          <Folder
            key={d.id}
            {...{
              data: d,
              getChild,
              open,
              toggleFolderState,
              addNew,
              setAddNew,
              setData
            }}
          />
        );
      if (d.type === "file") return <File key={d.id} {...{ data: d }} />;
      return null;
    });
  };

  return <div>{data && render()}</div>;
}
