import ReactGA from 'react-ga4';

export function createTracker(category: string) {
  return {
    event: (action: string, label: string) => {
      ReactGA.event({ category, action, label });
    },
    page: (title: string) => {
      ReactGA.send({ hitType: 'pageview', page: '/' + category, title: title });
    },
  };
}
