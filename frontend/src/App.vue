<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow flex-shrink-0">
      <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8 py-1.5 sm:py-4">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-1.5 sm:gap-0">
          <div>
            <h1 class="text-base sm:text-2xl lg:text-3xl font-bold text-gray-900">
              Nasdaq 下跌分析
            </h1>
          </div>
          <button
            @click="updateData"
            :disabled="loading"
            class="hidden sm:block px-4 py-2 bg-nasdaq-blue text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm sm:text-base"
          >
            {{ loading ? '更新中...' : '更新資料' }}
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-hidden">
      <div class="h-full flex flex-col max-w-7xl mx-auto px-2 sm:px-4 lg:px-8 py-2 sm:py-6 lg:py-8">
        <!-- Top Section: Date Picker, Chart -->
        <div class="flex-shrink-0">
          <!-- Date Range Picker -->
          <DateRangePicker
            :start-date="startDate"
            :end-date="endDate"
            @update:start-date="startDate = $event"
            @update:end-date="endDate = $event"
            @apply="loadData"
          />

          <!-- Chart View -->
          <ChartView
            ref="chartViewRef"
            v-if="historicalData.length > 0"
            :data="historicalData"
            :decline-periods="declinePeriods"
            :loading="loading"
            class="chart-container"
          />

          <!-- Loading State -->
          <div v-if="loading && historicalData.length === 0" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-nasdaq-blue"></div>
            <p class="mt-4 text-gray-600">載入資料中...</p>
          </div>

          <!-- Error State -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-800">{{ error }}</p>
          </div>
        </div>

        <!-- Scrollable Decline Alerts Section -->
        <div class="flex-1 overflow-y-auto mt-2 sm:mt-6" v-if="declinePeriods.length > 0">
          <DeclineAlert
            :periods="declinePeriods"
            :selected-alert="selectedAlert"
            @alert-level-click="handleAlertLevelClick"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChartView from './components/ChartView.vue'
import DateRangePicker from './components/DateRangePicker.vue'
import DeclineAlert from './components/DeclineAlert.vue'
import { fetchHistoricalData, fetchDeclinePeriods, fetchLatestData, triggerDataUpdate } from './api/nasdaq'

// State
const historicalData = ref([])
const declinePeriods = ref([])
const latestData = ref(null)
const loading = ref(false)
const error = ref(null)
const chartViewRef = ref(null)
const loadingTimeoutId = ref(null)
const selectedAlert = ref({
  periodStartDate: null,
  level: null
})

// Date range (default: last 5 years)
const endDate = ref(new Date().toISOString().split('T')[0])
const startDate = ref(
  new Date(new Date().setFullYear(new Date().getFullYear() - 5))
    .toISOString()
    .split('T')[0]
)

/**
 * Load historical data and decline periods with debouncing
 */
const loadData = async () => {
  // Clear any pending load requests
  if (loadingTimeoutId.value) {
    clearTimeout(loadingTimeoutId.value)
  }
  
  // Debounce: wait 300ms before actually loading
  return new Promise((resolve) => {
    loadingTimeoutId.value = setTimeout(async () => {
      loading.value = true
      error.value = null

      try {
        // Fetch data in parallel for better performance
        const [histData, periods, latest] = await Promise.all([
          fetchHistoricalData(startDate.value, endDate.value),
          fetchDeclinePeriods(startDate.value, endDate.value),
          fetchLatestData()
        ])

        historicalData.value = histData.data
        declinePeriods.value = periods.periods
        latestData.value = latest

        console.log(`Loaded ${histData.total_count} data points and ${periods.total_count} decline periods`)
        resolve()
      } catch (err) {
        error.value = `載入資料失敗: ${err.message}`
        console.error('Error loading data:', err)
        resolve()
      } finally {
        loading.value = false
      }
    }, 300)
  })
}

/**
 * Update data from Yahoo Finance
 */
const updateData = async () => {
  loading.value = true
  error.value = null

  try {
    const result = await triggerDataUpdate()
    console.log('Data updated:', result)
    
    // Reload data after update
    await loadData()
  } catch (err) {
    error.value = `更新資料失敗: ${err.message}`
    console.error('Error updating data:', err)
  } finally {
    loading.value = false
  }
}

/**
 * Handle alert level click from DeclineAlert component
 */
const handleAlertLevelClick = ({ period, level }) => {
  console.log(`Alert level clicked: ${level}% for period ${period.start_date}`)
  
  // Check if clicking the same alert - toggle off
  if (selectedAlert.value.periodStartDate === period.start_date && 
      selectedAlert.value.level === level) {
    selectedAlert.value.periodStartDate = null
    selectedAlert.value.level = null
  } else {
    // Update selected alert
    selectedAlert.value.periodStartDate = period.start_date
    selectedAlert.value.level = level
  }
  
  // Call the chart's highlight method
  if (chartViewRef.value) {
    chartViewRef.value.highlightAlertLevel(period, level)
    
    // Scroll to chart
    const chartElement = document.querySelector('.chart-container')
    if (chartElement) {
      chartElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }
}

// Load data on mount
onMounted(() => {
  loadData()
})
</script>
