import { Card, CardBody, Text } from '@chakra-ui/react';

type ErrorBoxProps = {
  message: string;
};

export const ErrorBox = ({ message }: ErrorBoxProps) => {
  return (
    <Card>
      <CardBody>
        <Text>{message}</Text>
      </CardBody>
    </Card>
  );
};
