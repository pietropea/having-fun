import { useRef } from 'react';
import { Flex, Heading, Spacer, Box } from '@chakra-ui/layout';
import {
  Button,
  Drawer,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
} from '@chakra-ui/react';
import Link from 'next/link';
import { GiHamburgerMenu } from 'react-icons/gi';
import { FormattedMessage } from 'react-intl';
import { createTracker } from './analytics/Tracker';

const tracker = createTracker('header');

export const Header = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = useRef();

  return (
    <>
      <Flex
        flexDirection="row"
        // position="fixed"
        as="nav"
        alignItems="center"
        padding="5"
        minW="100%"
        boxShadow="xs"
      >
        <Link href="/">
          <Heading as="h1">
            <FormattedMessage id="logo" defaultMessage="Having Fun" />
          </Heading>
        </Link>

        <Spacer />

        <Box
          display={{
            base: 'flex',
            md: 'none',
          }}
        >
          <Button ref={btnRef} onClick={onOpen}>
            <GiHamburgerMenu />
          </Button>
        </Box>
      </Flex>

      <Drawer
        isOpen={isOpen}
        placement="right"
        onClose={onClose}
        finalFocusRef={btnRef}
      >
        <DrawerOverlay />

        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>
            <FormattedMessage id="logo" defaultMessage="Having Fun" />
          </DrawerHeader>
          <DrawerBody></DrawerBody>
          <DrawerFooter></DrawerFooter>
        </DrawerContent>
      </Drawer>
    </>
  );
};
