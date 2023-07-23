import { Box, Flex } from '@chakra-ui/react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const prepareDataChart = ({ dataCOL, dataBFA }) => {
  let data = [];

  for (let index = 0; index < dataCOL.fcs_prevalence.length; index++) {
    const col = dataCOL.fcs_prevalence[index];
    const bfa = dataBFA.fcs_prevalence[index];

    data.push({
      name: col.date,
      col: col.prevalence,
      bfa: bfa.prevalence,
    });
  }

  return data;
};

export const MetricBChart = ({ dataCOL, dataBFA }) => {
  const preparedData = prepareDataChart({ dataCOL, dataBFA });

  return (
    <Flex alignItems="center" justifyContent="space-evenly">
      <Box width="100%">
        <LineChart
          width={800}
          height={350}
          data={preparedData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="col" stroke="#8884d8" />
          <Line type="monotone" dataKey="bfa" stroke="#82ca9d" />
        </LineChart>
      </Box>
    </Flex>
  );
};
