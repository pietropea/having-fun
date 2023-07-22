import { Box } from '@chakra-ui/react';
import { FormattedMessage } from 'react-intl';
import { MetricTitle } from '../layout/MetricTitle';

export const MetricA = () => {
  return (
    <Box width="100%">
      <MetricTitle>
        <FormattedMessage
          id="metrics.metricA.title"
          defaultMessage="Metric A"
        />
      </MetricTitle>
      This is
    </Box>
  );
};
