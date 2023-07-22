import type { NextApiRequest, NextApiResponse } from 'next'

export default async function fetchPodcasts(
  req: NextApiRequest,
  res: NextApiResponse
) {

  try {

    if (req.query && req.query.date) {

      const database_url = `${process.env.DATABASE_URL}/podcasts?date=${req.query.date}`
      // `/api/food_security/averages/${iso3}?date_start=${dateStart}&date_end=${dateEnd}`,

      const headers = {
        headers: {
          // Authorization: `Bearer ${database_token}`
        }
      }

      const response = await fetch(database_url, headers);
      let data = await response.json();
      let p = data.podcasts

      return res.status(200).json({
        hello: "Hi!"
      })

    } else {
      return res.status(200).json([])
    }
  } catch (_) {
    return res.status(500).json({ message: 'Unexpected error occurred.' })
  }
}
