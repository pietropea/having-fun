import { Box, ChakraProvider } from '@chakra-ui/react';
import { useState } from 'react';
import LangContext from '../contexts/langContext';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { Container } from '../components/Container';
import { IntlProvider } from 'react-intl';
import messagesInEng from '../lang/eng.json';
import ReactGA from 'react-ga4';
import theme from '../theme';
import { AppProps } from 'next/app';

const getLangMessages = ({ lang }) => {
  switch (lang) {
    case 'eng':
      return messagesInEng;
    default:
      return messagesInEng;
  }
};

const TRACKING_ID = process.env.NEXT_PUBLIC_GA_TRACKING_ID;
ReactGA.initialize(TRACKING_ID);

function MyApp({ Component, pageProps }: AppProps) {
  const [podcast, selectPodcast] = useState(null);
  const [podcasts, setPodcasts] = useState([]);
  const [isPlaying, setPlaying] = useState(false);
  const [seek, setSeek] = useState(0);
  const [playedSeconds, setPlayedSeconds] = useState(0);
  const [lang, setLang] = useState('ita');

  return (
    <IntlProvider
      messages={getLangMessages({ lang })}
      locale={lang}
      defaultLocale="ita"
    >
      <LangContext.Provider value={{ lang, setLang }}>
        <ChakraProvider theme={theme}>
          <Container
            backgroundColor="gray.50"
            minHeight="100rem"
            justifyContent="space-evenly"
            width="100%"
          >
            <Box
              backgroundColor="white"
              minHeight="100rem"
              justifyContent="space-evenly"
              width={{ base: '100%', md: '100%', xl: '1400px' }}
            >
              <Header />

              <Component {...pageProps} />

              <Footer />
            </Box>
          </Container>
        </ChakraProvider>
      </LangContext.Provider>
    </IntlProvider>
  );
}

export default MyApp;
