import { Box } from '@chakra-ui/react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  // ResponsiveContainer,
} from 'recharts';

export const MetricBChart = ({ data }) => {
  return (
    <Box width="100%">
      <LineChart
        width={500}
        height={300}
        data={data}
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
        <Line
          type="monotone"
          dataKey="col"
          stroke="#8884d8"
          // activeDot={{ r: 8 }}
        />
        <Line type="monotone" dataKey="bfa" stroke="#82ca9d" />
      </LineChart>
    </Box>
  );
};
