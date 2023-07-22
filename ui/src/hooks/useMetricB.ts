import type { MetricBData } from '../interfaces'
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((res) => res.json())

export default function useMetricB({ iso3, dateStart, dateEnd, includeVariance }) {

  const { data, isLoading, error } = useSWR<MetricBData[]>(
    `/api/metricB/?iso3=${iso3}&dateStart=${dateStart}&dateEnd=${dateEnd}&includeVariance=${includeVariance}`,
    fetcher
  )

  return { data, isLoading, error }
}
