import React from 'react';

const LangContext = React.createContext({
  lang: 'eng',
  setLang: (lang: string) => {},
});
export default LangContext;
