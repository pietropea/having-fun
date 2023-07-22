import { useState, useEffect } from 'react';
import { Box } from '@chakra-ui/react';
import { FormattedMessage } from 'react-intl';
import { MetricTitle } from '../layout/MetricTitle';
import useMetricB from '../../hooks/useMetricB';
import { Loading } from '../Loading';
import { MetricBChart } from '../viz/MetricBChart';

const prepareDataChart = ({ dataCOL, dataBFA }) => {
  let data = [];

  // console.log(dataCOL);
  // console.log(dataBFA);

  for (let index = 0; index < dataCOL.fcs_prevalence.length; index++) {
    const col = dataCOL.fcs_prevalence[index];
    const bfa = dataBFA.fcs_prevalence[index];

    data.push({
      name: col.name,
      col: col.prevalence,
      bfa: bfa.prevalence,
    });
  }

  return data;
};

export const MetricB = () => {
  const dateStart = '2022-06-01';
  const dateEnd = '2023-07-01';
  const includeVariance = 'true';

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

  console.log(errorCOL);
  console.log(errorBFA);

  return (
    <Box width="100%">
      <MetricTitle>
        <FormattedMessage
          id="metrics.metricB.title"
          defaultMessage="Metric B"
        />
      </MetricTitle>

      {(isLoadingCOL || isLoadingBFA) && <Loading />}

      {(errorCOL || errorBFA) && <div>OPS</div>}

      {/* {!errorCOL && !errorBFA && dataCOL && dataBFA && (
        <MetricBChart
          data={prepareDataChart({
            dataCOL,
            dataBFA,
          })}
        />
      )} */}
    </Box>
  );
};
