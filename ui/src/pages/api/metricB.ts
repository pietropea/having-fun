import type { NextApiRequest, NextApiResponse } from 'next'
import fetchMetricB from '../../lib/fetchMetricB'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  switch (req.method) {
    case 'GET':
      return fetchMetricB(req, res)
    default:
      return res.status(400).json({ message: 'Invalid method.' })
  }
}
