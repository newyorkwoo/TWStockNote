<template>
  <div class="bg-white rounded-lg shadow p-2 sm:p-4 lg:p-6 mb-2 sm:mb-6">
    <h2 class="text-sm sm:text-xl font-semibold text-gray-900 mb-2 sm:mb-4">下跌警報</h2>

    <div v-if="periods.length === 0" class="text-sm sm:text-base text-gray-600">
      在選定的時間範圍內沒有偵測到下跌期間。
    </div>

    <div v-else class="space-y-2 sm:space-y-4">
      <!-- Ongoing Decline Alert -->
      <div
        v-for="period in ongoingPeriods"
        :key="period.start_date"
        class="border-l-4 border-nasdaq-red bg-red-50 p-2 sm:p-4 rounded-r-lg"
      >
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg
              class="h-4 w-4 sm:h-6 sm:w-6 text-nasdaq-red"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <div class="ml-1.5 sm:ml-3 flex-1">
            <h3 class="text-sm sm:text-lg font-medium text-red-900">
              ⚠️ 進行中的下跌
            </h3>
            <div class="mt-1 sm:mt-2 text-xs sm:text-sm text-red-800">
              <p>
                <strong>峰值日期:</strong>
                {{ formatDate(period.start_date) }}
              </p>
              <p>
                <strong>峰值價格:</strong>
                {{ period.peak_value.toFixed(2) }}
              </p>
              <p>
                <strong>當前價格:</strong>
                {{ period.trough_value?.toFixed(2) || 'N/A' }}
              </p>
              <p class="text-lg font-bold mt-2">
                <strong>下跌幅度:</strong>
                {{ period.decline_percentage.toFixed(2) }}%
              </p>
              <div v-if="period.alert_levels.length > 0" class="mt-3">
                <strong>觸發的警報等級:</strong>
                <div class="flex flex-wrap gap-2 sm:gap-3 mt-2">
                  <button
                    v-for="level in period.alert_levels"
                    :key="level"
                    @click="handleAlertLevelClick(period, level)"
                    :class="getButtonClass(period, level, true)"
                  >
                    {{ level }}%
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Historical Decline Periods -->
      <div
        v-for="period in completedPeriods"
        :key="period.start_date"
        class="border-l-4 border-gray-300 bg-gray-50 p-2 sm:p-4 rounded-r-lg"
      >
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg
              class="h-4 w-4 sm:h-6 sm:w-6 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div class="ml-1.5 sm:ml-3 flex-1">
            <h3 class="text-sm sm:text-lg font-medium text-gray-900">
              歷史下跌期間
            </h3>
            <div class="mt-1 sm:mt-2 text-xs sm:text-sm text-gray-700">
              <p>
                <strong>期間:</strong>
                {{ formatDate(period.start_date) }} →
                {{ formatDate(period.end_date) }}
              </p>
              <p>
                <strong>峰值價格:</strong>
                {{ period.peak_value.toFixed(2) }}
              </p>
              <p>
                <strong>谷底價格:</strong>
                {{ period.trough_value?.toFixed(2) || 'N/A' }}
              </p>
              <p class="font-bold">
                <strong>最大下跌幅度:</strong>
                {{ period.decline_percentage.toFixed(2) }}%
              </p>
              <div v-if="period.alert_levels.length > 0" class="mt-1.5 sm:mt-3">
                <strong>觸發的警報等級:</strong>
                <div class="flex flex-wrap gap-2 sm:gap-3 mt-1.5 sm:mt-2">
                  <button
                    v-for="level in period.alert_levels"
                    :key="level"
                    @click="handleAlertLevelClick(period, level)"
                    :class="getButtonClass(period, level, false)"
                  >
                    {{ level }}%
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  periods: {
    type: Array,
    required: true
  },
  selectedAlert: {
    type: Object,
    default: () => ({ periodStartDate: null, level: null })
  }
})

const emit = defineEmits(['alert-level-click'])

/**
 * Handle alert level click
 */
const handleAlertLevelClick = (period, level) => {
  emit('alert-level-click', { period, level })
}

/**
 * Check if alert level button is selected
 */
const isAlertSelected = (period, level) => {
  return props.selectedAlert.periodStartDate === period.start_date && 
         props.selectedAlert.level === level
}

/**
 * Get button class based on selection state
 */
const getButtonClass = (period, level, isOngoing = false) => {
  const isSelected = isAlertSelected(period, level)
  
  if (isSelected) {
    return 'px-3 sm:px-4 py-2 sm:py-2.5 min-h-[44px] bg-green-500 text-white rounded-lg text-sm sm:text-base font-medium ring-2 ring-green-600 ring-offset-1 transition-all cursor-pointer active:scale-95'
  }
  
  if (isOngoing) {
    // For ongoing periods, use the original alert level colors
    let baseClass = 'px-3 sm:px-4 py-2 sm:py-2.5 min-h-[44px] rounded-lg text-sm sm:text-base font-medium hover:ring-2 hover:ring-offset-1 hover:ring-blue-500 transition-all cursor-pointer active:scale-95 '
    if (level >= 30) return baseClass + 'bg-red-700 text-white'
    if (level >= 25) return baseClass + 'bg-red-600 text-white'
    if (level >= 20) return baseClass + 'bg-red-500 text-white'
    if (level >= 15) return baseClass + 'bg-orange-500 text-white'
    return baseClass + 'bg-orange-400 text-white'
  }
  
  // For historical periods
  return 'px-3 sm:px-4 py-2 sm:py-2.5 min-h-[44px] bg-gray-200 text-gray-700 rounded-lg text-sm sm:text-base font-medium hover:bg-blue-500 hover:text-white transition-all cursor-pointer active:scale-95'
}

/**
 * Filter ongoing decline periods
 */
const ongoingPeriods = computed(() => {
  return props.periods.filter(p => p.is_ongoing)
})

/**
 * Filter completed decline periods (sorted by date, newest first)
 */
const completedPeriods = computed(() => {
  return props.periods
    .filter(p => !p.is_ongoing)
    .sort((a, b) => new Date(b.start_date) - new Date(a.start_date))
})

/**
 * Format date string
 */
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

/**
 * Get CSS class for alert level badge
 */
const getAlertLevelClass = (level) => {
  if (level >= 30) return 'bg-red-700 text-white'
  if (level >= 25) return 'bg-red-600 text-white'
  if (level >= 20) return 'bg-red-500 text-white'
  if (level >= 15) return 'bg-orange-500 text-white'
  return 'bg-orange-400 text-white'
}
</script>
