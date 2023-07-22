import type { MetricAData } from '../interfaces'
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((res) => res.json())

export default function useMetricA({ iso3, dateStart, dateEnd }) {

  const { data: articles, mutate, error, isLoading } = useSWR<MetricAData[]>(
    `/api/metricA/${iso3}?date_start=${dateStart}&date_end=${dateEnd}`,
    fetcher,
    { fallbackData: [] }
  )

  const fetchMetricA = async ({ date }) => {
    try {

      mutate()
    } catch (err) {
      console.log(err)
    }
  }

  return { articles, fetchMetricA, error, isLoading }
}
