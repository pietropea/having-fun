import { Box } from '@chakra-ui/react';

import { Divider } from '@chakra-ui/react';
import { MetricA } from './metrics/MetricA';
import { MetricB } from './metrics/MetricB';

export const Metrics = () => {
  return (
    <Box width={'100%'}>
      {/* <MetricA />

      <Divider /> */}

      <MetricB />
    </Box>
  );
};
