import { Flex, FlexProps, Text } from '@chakra-ui/react';
import { FormattedMessage } from 'react-intl';

export const Footer = (props: FlexProps) => (
  <Flex as="footer" py="6rem" justifyContent="space-evenly" {...props}>
    <Text color="text" fontSize="1rem">
      <FormattedMessage id="footer" defaultMessage="Built with ❤️" />
    </Text>
  </Flex>
);
