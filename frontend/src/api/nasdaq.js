/**
 * API service for Nasdaq data
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Fetch historical Nasdaq data
 * @param {string} startDate - Start date in YYYY-MM-DD format
 * @param {string} endDate - End date in YYYY-MM-DD format
 * @returns {Promise<Object>} Historical data response
 */
export const fetchHistoricalData = async (startDate, endDate) => {
  const params = {}
  if (startDate) params.start_date = startDate
  if (endDate) params.end_date = endDate

  const response = await api.get('/nasdaq/historical', { params })
  return response.data
}

/**
 * Fetch decline periods
 * @param {string} startDate - Start date in YYYY-MM-DD format
 * @param {string} endDate - End date in YYYY-MM-DD format
 * @param {number} threshold - Minimum decline percentage (default: 0.10)
 * @returns {Promise<Object>} Decline periods response
 */
export const fetchDeclinePeriods = async (startDate, endDate, threshold = 0.10) => {
  const params = { threshold }
  if (startDate) params.start_date = startDate
  if (endDate) params.end_date = endDate

  const response = await api.get('/nasdaq/declines', { params })
  return response.data
}

/**
 * Fetch latest data point
 * @returns {Promise<Object>} Latest data response
 */
export const fetchLatestData = async () => {
  const response = await api.get('/nasdaq/latest')
  return response.data
}

/**
 * Trigger data update from Yahoo Finance
 * @returns {Promise<Object>} Update result
 */
export const triggerDataUpdate = async () => {
  const response = await api.post('/nasdaq/update')
  return response.data
}

export default api
