import React, { useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import { FcFolder, FcFile } from "react-icons/fc";
export default function Input(props) {
  const { addNew, setAddNew, setData } = props;
  const myRef = useRef(null);

  const handleOnSubmit = (e) => {
    e.preventDefault();
    
    // Prevent empty names
    if (!myRef.current.value.trim()) {
      setAddNew({});
      return;
    }
    
    let data;
    if (addNew.type === "file") {
      data = {
        id: uuidv4(),
        type: "file",
        name: myRef.current.value.trim()
      };
    } else {
      data = {
        id: uuidv4(),
        children: [],
        type: "folder",
        name: myRef.current.value.trim()
      };
    }
    
    if (addNew.root) {
      setData((prev) => [data, ...prev]);
    } else {
      setData((prev) => {
        // Create new array with immutable update
        let newPrev = prev.map((pd) => {
          if (pd.id === addNew.id) {
            return {
              ...pd,
              children: [...pd.children, data.id]
            };
          }
          return pd;
        });
        return [data, ...newPrev];
      });
    }
    
    setAddNew({});
  };

  const handleBlur = (e) => {
    // Only close if clicking outside the form entirely
    if (!e.currentTarget.contains(e.relatedTarget)) {
      setAddNew({});
    }
  };

  return (
    <form
      onSubmit={handleOnSubmit}
      onBlur={handleBlur}
      className="mt-2 space-x-2 flex items-center"
    >
      {addNew.type === "file" && <FcFile fontSize={22} />}
      {addNew.type === "folder" && <FcFolder fontSize={22} />}
      <input
        ref={myRef}
        autoFocus
        maxLength={16}
        className="flex-1 rounded-md p-1 px-2 text-gray-200 bg-transparent border"
      />
    </form>
  );
}
