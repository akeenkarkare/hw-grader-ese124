import { useEffect } from "react";
import type { ComponentProps, Dispatch, SetStateAction,  } from "react";
import TopBar from "./TopBar";
import Display from "./Display";
import localData from "./data.json";
import Input from "./Input";
import type { FileNode, FolderNode } from "@/types/types";
/*for adding new files */
interface AddNewState {
  id?: string;
  type?: 'file' | 'folder';
  root?: boolean;
}

interface propsType {
  data: FileNode|FolderNode;
  setData: Dispatch<SetStateAction<FileNode>>;
  addNew: AddNewState;
  setAddNew: Dispatch<SetStateAction<AddNewState>>;

}

export default function FileExplorer({props}){
  const {data, setData, addNew, setAddNew} = props
 // 

/*  useEffect(() => {
    if (!localStorage.getItem("data")) {
      setData(localData);
      localStorage.setItem("data", JSON.stringify(localData));
    } else {
      setData(JSON.parse(localStorage.getItem("data")));
    }
  }, []);

  useEffect(() => {
    if (data) localStorage.setItem("data", JSON.stringify(data));
  }, [data]);*/

  

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