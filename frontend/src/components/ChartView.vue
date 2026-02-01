<template>
  <div class="bg-white rounded-lg shadow p-2 sm:p-4 lg:p-6 mb-1 sm:mb-6">
    <h2 class="text-xs sm:text-xl font-semibold text-gray-900 mb-1 sm:mb-4">K線圖表</h2>
    
    <div class="relative">
      <!-- Chart Container -->
      <div ref="chartContainer" class="w-full" :style="chartStyle"></div>
      
      <!-- Loading Overlay -->
      <div
        v-if="loading"
        class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center"
      >
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-nasdaq-blue"></div>
      </div>
    </div>

    <!-- Chart Info -->
    <div class="hidden sm:block mt-1.5 sm:mt-4 text-xs sm:text-sm text-gray-600">
      <p>
        紅色區域表示下跌期間 (峰值到谷底 >10%)
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'
import { createChart } from 'lightweight-charts'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  declinePeriods: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['ready'])

// Track selected alert level
const selectedAlert = ref({
  periodStartDate: null,
  level: null
})

// Responsive chart height
const chartStyle = computed(() => {
  // Use window.innerWidth to determine device size
  const width = typeof window !== 'undefined' ? window.innerWidth : 1024
  const height = width < 640 ? '280px' : width < 1024 ? '350px' : '500px'
  return `height: ${height};`
})

let currentPriceLine = null

/**
 * Highlight alert level on chart
 */
const highlightAlertLevel = (period, level) => {
  if (!candlestickSeries || !chart) return

  // Check if clicking the same alert level - toggle off
  if (selectedAlert.value.periodStartDate === period.start_date && 
      selectedAlert.value.level === level) {
    // Clear selection
    selectedAlert.value.periodStartDate = null
    selectedAlert.value.level = null
    
    // Remove price line if exists
    if (currentPriceLine) {
      candlestickSeries.removePriceLine(currentPriceLine)
      currentPriceLine = null
    }
    
    // Reset to original view
    updateChart()
    return
  }

  // Update selected alert
  selectedAlert.value.periodStartDate = period.start_date
  selectedAlert.value.level = level

  // Calculate the price at this alert level
  const alertPrice = period.peak_value * (1 - level / 100)
  
  // Find the date when price first reached this level during the decline
  const startTime = new Date(period.start_date).getTime() / 1000
  const endTime = new Date(period.end_date).getTime() / 1000
  
  const periodData = props.data.filter(d => {
    const time = new Date(d.date).getTime() / 1000
    return time >= startTime && time <= endTime && d.close <= alertPrice
  })
  
  // Remove old price line if exists
  if (currentPriceLine) {
    candlestickSeries.removePriceLine(currentPriceLine)
  }
  
  if (periodData.length > 0) {
    // Find first occurrence
    const alertDate = periodData[0]
    const alertTime = new Date(alertDate.date).getTime() / 1000
    
    // Create a price line at the alert level
    currentPriceLine = candlestickSeries.createPriceLine({
      price: alertPrice,
      color: '#3B82F6',
      lineWidth: 2,
      lineStyle: 2, // Dashed
      axisLabelVisible: true,
      title: `${level}% 下跌警報`,
    })
  }
  
  // Update chart with highlighted period
  updateChart()
  
  // Center the decline period in the chart view (maintain current zoom level)
  setTimeout(() => {
    if (!chart) return
    
    // Get the current visible range to maintain zoom level
    const timeScale = chart.timeScale()
    const currentRange = timeScale.getVisibleRange()
    
    if (!currentRange) return
    
    // Calculate current visible range duration
    const currentDuration = currentRange.to - currentRange.from
    
    // Calculate the middle point of the decline period
    const middleTime = (startTime + endTime) / 2
    
    // Set new range with the same duration, centered on the decline period
    const newFrom = middleTime - (currentDuration / 2)
    const newTo = middleTime + (currentDuration / 2)
    
    // Scroll to the new range while maintaining zoom level
    timeScale.setVisibleRange({
      from: newFrom,
      to: newTo
    })
  }, 100) // Small delay to ensure chart is updated
}

// Expose method to parent
defineExpose({
  highlightAlertLevel
})

const chartContainer = ref(null)
let chart = null
let candlestickSeries = null
let declineBackgroundSeries = [] // Store decline background series

/**
 * Initialize chart
 */
const initChart = () => {
  if (!chartContainer.value) return

  // Get responsive height
  const width = typeof window !== 'undefined' ? window.innerWidth : 1024
  const height = width < 640 ? 280 : width < 1024 ? 350 : 500

  // Create chart
  chart = createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
    height: height,
    layout: {
      background: { color: '#ffffff' },
      textColor: '#333'
    },
    grid: {
      vertLines: { color: '#f0f0f0' },
      horzLines: { color: '#f0f0f0' }
    },
    crosshair: {
      mode: 1
    },
    rightPriceScale: {
      borderColor: '#d1d4dc'
    },
    timeScale: {
      borderColor: '#d1d4dc',
      timeVisible: true,
      secondsVisible: false
    }
  })

  // Add candlestick series
  candlestickSeries = chart.addCandlestickSeries({
    upColor: '#10B981',
    downColor: '#EF4444',
    borderUpColor: '#10B981',
    borderDownColor: '#EF4444',
    wickUpColor: '#10B981',
    wickDownColor: '#EF4444'
  })

  // Handle window resize
  const handleResize = () => {
    if (chart && chartContainer.value) {
      chart.applyOptions({
        width: chartContainer.value.clientWidth
      })
    }
  }
  window.addEventListener('resize', handleResize)

  return () => {
    window.removeEventListener('resize', handleResize)
  }
}

/**
 * Update chart data with optimized rendering
 */
const updateChart = () => {
  if (!candlestickSeries || props.data.length === 0) return

  // Use requestAnimationFrame for smoother rendering
  requestAnimationFrame(() => {
    // Convert data to chart format (minimize object creation)
    const candleData = props.data.map(item => ({
      time: new Date(item.date).getTime() / 1000,
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close
    }))

    // Set data
    candlestickSeries.setData(candleData)

    // Add decline period background shading
    addDeclineBackgrounds()

    // Add decline period markers
    addDeclineMarkers()

    // Fit content
    chart.timeScale().fitContent()
  })
}

/**
 * Add background shading for decline periods (optimized)
 */
const addDeclineBackgrounds = () => {
  if (!chart || props.declinePeriods.length === 0) return

  // Remove old background series efficiently
  while (declineBackgroundSeries.length > 0) {
    const series = declineBackgroundSeries.pop()
    chart.removeSeries(series)
  }

  // Pre-convert all dates to timestamps for faster lookup
  const dataTimestamps = new Map()
  props.data.forEach(d => {
    dataTimestamps.set(new Date(d.date).getTime() / 1000, d)
  })

  // Add background for each decline period
  props.declinePeriods.forEach((period) => {
    const startTime = new Date(period.start_date).getTime() / 1000
    const endTime = new Date(period.end_date).getTime() / 1000

    // Filter data using Map for faster lookup
    const periodData = props.data.filter(d => {
      const time = new Date(d.date).getTime() / 1000
      return time >= startTime && time <= endTime
    })

    if (periodData.length === 0) return

    // Find max high in the period for the top of the shaded area
    let maxHigh = period.peak_value
    let minLow = period.trough_value
    
    for (const d of periodData) {
      if (d.high > maxHigh) maxHigh = d.high
      if (d.low < minLow) minLow = d.low
    }

    // Check if this period is selected
    const isSelected = selectedAlert.value.periodStartDate === period.start_date
    
    // Choose colors based on selection state
    const topColor = isSelected ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'
    const bottomColor = isSelected ? 'rgba(16, 185, 129, 0.05)' : 'rgba(239, 68, 68, 0.05)'
    const lineColor = isSelected ? 'rgba(16, 185, 129, 0.4)' : 'rgba(239, 68, 68, 0.4)'

    // Create an area series to fill the decline period with red or green background
    const bgSeries = chart.addAreaSeries({
      topColor,
      bottomColor,
      lineColor,
      lineWidth: 2,
      priceLineVisible: false,
      lastValueVisible: false,
      crosshairMarkerVisible: false,
    })

    // Create data points covering the entire decline period
    // Use the peak value as the fill height to show the full decline area
    const fillData = periodData.map(d => ({
      time: new Date(d.date).getTime() / 1000,
      value: maxHigh
    }))

    bgSeries.setData(fillData)
    declineBackgroundSeries.push(bgSeries)

    // Add another series for the bottom boundary line
    const bottomLineSeries = chart.addLineSeries({
      color: 'rgba(239, 68, 68, 0.3)',
      lineWidth: 1,
      priceLineVisible: false,
      lastValueVisible: false,
      crosshairMarkerVisible: false,
      lineStyle: 2, // Dashed line
    })

    const bottomLineData = periodData.map(d => ({
      time: new Date(d.date).getTime() / 1000,
      value: minLow
    }))

    bottomLineSeries.setData(bottomLineData)
    declineBackgroundSeries.push(bottomLineSeries)
  })
}

/**
 * Add markers for decline periods
 */
const addDeclineMarkers = () => {
  if (!candlestickSeries || props.declinePeriods.length === 0) return

  const markers = []

  props.declinePeriods.forEach(period => {
    // Peak marker (start)
    markers.push({
      time: new Date(period.start_date).getTime() / 1000,
      position: 'aboveBar',
      color: '#EF4444',
      shape: 'arrowDown',
      text: `峰值: ${period.peak_value.toFixed(2)}`
    })

    // Trough marker (end) - only if decline ended
    if (period.end_date && !period.is_ongoing) {
      markers.push({
        time: new Date(period.end_date).getTime() / 1000,
        position: 'belowBar',
        color: '#10B981',
        shape: 'arrowUp',
        text: `谷底: ${period.trough_value.toFixed(2)} (-${period.decline_percentage.toFixed(1)}%)`
      })
    }

    // Ongoing decline marker
    if (period.is_ongoing) {
      markers.push({
        time: new Date(period.end_date).getTime() / 1000,
        position: 'belowBar',
        color: '#F59E0B',
        shape: 'circle',
        text: `進行中: -${period.decline_percentage.toFixed(1)}%`
      })
    }
  })

  candlestickSeries.setMarkers(markers)
}

// Initialize chart on mount
onMounted(() => {
  const cleanup = initChart()
  updateChart()

  onUnmounted(() => {
    if (cleanup) cleanup()
    if (chart) chart.remove()
  })
})

// Watch for data changes
watch(() => [props.data, props.declinePeriods], () => {
  updateChart()
}, { deep: true })
</script>
