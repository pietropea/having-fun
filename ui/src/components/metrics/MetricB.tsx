import { useState, useEffect } from 'react';
import {
  Accordion,
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Divider,
} from '@chakra-ui/react';
import { FormattedMessage } from 'react-intl';
import { MetricTitle } from '../layout/MetricTitle';
import useMetricB from '../../hooks/useMetricB';
import { Loading } from '../Loading';
import { ErrorBox } from '../ErrorBox';
import { MetricBChart } from '../viz/MetricBChart';
import {
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
} from '@chakra-ui/react';

export const MetricB = () => {
  const dateStart = '2022-06-01';
  const dateEnd = '2023-07-01';
  const includeVariance = 'false';

  const {
    data: dataCOL,
    isLoading: isLoadingCOL,
    error: errorCOL,
  } = useMetricB({
    iso3: 'COL',
    dateStart,
    dateEnd,
    includeVariance,
  });

  const {
    data: dataBFA,
    isLoading: isLoadingBFA,
    error: errorBFA,
  } = useMetricB({
    iso3: 'BFA',
    dateStart,
    dateEnd,
    includeVariance,
  });

  const hasError = !!errorCOL || !!errorBFA;

  return (
    <Box width="100%">
      <MetricTitle>
        <FormattedMessage
          id="metrics.metricB.title"
          defaultMessage="Metric B"
        />
      </MetricTitle>

      <Box p="2rem" />

      {(isLoadingCOL || isLoadingBFA) && <Loading />}

      {hasError && (
        <ErrorBox message="Something went wrong while retrieving you data :/ Please refresh the page" />
      )}

      {!hasError && dataCOL && dataBFA && (
        <MetricBChart dataCOL={dataCOL} dataBFA={dataBFA} />
      )}

      <Accordion allowToggle pt="5em">
        <AccordionItem>
          <h2>
            <AccordionButton>
              <Box as="span" flex="1" textAlign="left">
                Logs
              </Box>
              <AccordionIcon />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4}>
            <TableContainer>
              <Table variant="simple">
                <Thead>
                  <Tr>
                    <Th>Country</Th>
                    <Th>Is Loading</Th>
                    <Th>Has error</Th>
                    <Th>Data returned</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  <Tr>
                    <Td>Colombia</Td>
                    <Td>{String(isLoadingCOL)}</Td>
                    <Td>{String(!!errorCOL)}</Td>
                    <Td>{String(!!dataCOL)}</Td>
                  </Tr>
                  <Tr>
                    <Td>Burkina Faso</Td>
                    <Td>{String(isLoadingBFA)}</Td>
                    <Td>{String(!!errorBFA)}</Td>
                    <Td>{String(!!dataBFA)}</Td>
                  </Tr>
                </Tbody>
              </Table>
            </TableContainer>
          </AccordionPanel>
        </AccordionItem>
      </Accordion>
    </Box>
  );
};
