import { Data, DataNode, FileNode, FolderNode } from "@/types/types";
import JSZip from "jszip";

export async function dataToZip(data: Data): Promise<string> {
  if(data.language_id == 89){
    const zip = new JSZip();
    let {language_id, additional_files, compile_id, run_id} = data; 
    
    let q = []
    
    let curr: JSZip= zip;
    q.push(additional_files);

    while(q.length){ // BSF through files, make a tree
      let file: DataNode = q.shift();
      if(file.kind == "folder"){
        let folder = file as FolderNode;
        curr.folder(folder.name);
        q.push(folder.children); // enqueue children 
      } else {
        file = file as FileNode;
        curr.file(file.name, file.source_code);
      }
    }
    additional_files.forEach((file: DataNode) => {
      if(file.kind == "folder"){
        zip.folder(file.name)
      }
    })
    return zip.generateAsync({type: 'base64'});
  } else {
    return '#include <stdio.h>\n\nint main() {\n    // Single file generation not implemented\n    \n    return 0;\n}'
  }
  
}
