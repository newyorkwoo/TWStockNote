<template>
  <div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">統計資訊</h2>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Latest Price -->
      <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4">
        <div class="text-sm font-medium text-blue-600 mb-1">最新價格</div>
        <div class="text-2xl font-bold text-blue-900">
          {{ latest.close.toFixed(2) }}
        </div>
        <div class="text-xs text-blue-600 mt-1">
          {{ formatDate(latest.date) }}
        </div>
      </div>

      <!-- Daily Change -->
      <div
        :class="[
          'rounded-lg p-4',
          dailyChange >= 0
            ? 'bg-gradient-to-br from-green-50 to-green-100'
            : 'bg-gradient-to-br from-red-50 to-red-100'
        ]"
      >
        <div
          :class="[
            'text-sm font-medium mb-1',
            dailyChange >= 0 ? 'text-green-600' : 'text-red-600'
          ]"
        >
          當日變化
        </div>
        <div
          :class="[
            'text-2xl font-bold',
            dailyChange >= 0 ? 'text-green-900' : 'text-red-900'
          ]"
        >
          {{ dailyChange >= 0 ? '+' : '' }}{{ dailyChange.toFixed(2) }}
        </div>
        <div
          :class="[
            'text-xs mt-1',
            dailyChange >= 0 ? 'text-green-600' : 'text-red-600'
          ]"
        >
          {{ dailyChangePercent >= 0 ? '+' : '' }}{{ dailyChangePercent.toFixed(2) }}%
        </div>
      </div>

      <!-- Current Status -->
      <div
        :class="[
          'rounded-lg p-4',
          currentDecline
            ? 'bg-gradient-to-br from-red-50 to-red-100'
            : 'bg-gradient-to-br from-green-50 to-green-100'
        ]"
      >
        <div
          :class="[
            'text-sm font-medium mb-1',
            currentDecline ? 'text-red-600' : 'text-green-600'
          ]"
        >
          當前狀態
        </div>
        <div
          :class="[
            'text-lg font-bold',
            currentDecline ? 'text-red-900' : 'text-green-900'
          ]"
        >
          {{ currentDecline ? '下跌中' : '正常' }}
        </div>
        <div
          v-if="currentDecline"
          :class="['text-xs mt-1', 'text-red-600']"
        >
          -{{ currentDecline.decline_percentage.toFixed(2) }}%
        </div>
      </div>

      <!-- Volume -->
      <div class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4">
        <div class="text-sm font-medium text-purple-600 mb-1">成交量</div>
        <div class="text-2xl font-bold text-purple-900">
          {{ formatVolume(latest.volume) }}
        </div>
        <div class="text-xs text-purple-600 mt-1">
          {{ formatDate(latest.date) }}
        </div>
      </div>
    </div>

    <!-- Additional Info for Current Decline -->
    <div
      v-if="currentDecline"
      class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg"
    >
      <h3 class="text-sm font-semibold text-red-900 mb-2">
        ⚠️ 下跌期間資訊
      </h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
        <div>
          <span class="text-red-600">峰值日期:</span>
          <div class="font-medium text-red-900">
            {{ formatDate(currentDecline.start_date) }}
          </div>
        </div>
        <div>
          <span class="text-red-600">峰值價格:</span>
          <div class="font-medium text-red-900">
            {{ currentDecline.peak_value.toFixed(2) }}
          </div>
        </div>
        <div>
          <span class="text-red-600">當前價格:</span>
          <div class="font-medium text-red-900">
            {{ currentDecline.trough_value?.toFixed(2) || 'N/A' }}
          </div>
        </div>
        <div>
          <span class="text-red-600">下跌幅度:</span>
          <div class="font-bold text-red-900 text-lg">
            {{ currentDecline.decline_percentage.toFixed(2) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  latest: {
    type: Object,
    required: true
  },
  currentDecline: {
    type: Object,
    default: null
  }
})

/**
 * Calculate daily change
 */
const dailyChange = computed(() => {
  return props.latest.close - props.latest.open
})

/**
 * Calculate daily change percentage
 */
const dailyChangePercent = computed(() => {
  return (dailyChange.value / props.latest.open) * 100
})

/**
 * Format date string
 */
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

/**
 * Format volume with suffixes (K, M, B)
 */
const formatVolume = (volume) => {
  if (volume >= 1e9) {
    return (volume / 1e9).toFixed(2) + 'B'
  } else if (volume >= 1e6) {
    return (volume / 1e6).toFixed(2) + 'M'
  } else if (volume >= 1e3) {
    return (volume / 1e3).toFixed(2) + 'K'
  }
  return volume.toString()
}
</script>
