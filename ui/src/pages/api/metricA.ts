import type { NextApiRequest, NextApiResponse } from 'next'
import fetchMetricA from '../../lib/fetchMetricA'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  switch (req.method) {
    case 'GET':
      return fetchMetricA(req, res)
    default:
      return res.status(400).json({ message: 'Invalid method.' })
  }
}
