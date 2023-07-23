import { Box, Button, Center, Flex, HStack, Spacer } from '@chakra-ui/react';
import { createTracker } from '../analytics/Tracker';
import { Metrics } from '../components/Metrics';

const tracker = createTracker('home');

const Index = () => {
  return (
    <>
      <Flex
        pt="2rem"
        px="1rem"
        width={{
          base: '100%',
        }}
        justifyContent="space-evenly"
      >
        <Metrics />
      </Flex>
    </>
  );
};

export default Index;
