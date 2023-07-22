import type { NextApiRequest, NextApiResponse } from 'next'

export default async function fetchMetricB(
  req: NextApiRequest,
  res: NextApiResponse
) {

  const { iso3, dateStart, dateEnd, includeVariance } = req.query
  let API_URL = `${process.env.API_BASE_URL}daily_fcs/${iso3}?`

  if (dateStart) {
    API_URL = `${API_URL}date_start=${dateStart}&`
  }

  if (dateEnd) {
    API_URL = `${API_URL}date_end=${dateEnd}&`
  }

  if (includeVariance) {
    API_URL = `${API_URL}include_variance=${includeVariance}&`
  }

  const headers = {
    headers: {
      // Authorization: `Bearer ${token}`
    }
  }

  const response = await fetch(API_URL, headers);
  let data = await response.json();

  return res.status(200).json(data)
}
