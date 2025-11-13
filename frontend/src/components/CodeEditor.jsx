import Editor from '@monaco-editor/react'

const CodeEditor = ({ value, onChange, height = '400px' }) => {
  return (
    <Editor
      height={height}
      defaultLanguage="c"
      theme="vs-dark"
      value={value}
      onChange={onChange}
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
        automaticLayout: true,
      }}
    />
  )
}

export default CodeEditor

